export interface TableData {
    data: any[];
    totalCount: number;
    pageIndex: number;
    pageSize: number;
}

export interface Column {
    title: string;
    dataIndex: string;
}
