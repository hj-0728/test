import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '名称',
      dataIndex: 'name',
      ellipsis: false,
    },
    {
      title: '评价目标',
      dataIndex: 'teamGoal',
      ellipsis: false,
    },
    {
      title: '评价参与人员',
      dataIndex: 'memberList',
      ellipsis: false,
    },
    {
      title: '创建人',
      dataIndex: 'createPeopleName',
      width: 100,
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: 350,
    },
  ];
}
