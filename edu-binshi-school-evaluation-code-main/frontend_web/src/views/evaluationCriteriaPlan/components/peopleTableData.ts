import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '姓名',
      dataIndex: 'studentName',
      ellipsis: false,
    },
    {
      title: '班级',
      dataIndex: 'dept',
    },
  ];
}
