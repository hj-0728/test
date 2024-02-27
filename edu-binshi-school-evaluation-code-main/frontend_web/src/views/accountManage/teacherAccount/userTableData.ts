import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '用户名',
      dataIndex: 'name',
      width: '20%',
    },
    {
      title: '关联人员名称',
      dataIndex: 'peopleName',
      width: '20%',
    },
    {
      title: '角色',
      dataIndex: 'roleNameList',
      width: '20%',
    },
    {
      title: '状态',
      dataIndex: 'isActivated',
      width: '10%',
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: '30%',
    },
  ];
}

export function getBasicPeopleColumns(): BasicColumn[] {
  return [
    {
      title: '姓名',
      dataIndex: 'name',
      width: '20%',
    },
    {
      title: '部门',
      dataIndex: 'dept',
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: 200,
    },
  ];
}
