import type { AxiosRequestConfig, AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import type { RequestOptions, Result, UploadFileParams } from '/#/axios';
import type { CreateAxiosOptions } from './axiosTransform';
import axios from 'axios';
import qs from 'qs';
import { AxiosCanceler } from './axiosCancel';
import { isFunction } from '/@/utils/is';
import { cloneDeep } from 'lodash-es';
import { ContentTypeEnum } from '/@/enums/httpEnum';
import { RequestEnum } from '/@/enums/httpEnum';
import { PageEnum } from '/@/enums/pageEnum';
import { router } from '/@/router';
import { clearAuthCache, getToken, setToken } from '/@/utils/auth';
import { doLogout } from '/@/api/sys/user';
import { checkStatus } from '/@/utils/http/axios/checkStatus';
import { useMessage } from '/@/hooks/web/useMessage';

export * from './axiosTransform';

let isRefreshing = false;
const refreshSubscribers = [];

/**
 * @description:  axios module
 */
export class VAxios {
  private axiosInstance: AxiosInstance;
  private readonly options: CreateAxiosOptions;

  constructor(options: CreateAxiosOptions) {
    this.options = options;
    this.axiosInstance = axios.create(options);
    this.setupInterceptors();
  }

  /**
   * @description:  Create axios instance
   */
  private createAxios(config: CreateAxiosOptions): void {
    this.axiosInstance = axios.create(config);
  }

  private getTransform() {
    const { transform } = this.options;
    return transform;
  }

  getAxios(): AxiosInstance {
    return this.axiosInstance;
  }

  /**
   * @description: Reconfigure axios
   */
  configAxios(config: CreateAxiosOptions) {
    if (!this.axiosInstance) {
      return;
    }
    this.createAxios(config);
  }

  /**
   * @description: Set general header
   */
  setHeader(headers: any): void {
    if (!this.axiosInstance) {
      return;
    }
    Object.assign(this.axiosInstance.defaults.headers, headers);
  }

  /**
   * @description: Interceptor configuration
   */
  private setupInterceptors() {
    const transform = this.getTransform();
    if (!transform) {
      return;
    }
    const {
      requestInterceptors,
      requestInterceptorsCatch,
      responseInterceptors,
      responseInterceptorsCatch,
    } = transform;

    const axiosCanceler = new AxiosCanceler();

    // Request interceptor configuration processing
    this.axiosInstance.interceptors.request.use((config: AxiosRequestConfig) => {
      // If cancel repeat request is turned on, then cancel repeat request is prohibited
      // @ts-ignore
      const { ignoreCancelToken } = config.requestOptions;
      const ignoreCancel =
        ignoreCancelToken !== undefined
          ? ignoreCancelToken
          : this.options.requestOptions?.ignoreCancelToken;

      !ignoreCancel && axiosCanceler.addPending(config);
      if (requestInterceptors && isFunction(requestInterceptors)) {
        config = requestInterceptors(config, this.options);
      }
      return config;
    }, undefined);

    // Request interceptor error capture
    requestInterceptorsCatch &&
      isFunction(requestInterceptorsCatch) &&
      this.axiosInstance.interceptors.request.use(undefined, requestInterceptorsCatch);

    // Response result interceptor processing
    this.axiosInstance.interceptors.response.use(
      (res: AxiosResponse<any>) => {
        if (res.data.code === 403) {
          router.push(PageEnum.ERROR_PAGE_403);
        } else if (res.data.code === 401) {
          const dom = document.getElementsByClassName('error401-modal');
          if (dom?.length === 0) {
            useMessage().createErrorModal({
              iconType: 'error',
              title: () => '用户信息发生变更',
              content: () => '需要重新登录',
              showOkCancel: false,
              class: 'error401-modal',
              onOk: () => {
                clearAuthCache();
                router.push(PageEnum.BASE_LOGIN);
              },
              onCancel: () => {
                clearAuthCache();
                router.push(PageEnum.BASE_LOGIN);
              },
            });
          }
        }
        res && axiosCanceler.removePending(res.config);
        if (responseInterceptors && isFunction(responseInterceptors)) {
          res = responseInterceptors(res);
        }
        return res;
      },
      (error) => {
        const { response } = error;
        if (response !== undefined) {
          const {
            config,
            response: { status },
          } = error;
          const originalRequest = config;
          if (status === 499) {
            if (!isRefreshing) {
              isRefreshing = true;
              const token = getToken();
              // @ts-ignore
              const refreshToken = token.refresh_token;
              const config = {
                headers: {
                  Authorization: `Bearer ${refreshToken}`,
                },
              };
              // @ts-ignore
              const env = import.meta.env;
              const urlPrefix = env.VITE_API_URI;
              axios
                .get(`${urlPrefix}/auth/refresh`, config)
                .then((res) => {
                  isRefreshing = false;
                  if (res.data.code === 200) {
                    const token = res.data.data;
                    setToken(token);
                    onRefreshed(token.access_token);
                  } else if (res.data.code === 302) {
                    clearAuthCache();
                    window.location.href = res.data.data.redirect_url;
                  } else {
                    clearAuthCache();
                    router.push(PageEnum.BASE_LOGIN);
                  }
                })
                .catch(() => {
                  clearAuthCache();
                  router.push(PageEnum.BASE_LOGIN);
                });
            }

            return new Promise((resolve) => {
              subscribeTokenRefresh((token) => {
                originalRequest.headers.Authorization = `Bearer ${token}`;
                resolve(axios(originalRequest));
              });
            });
          } else if (error.response.status === 401) {
            clearAuthCache();
            doLogout().then(async () => {
              await router.push(PageEnum.BASE_LOGIN);
            });
          } else if (error.response.status === 500) {
            router.push(PageEnum.RESULT_PAGE);
          } else {
            return Promise.reject(error);
          }
        } else {
          checkStatus(502, '');
        }
      },
    );

    // Response result interceptor error capture
    responseInterceptorsCatch &&
      isFunction(responseInterceptorsCatch) &&
      this.axiosInstance.interceptors.response.use(undefined, (error) => {
        console.log(this.axiosInstance);
        console.log(error);
        // @ts-ignore
        responseInterceptorsCatch(this.axiosInstance, error);
      });
  }

  /**
   * @description:  File Upload
   */
  uploadFile<T = any>(config: AxiosRequestConfig, params: UploadFileParams) {
    const formData = new window.FormData();
    const customFilename = params.name || 'file';

    if (params.filename) {
      formData.append(customFilename, params.file, params.filename);
    } else {
      formData.append(customFilename, params.file);
    }

    if (params.data) {
      Object.keys(params.data).forEach((key) => {
        const value = params.data![key];
        if (Array.isArray(value)) {
          value.forEach((item) => {
            formData.append(`${key}[]`, item);
          });
          return;
        }

        formData.append(key, params.data![key]);
      });
    }

    return this.axiosInstance.request<T>({
      ...config,
      method: 'POST',
      data: formData,
      headers: {
        'Content-type': ContentTypeEnum.FORM_DATA,
        // @ts-ignore
        ignoreCancelToken: true,
      },
    });
  }

  // support form-data
  supportFormData(config: AxiosRequestConfig) {
    const headers = config.headers || this.options.headers;
    const contentType = headers?.['Content-Type'] || headers?.['content-type'];

    if (
      contentType !== ContentTypeEnum.FORM_URLENCODED ||
      !Reflect.has(config, 'data') ||
      config.method?.toUpperCase() === RequestEnum.GET
    ) {
      return config;
    }

    return {
      ...config,
      data: qs.stringify(config.data, { arrayFormat: 'brackets' }),
    };
  }

  get<T = any>(config: AxiosRequestConfig, options?: RequestOptions): Promise<T> {
    return this.request({ ...config, method: 'GET' }, options);
  }

  post<T = any>(config: AxiosRequestConfig, options?: RequestOptions): Promise<T> {
    return this.request({ ...config, method: 'POST' }, options);
  }

  put<T = any>(config: AxiosRequestConfig, options?: RequestOptions): Promise<T> {
    return this.request({ ...config, method: 'PUT' }, options);
  }

  delete<T = any>(config: AxiosRequestConfig, options?: RequestOptions): Promise<T> {
    return this.request({ ...config, method: 'DELETE' }, options);
  }

  request<T = any>(config: AxiosRequestConfig, options?: RequestOptions): Promise<T> {
    let conf: CreateAxiosOptions = cloneDeep(config);
    const transform = this.getTransform();

    const { requestOptions } = this.options;

    const opt: RequestOptions = Object.assign({}, requestOptions, options);

    const { beforeRequestHook, requestCatchHook, transformRequestHook } = transform || {};
    if (beforeRequestHook && isFunction(beforeRequestHook)) {
      conf = beforeRequestHook(conf, opt);
    }
    conf.requestOptions = opt;

    conf = this.supportFormData(conf);

    return new Promise((resolve, reject) => {
      this.axiosInstance
        .request<any, AxiosResponse<Result>>(conf)
        .then((res: AxiosResponse<Result>) => {
          if (transformRequestHook && isFunction(transformRequestHook)) {
            try {
              const ret = transformRequestHook(res, opt);
              resolve(ret);
            } catch (err) {
              reject(err || new Error('request error!'));
            }
            return;
          }
          resolve(res as unknown as Promise<T>);
        })
        .catch((e: Error | AxiosError) => {
          if (requestCatchHook && isFunction(requestCatchHook)) {
            reject(requestCatchHook(e, opt));
            return;
          }
          if (axios.isAxiosError(e)) {
            // rewrite error message from axios in here
          }
          reject(e);
        });
    });
  }
}

function onRefreshed(token) {
  // @ts-ignore
  refreshSubscribers.map((cb) => cb(token));
}

function subscribeTokenRefresh(cb) {
  // @ts-ignore
  refreshSubscribers.push(cb);
}
