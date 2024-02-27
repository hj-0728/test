import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '名称',
      dataIndex: 'name',
      ellipsis: false,
    },
    {
      title: '状态',
      dataIndex: 'isActivated',
      filterMultiple: false,
      filters: [
        {
          text: '启用',
          value: 'isActivated',
        },
        {
          text: '禁用',
          value: 'isNotActivated',
        },
      ],
      width: '15%',
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
