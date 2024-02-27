/**
 * @description: Request list interface parameters
 */

export interface MessagePageQueryResponseModel {
  searchText: string;
  pageSize: number;
  pageIndex: number;
  draw: number;
  isRead?: string;
  sortName?: string;
  orderBy?: string;
  category?: object;
}
