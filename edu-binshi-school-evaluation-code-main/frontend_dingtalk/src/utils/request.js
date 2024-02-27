import axios from 'axios'
import router from '../router'
import {Notify} from "vant";

let isRefreshing = false
const refreshSubscribers = []

/**
 * @description axios初始化
 */
const instance = axios.create({
    baseURL: import.meta.env.VITE_GLOB_API_URL,
});


/**
 * @description axios响应拦截器
 */


instance.interceptors.response.use(response => {
    return response
}, error => {
    const {message} = error
    if (message === 'Network Error') {
        Notify({type: 'danger', message: '网络异常'})
         return Promise.reject(error)
    } else {
        const {config, response: {status}} = error
        const originalRequest = config
        if (status === 499) {
            if (!isRefreshing) {
                isRefreshing = true
                axios.get('auth/refresh')
                    .then(res => {
                        isRefreshing = false
                        if (res.data.code === 200) {
                            const accessToken = res.data.data.access_token
                            sessionStorage.setItem('accessToken', res.data.data.access_token)
                            sessionStorage.setItem('refreshToken', res.data.data.refresh_token)
                            onRefreshed(accessToken)
                        } else if (res.data.code === 302) {
                            window.location.href = res.data.data.redirect_url
                        }
                    })
            }

            return new Promise((resolve, reject) => {
                subscribeTokenRefresh(token => {
                    originalRequest.headers.Authorization = `Bearer ${token}`
                    resolve(axios(originalRequest))
                })
            })
        } else if (error.response.status === 401) {
            sessionStorage.clear()
            const url = new URL(window.location.href)
            const params = new URLSearchParams(url.search)
            if (params.has('code')) {
                params.delete('code')
                window.location.href = window.location.pathname + '?' + params.toString()
            } else {
                window.location.reload()
            }
        } else if (error.response.status === 500) {
            router.isForward = true
            router.push('/error?data=系统错误')
        } else {
            return Promise.reject(error)
        }
    }


})


/**
 * @description axios请求拦截器
 */

instance.interceptors.request.use(function (config) {
    const accessToken = sessionStorage.getItem('accessToken')
    const refreshToken = sessionStorage.getItem('refreshToken')
    const url = config.url || ''

    // console.log('before request config', config, url.indexOf('auth/refresh'))
    if (accessToken && url.indexOf('auth/refresh') === -1) {
        config.headers.authorization = `Bearer ${accessToken}`
    } else {
        config.headers.authorization = `Bearer ${refreshToken}`
    }
    // console.log(config)
    return config
}, function (error) {
    // Do something with request error
    return Promise.reject(error)
})


function onRefreshed(token) {
    refreshSubscribers.map(cb => cb(token))
}

function subscribeTokenRefresh(cb) {
    refreshSubscribers.push(cb)
}

export default instance;