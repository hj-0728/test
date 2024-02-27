export interface Error {
    token: string
    createdAt: string
    message: string
    err_type: string
}

export interface MessageCarrier<T> {
  code: number
  createdAt: string
  data: T
  error: null | Error
  message: string[]
}

export interface PageFilterParams {
    draw: number
    searchText: string
    pageSize: number
    pageIndex: number
}

export interface PageFilterResult<T> {
    searchText: string | null
    totalCount: number
    filterCount: number
    pageIndex: number
    pageSize: number
    draw: number
    data: T[]
}
