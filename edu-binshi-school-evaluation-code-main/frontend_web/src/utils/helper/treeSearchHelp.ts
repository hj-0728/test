//获取节点中含有value的所有key
import { cloneDeep } from 'lodash';

export const getkeyList = (
  value,
  tree,
  keyList,
  searchKey = 'name',
  idKey = 'id',
  childKey = 'children',
) => {
  for (let i = 0; i < tree.length; i++) {
    const node = tree[i];
    if (node[searchKey].indexOf(value) > -1) {
      keyList.push(node[idKey]);
    }
    if (node[childKey]) {
      getkeyList(value, node[childKey], keyList, searchKey, idKey, childKey);
    }
  }
  return keyList;
};

//获取节点中所有key
export const getAllKeyList = (tree, keyList, idKey = 'id', childKey = 'children') => {
  for (let i = 0; i < tree.length; i++) {
    const node = tree[i];
    keyList.push(node[idKey]);
    if (node[childKey]) {
      getAllKeyList(node[childKey], keyList, idKey, childKey);
    }
  }
  return keyList;
};

//获取该节点的父节点
export const getParentKey = (key, tree, idKey = 'id', childKey = 'children') => {
  let parentKey: any;
  let temp;
  for (let i = 0; i < tree.length; i++) {
    const node = tree[i];
    if (node[childKey]) {
      if (node[childKey].some((item) => item[idKey] === key)) {
        parentKey = node[idKey];
      } else if ((temp = getParentKey(key, node[childKey], idKey, childKey))) {
        parentKey = temp;
      }
    }
  }
  return parentKey;
};

//获取该节点的所有父节点
export const getAllParentKey = (
  key,
  tree,
  backupsExpandedKeys: any[] = [],
  idKey = 'id',
  childKey = 'children',
) => {
  let parentKey;
  if (key) {
    parentKey = getParentKey(key, tree, idKey, childKey);
    if (!backupsExpandedKeys.some((item) => item === key)) {
      backupsExpandedKeys.push(key);
    }
    if (parentKey) {
      if (!backupsExpandedKeys.some((item) => item === parentKey)) {
        backupsExpandedKeys.push(parentKey);
      }
      getAllParentKey(parentKey, tree, backupsExpandedKeys, idKey, childKey);
    }
  }
  return backupsExpandedKeys;
};

export const getNode = (key, tree, idKey = 'id', childKey = 'children') => {
  for (const node of tree) {
    if (node[idKey] === key) {
      return node;
    } else if (node.children) {
      const result = getNode(key, node[childKey], idKey, childKey);
      if (result) return result;
    }
  }
  return null;
};

export const getAllChildrenKeys = (
  key,
  tree: any[],
  idKey = 'id',
  childKey = 'children',
): any[] => {
  const childrenKeys: any[] = [];

  const node = getNode(key, tree);
  if (node) {
    if (node[childKey]) {
      for (const item of node[childKey]) {
        childrenKeys.push(item[idKey]);
        childrenKeys.push(...getAllChildrenKeys(item[idKey], tree, idKey, childKey));
      }
    } else {
      childrenKeys.push(node[idKey]);
    }
  }

  return childrenKeys;
};

export const filterTreeData = (treeDataInfo, canShow, idKey = 'id', childKey = 'children') => {
  const dataList: string[] = [];
  treeDataInfo.forEach((val) => {
    if (canShow.includes(val[idKey])) {
      if (val[childKey]) {
        val[childKey] = filterTreeData(val[childKey], canShow);
      }
      dataList.push(val);
    }
  });
  return dataList;
};

export const searchTree = (
  searchValue,
  originalTreeData,
  searchKey = 'name',
  idKey = 'id',
  childKey = 'children',
) => {
  let treeData: object[];
  let expandedKeys: string[];
  let unexpandedKeys: string[];
  if (searchValue.trim() === '') {
    treeData = cloneDeep(originalTreeData);
    expandedKeys = getAllKeyList(originalTreeData, [], idKey, childKey);
  } else {
    expandedKeys = [];
    unexpandedKeys = [];
    const backupsExpandedKeys: string[] = [];
    const canShow: string[] = [];
    const candidateKeysList = getkeyList(
      searchValue,
      originalTreeData,
      [],
      searchKey,
      idKey,
      childKey,
    );
    if (candidateKeysList.length > 0) {
      canShow.push(...candidateKeysList);
    }
    candidateKeysList.map((item) => {
      const key = getParentKey(item, originalTreeData, idKey, childKey);
      const childrenKeys = getAllChildrenKeys(item, originalTreeData, idKey, childKey);
      unexpandedKeys.push(...childrenKeys);
      if (key && !backupsExpandedKeys.some((item) => item === key)) backupsExpandedKeys.push(key);
    });
    const length = backupsExpandedKeys.length;
    for (let i = 0; i < length; i++) {
      expandedKeys.push(
        ...getAllParentKey(
          backupsExpandedKeys[i],
          originalTreeData,
          backupsExpandedKeys,
          idKey,
          childKey,
        ),
      );
    }
    if (expandedKeys.length > 0) {
      canShow.push(...expandedKeys, ...unexpandedKeys);
    }
    if (canShow.length === 0) {
      treeData = [];
      expandedKeys = [];
    } else {
      const treeDataInfo = cloneDeep(originalTreeData);
      treeData = filterTreeData(treeDataInfo, canShow, idKey, childKey);
      expandedKeys = expandedKeys.slice();
    }
  }
  expandedKeys = Array.from(new Set(expandedKeys));
  return { treeData, expandedKeys };
};
