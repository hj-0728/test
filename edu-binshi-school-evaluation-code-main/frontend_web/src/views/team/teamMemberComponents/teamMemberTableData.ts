import { BasicColumn } from '/@/components/Table/src/types/table';

export function getTeamMemberColumns(): BasicColumn[] {
  return [
    {
      title: '姓名',
      dataIndex: 'peopleName',
    },
    {
      title: '职责',
      dataIndex: 'capacityName',
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
}
