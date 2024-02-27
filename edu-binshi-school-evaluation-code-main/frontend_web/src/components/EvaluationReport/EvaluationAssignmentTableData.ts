import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '姓名',
      dataIndex: 'peopleName',
      ellipsis: false,
    },
    {
      title: '班级',
      dataIndex: 'deptName',
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
