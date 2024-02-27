import { USER_INFO_KEY } from '/@/enums/cacheEnum';
import { getAuthCache } from '/@/utils/auth';
import { UserInfo } from '/#/store';
import { router } from '/@/router';
import { PageEnum } from '/@/enums/pageEnum';
import {ref} from "vue";

export function getUserInfo() {
  return (getAuthCache(USER_INFO_KEY) as UserInfo) || undefined;
}

export const getMsgDom = (msgList: Array<string>) => {
  let dom = ``;
  for (const msg of msgList) {
    dom += `<div>${msg}</div>`;
  }
  return dom;
};

// 新增
export function getCurrentOrganization() {
  const currentUserInfo = (getAuthCache(USER_INFO_KEY) as UserInfo) || undefined;
  if (currentUserInfo) {
    return currentUserInfo.currentOrganization;
  } else {
    router.push(PageEnum.BASE_LOGIN);
  }
}

export const benchmarkStrategySourceCategory = {
  INPUT: {
    color: '#49beff',
    backgroundColor: '#e8f7ff',
    name:'输入类评价分类'
  },
  CALC: {
    color: '#6591d9',
    backgroundColor: '#e8ebff',
    name:'计算类评价分类'
  },
};

export const colorData = {
  PUBLISHED: 'blue',
  ABOLISHED: 'red',
  ARCHIVED: 'green',
  DRAFT: 'purple',
  IN_PROGRESS: 'cyan',
};
