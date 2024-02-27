import ky from 'ky';
import Router from 'next/router';
import useAppState from './store/app';

// 创建一个ky实例
const http = ky.create({
  prefixUrl: process.env.NEXT_PUBLIC_API_URL,
  hooks: {
    beforeRequest: [
      async (request: any) => {
        const token = useAppState.getState().accessToken;
        if (token) {
          request.headers.set('Authorization', `Bearer ${token}`);
        }
      },
    ],
    afterResponse: [
      async (request, options, response) => {
        if (response.status === 400) {
          // const data: any = await response.json();
        }

        if (response.status === 401) {
          await Router.push('/auth/sign-in');
          return new Response(JSON.stringify({}), { status: 200 });
        }
        return response;
      },
    ],
  },
  timeout: 600000,
});

export default http;
