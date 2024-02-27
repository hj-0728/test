import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '姓名',
      dataIndex: 'peopleName',
      ellipsis: false,
    },
    {
      title: '职责',
      dataIndex: 'capacityName',
    },
    {
      title: '部门',
      dataIndex: 'deptName',
    },
  ];
}
