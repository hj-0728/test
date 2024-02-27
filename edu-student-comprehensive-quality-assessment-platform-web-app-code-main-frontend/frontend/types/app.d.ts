declare module 'MyApp' {
   export type Role = {
    id: string;
    name: string;
    code: string;
  };
  export type UserInfo = {
    name: string;
    roleList: Role[];
    currentRole: Role;
  };
}
