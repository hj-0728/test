import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '名称',
      dataIndex: 'name',
      fixed: 'left',
    },
    {
      title: '编码',
      dataIndex: 'code',
    },
    {
      title: '状态',
      dataIndex: 'isActivated',
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
