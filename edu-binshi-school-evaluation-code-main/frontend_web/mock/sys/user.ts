import { MockMethod } from 'vite-plugin-mock';
import { resultError, resultSuccess, getRequestToken, requestParams } from '../_util';

export function createFakeUserList() {
  return [
    {
      userId: '1',
      name: 'admin',
      realName: 'Vben Admin',
      avatar: 'https://q1.qlogo.cn/g?b=qq&nk=190848757&s=640',
      desc: 'manager',
      password: '123456',
      token: 'fakeToken1',
      homePath: '/basic-table',
      currentRole: {
        id: '1',
        name: '管理员',
        code: 'EXPERT',
      },
      roleList: [
        {
          id: '1',
          name: '管理员',
          code: 'EXPERT',
        },
      ],
      roles: [
        {
          roleName: 'Super Admin',
          value: 'super',
        },
      ],
    },
  ];
}

const fakeCodeList: any = {
  '1': ['1000', '3000', '5000'],

  '2': ['2000', '4000', '6000'],
};
export default [
  // mock user login
  {
    url: '/api/web/user/mock-login',
    timeout: 200,
    method: 'post',
    response: ({ body }) => {
      const { name, password } = body;
      const checkUser = createFakeUserList().find(
        (item) => item.name === name && password === item.password,
      );
      if (!checkUser) {
        return resultError('账号或密码错误！');
      }
      const { token } = checkUser;
      return resultSuccess(token);
    },
  },
  {
    url: '/api/web/user/mock-get-user-info',
    method: 'get',
    response: (request: requestParams) => {
      const token = getRequestToken(request);
      if (!token) return resultError('Invalid token');
      const checkUser = createFakeUserList().find((item) => item.token === token);
      if (!checkUser) {
        return resultError('The corresponding user information was not obtained!');
      }
      return resultSuccess(checkUser);
    },
  },
  {
    url: '/api/web/mock-get-perm-code',
    timeout: 200,
    method: 'get',
    response: (request: requestParams) => {
      const token = getRequestToken(request) ? getRequestToken(request) : 'fakeToken1';
      if (!token) return resultError('Invalid token');
      const checkUser = createFakeUserList().find((item) => item.token === token);
      if (!checkUser) {
        return resultError('Invalid token!');
      }
      const codeList = fakeCodeList[checkUser.userId];

      return resultSuccess(codeList);
    },
  },
  {
    url: '/api/web/user/mock-logout',
    timeout: 200,
    method: 'post',
    response: (request: requestParams) => {
      const token = getRequestToken(request);
      if (!token) return resultError('Invalid token');
      const checkUser = createFakeUserList().find((item) => item.token === token);
      if (!checkUser) {
        return resultError('Invalid token!');
      }
      return resultSuccess(undefined, { message: 'Token has been destroyed' });
    },
  },
] as MockMethod[];
