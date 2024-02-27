import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { MessagePageQueryResponseModel } from '/@/api/siteMessage/siteMessageModel';
import { BasicResponseModel } from '/@/api/model/baseModel';

const PREFIX = '/site-message';

enum Api {
  MESSAGE_LIST = '/list',
  MESSAGE_INFO = '/info/',
  EXIST_UNREAD_MESSAGE = '/unread-exist',
  READ_SITE_MESSAGE = '/read/',
}

/**
 * @description: Get sample options value
 */

export const apiSiteMessageList = (
  params: MessagePageQueryResponseModel,
  mode: ErrorMessageMode = 'modal',
) => {
  return defHttp.post(
    {
      url: PREFIX + Api.MESSAGE_LIST,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
};

export const apiGetSiteMessageInfo = (messageId: string, mode: ErrorMessageMode = 'modal') => {
  return defHttp.get(
    {
      url: PREFIX + Api.MESSAGE_INFO + messageId,
    },
    {
      errorMessageMode: mode,
    },
  );
};

/**
 * @description: 判断是否存在未读消息
 */

export const apiJudgeUnreadMessageExist = () =>
  defHttp.get<BasicResponseModel>(
    {
      url: PREFIX + Api.EXIST_UNREAD_MESSAGE,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );

export const apiReadSiteMessage = (messageId) => {
  return defHttp.post<any>({
    url: PREFIX + Api.READ_SITE_MESSAGE + messageId,
  });
};
