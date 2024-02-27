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
      ellipsis: false,
    },
    {
      title: '账号',
      dataIndex: 'userName',
    },
    {
      title: '是否初始密码',
      dataIndex: 'isInitPassword',
      width: 130,
    },
    {
      title: '状态',
      dataIndex: 'isActivated',
      width: 120,
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
