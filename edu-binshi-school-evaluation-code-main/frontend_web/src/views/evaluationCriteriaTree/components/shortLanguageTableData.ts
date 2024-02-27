import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '评价语',
      dataIndex: 'content',
      ellipsis: false,
    },
    {
      title: '是否启用',
      dataIndex: 'isActive',
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
