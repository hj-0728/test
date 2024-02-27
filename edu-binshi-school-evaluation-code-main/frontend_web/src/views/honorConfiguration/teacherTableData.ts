import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '荣誉勋章',
      dataIndex: 'imgUrl',
      width: 120,
    },
    {
      title: '荣誉名称',
      dataIndex: 'peopleName',
      ellipsis: false,
    },
    {
      title: '适用年级',
      dataIndex: 'deptName',
    },
    {
      title: '分值',
      dataIndex: 'capacityName',
      ellipsis: false,
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
