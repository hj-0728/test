import { LoginParams, Token } from '@/model/Auth.model';
import { UserInfo } from 'MyApp';
import { NavbarMenu } from '@/model/Menu.model';
import defHttp from './BasicApi';

enum Api {
    Login = 'auth/login',
    GET_USER_SIDEBAR_MENU = 'auth/get-user-sidebar-menu',
    GET_CURRENT_USER_INFO = 'auth/get-current-user-info',
    GET_LOGIN_VALIDATE_IMAGE = 'auth/get-login-validate-image',
}

export const apiLogin = (params: LoginParams) => defHttp.post<Token>(Api.Login, { ...params });
export const apiGetUserSidebarMenu = () => defHttp.get<NavbarMenu[]>(Api.GET_USER_SIDEBAR_MENU);
export const apiGetCurrentUserInfo = () => defHttp.get<UserInfo>(Api.GET_CURRENT_USER_INFO);
export const apiGetLoginValidateImage = () => defHttp.get<string>(Api.GET_LOGIN_VALIDATE_IMAGE);
