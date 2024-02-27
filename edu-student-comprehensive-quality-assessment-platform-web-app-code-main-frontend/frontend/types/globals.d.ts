declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NEXT_PUBLIC_API_URL: string;
      NEXT_PUBLIC_APP_TITLE: string;
      NEXT_PUBLIC_APP_SUB_TITLE: string;
    }
  }
}

// 在这种情况下，"export {}" 是必需的，以确保 TypeScript 将该文件识别为模块
export {};
