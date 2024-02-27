import { BasicColumn } from '/@/components/Table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '评价标准计划',
      dataIndex: 'planName',
      ellipsis: false,
      width: '25%',
    },
    {
      title: '评价标准计划时间',
      dataIndex: 'executedStartAt',
      width: 200,
    },
    {
      title: '评价标准',
      dataIndex: 'evaluationCriteriaName',
      ellipsis: false,
      width: '25%',
    },
    // {
    //   title: '评价对象类型',
    //   dataIndex: 'evaluationObjectCategoryName',
    //   filters: [
    //     { text: '学生', value: 'STUDENT' },
    //     { text: '家长', value: 'PARENTS' },
    //     { text: '老师', value: 'TEACHER' },
    //   ],
    //   width: 150,
    // },
    {
      title: '状态',
      dataIndex: 'planStatusName',
      filters: [
        { text: '进行中', value: 'IN_PROGRESS' },
        { text: '已归档', value: 'ARCHIVED' },
        { text: '已废除', value: 'ABOLISHED' },
      ],
      width: 100,
    },
    {
      title: '已填写',
      dataIndex: 'fillCount',
      width: 80,
    },
    {
      title: '未填写',
      dataIndex: 'notFillCount',
      width: 80,
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: '22%',
    },
  ];
}
