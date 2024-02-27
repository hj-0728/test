import { BasicColumn } from '/@/components/Table';
import { evaluationCriteriaPlanStatusEnum } from '/@/enums/bizEnum';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: '评价计划',
      dataIndex: 'name',
      ellipsis: false,
    },
    {
      title: '评价标准',
      dataIndex: 'evaluationCriteriaName',
      ellipsis: false,
    },
    {
      title: '评价标准计划时间',
      dataIndex: 'executedAt',
      width: 200,
    },
    {
      title: '状态',
      dataIndex: 'statusName',
      filters: [
        { text: '草稿', value: evaluationCriteriaPlanStatusEnum.DRAFT },
        { text: '已发布', value: evaluationCriteriaPlanStatusEnum.PUBLISHED },
        { text: '已废除', value: evaluationCriteriaPlanStatusEnum.ABOLISHED },
        { text: '已归档', value: evaluationCriteriaPlanStatusEnum.ARCHIVED },
      ],
      width: '8%',
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: '45%',
    },
  ];
}
