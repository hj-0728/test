export interface BasicPageParams {
  page: number;
  pageSize: number;
}

export interface BasicPageQueryParamsModel {
  searchText: string;
  pageSize: number;
  pageIndex: number;
  draw: number;
}

export interface Error {
  token: string;
  createdAt: Date;
  message: string;
  errType: string;
  stackList: any[];
}

export interface BasicPageQueryResponseModel {
  searchText: string;
  pageSize: number;
  pageIndex: number;
  draw: number;
}

export interface BasicResponseModel<T = any> {
  code: number;
  createdAt: Date;
  messages: string[];
  error: Error;
  data: T;
}

export interface BasicPageQueryResult<T = any> {
  data: T;
  draw: number;
  filterCount: number;
  pageIndex: number;
  pageSize: number;
  totalCount: number;
  searchText: string;
}
