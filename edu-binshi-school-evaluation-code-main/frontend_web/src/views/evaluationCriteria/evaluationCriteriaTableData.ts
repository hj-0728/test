import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '名称',
      dataIndex: 'name',
      ellipsis: false,
      width: '25%',
    },
    // {
    //   title: '评价对象',
    //   dataIndex: 'evaluationObjectCategoryDisplay',
    //   // filters: [],
    //   width: '10%',
    // },
    {
      title: '描述',
      dataIndex: 'comments',
      width: '20%',
    },
    {
      title: '状态',
      dataIndex: 'statusDisplay',
      filters: [],
      width: '10%',
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: '40%',
    },
  ];
}
