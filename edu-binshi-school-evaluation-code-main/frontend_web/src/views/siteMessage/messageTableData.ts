import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(messageCategoryFilters): BasicColumn[] {
  return [
    {
      title: '消息类型',
      dataIndex: 'initResourceCategoryName',
      key: 'category',
      width: '15%',
      filters: messageCategoryFilters,
      filterMultiple: true,
    },
    {
      title: '标题',
      dataIndex: 'title',
      width: '15%',
    },
    {
      title: '内容',
      dataIndex: 'content',
      width: '35%',
    },
    {
      title: '发送时间',
      dataIndex: 'createdAt',
      sorter: true,
      width: '150px',
    },
    {
      title: '是否阅读',
      dataIndex: 'readAt',
      filterMultiple: false,
      filters: [
        {
          text: '已读',
          value: 'read',
        },
        {
          text: '未读',
          value: 'unread',
        },
      ],
      width: '100px',
    },
    {
      title: '操作',
      dataIndex: 'operation',
      width: '240px',
      fixed: 'right',
    },
  ];
}
