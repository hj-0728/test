const demoList = (() => {
  const result: any[] = [];

  for (let index = 1; index < 61; index++) {
    result.push({
      id: index,
      name: 'Template' + index,
      is_activated: true,
    });
  }
  return result;
})();
export const treeData = (() => {
  const tree = [
    {
      title: '一级节点1',
      key: 'L1-1',
      children: [
        { title: '二级节点1', key: 'L2-1' },
        {
          title: '二级节点2',
          key: 'L2-2',
        },
      ],
    },
    {
      title: '一级节点2',
      key: 'L1-2',
      children: [
        { title: '二级节点3', key: 'L2-3' },
        { title: '二级节点4', key: 'L2-4' },
      ],
    },
    {
      title: '一级节点3',
      key: 'L1-3',
      children: [
        { title: '二级节点5', key: 'L2-5' },
        { title: '二级节点6', key: 'L2-6' },
      ],
    },
  ];
  return tree;
})();
export default [
  {
    url: '/api/web/template/list',
    timeout: 200,
    method: 'post',
    response: ({ body }) => {
      console.log(body);
      return {
        created_at: '2022-02-24T17:41:05.098605+08:00',
        code: 200,
        messages: [],
        data: demoList,
      };
    },
  },
  {
    url: '/api/web/template/tree',
    timeout: 200,
    method: 'post',
    response: ({ body }) => {
      console.log(body);
      return {
        created_at: '2022-02-24T17:41:05.098605+08:00',
        code: 200,
        messages: [],
        data: treeData,
      };
    },
  },
];
