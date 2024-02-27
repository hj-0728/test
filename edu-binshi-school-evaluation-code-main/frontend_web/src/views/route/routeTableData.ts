import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '路径',
      dataIndex: 'path',
      fixed: 'left',
    },
    {
      title: '编码',
      dataIndex: 'entryCode',
      width: 100,
    },
    {
      title: '类型',
      dataIndex: 'categoryName',
      width: 100,
      filters: [
        {
          text: '前端',
          value: 'FRONTEND',
        },
        {
          text: '后端',
          value: 'BACKEND',
        },
      ],
      filterMultiple: false,
    },
    {
      title: '身份验证',
      dataIndex: 'accessStrategyName',
      width: 200,
      filters: [
        {
          text: '忽略',
          value: 'IGNORE',
        },
        {
          text: '身份验证',
          value: 'AUTHORIZED',
        },
        {
          text: '受控',
          value: 'CONTROLLED',
        },
      ],
      filterMultiple: false,
    },
    {
      title: '角色名称',
      dataIndex: 'roleNameList',
      width: 200,
    },
    {
      title: '功能权限',
      dataIndex: 'abilityPermissionList',
      width: 120,
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: 150,
    },
  ];
}
