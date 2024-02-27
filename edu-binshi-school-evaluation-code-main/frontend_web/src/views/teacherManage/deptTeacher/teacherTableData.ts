import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '教师姓名',
      dataIndex: 'peopleName',
      ellipsis: false,
    },
    {
      title: '班级',
      dataIndex: 'deptName',
    },
    {
      title: '职责',
      dataIndex: 'capacityName',
      filters: [],
      ellipsis: false,
    },
    {
      title: '任教科目',
      dataIndex: 'subjectName',
      filters: [],
      ellipsis: false,
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
