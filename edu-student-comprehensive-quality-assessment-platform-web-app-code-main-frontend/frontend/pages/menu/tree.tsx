import { NextPage } from 'next';
import { Button, Grid, Input, LoadingOverlay, ScrollArea } from '@mantine/core';
import React, { ChangeEvent, KeyboardEvent, useEffect, useRef, useState } from 'react';
import { ContextMenu } from 'primereact/contextmenu';
import { IconCheck, IconRefresh, IconSearch } from '@tabler/icons-react';
import AdminLayout from '@/layouts/adminLayout';
import { apiDeleteMenu, apiGetMenuTree, apiUpdateSort } from '@/api/MenuApi';
import BasicTree from '@/components/BasicTree';
import { showErrorNotification, showSuccessNotification } from '@/components/BasicNotifications';
import openConfirmModal from '@/components/BasicConfirmModal';
import { MenuTree, PrimereactMenuTree, UpdateMenuSort } from '@/model/Menu.model';
import PageWrapperCard from '@/components/Page/WrapperCard';
import EditForm from './_components/EditForm';

function MenuTreeBody() {
  const [nodes, setNodes] = useState<PrimereactMenuTree[]>([]);
  const [expandedKeys, setExpandedKeys] = useState({});
  const [selectedNodeKey, setSelectedNodeKey] = useState<string>('');
  const [editParams, setEditParams] = useState({});
  const [open, setOpen] = useState(false);
  const [visible, setVisible] = useState(true);
  const [searchText, setSearchText] = useState('');

  const childCm = useRef(null);
  const rootCm = useRef(null);

  const expandNode = (node: PrimereactMenuTree, _expandedKeys: {}) => {
    if (node.children && node.children.length) {
      _expandedKeys[node.key] = true;
      for (const child of node.children) {
        expandNode(child, _expandedKeys);
      }
    }
  };

  const expandAll = (data: PrimereactMenuTree[]) => {
    const _expandedKeys = {};
    for (const node of data) {
      expandNode(node, _expandedKeys);
    }
    setExpandedKeys(_expandedKeys);
  };

  const convertNavbarMenuToMenu = (navbarMenu: MenuTree[]): PrimereactMenuTree[] => navbarMenu.map(menuItem => ({
    key: menuItem.id,
    version: menuItem.version,
    parentId: menuItem.parentId,
    label: menuItem.name,
    children: convertNavbarMenuToMenu(menuItem.childList),
  }));

  const onLoadMenuTree = async () => {
    const res = await apiGetMenuTree(searchText);
    if (res.code === 200) {
      const primeMenu: PrimereactMenuTree[] = convertNavbarMenuToMenu(res.data);
      const data = [
        { key: '0', label: '菜单树', type: 'root', children: primeMenu },
      ];
      setNodes(data);
      expandAll(data);
    } else {
      showErrorNotification(res.error!.message);
    }
    setVisible(false);
  };

  const reloadData = () => {
    setVisible(true);
    onLoadMenuTree();
  };
  const handleDeleteMenu = async () => {
    const res = await apiDeleteMenu(selectedNodeKey);
    if (res.code === 200) {
      showSuccessNotification('删除成功');
      reloadData();
    } else {
      showErrorNotification(res.error!.message);
    }
  };

  const getNewMenu = (data: PrimereactMenuTree[], newMenu: UpdateMenuSort[], parentId: null | string) => {
    data.map((item, index) => {
      const _item: UpdateMenuSort = { id: item.key, version: item.version, seq: index + 1, parentId };
      newMenu.push(_item);
      if (item.children && item.children.length) {
        getNewMenu(item.children, newMenu, item.key);
      }
    });
  };

  const handleAcceptUpdateSort = async () => {
    const _newMenu: UpdateMenuSort[] = [];
    getNewMenu(nodes[0].children || [], _newMenu, null);
    const res = await apiUpdateSort(_newMenu);
    if (res.code === 200) {
      showSuccessNotification('排序更新成功');
      reloadData();
    } else {
      showErrorNotification(res.error!.message);
    }
  };

  const rootRightMenu = [
    {
      label: '添加子节点',
      icon: 'pi pi-plus',
      command: () => {
        setOpen(true);
      },
    },
  ];
  const childRightMenu = [
    {
      label: '添加子节点',
      icon: 'pi pi-plus',
      command: () => {
        setOpen(true);
        setEditParams({ parentId: selectedNodeKey });
      },
    },
    {
      label: '编辑',
      icon: 'pi pi-file-edit',
      command: () => {
        setOpen(true);
        setEditParams({ menuId: selectedNodeKey });
      },
    },
    {
      label: '删除',
      icon: 'pi pi-trash',
      command: () => {
        openConfirmModal({
          message: '确定要删除吗？',
          confirmLabel: '删除',
          onConfirm: () => handleDeleteMenu(),
        });
      },
    },
  ];

  useEffect(() => {
    onLoadMenuTree();
  }, []);

  const onDragNode = (value: PrimereactMenuTree[]) => {
    setNodes(value);
  };

  const onCloseEditForm = () => {
    setOpen(false);
    reloadData();
  };

  const handleUpdateSort = () => {
    openConfirmModal({
      message: '确定要保存排序吗？',
      onConfirm: () => handleAcceptUpdateSort(),
    });
  };

  return (
    <>
      <LoadingOverlay visible={visible} zIndex={1000} />

      <Grid>
        <Grid.Col span={8}>
          <Input
            placeholder="搜索"
            value={searchText}
            rightSectionPointerEvents="all"
            rightSection={
              <Button leftSection={<IconSearch size={16} />} onClick={reloadData} />
            }
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              setSearchText(e.target.value);
            }}
            onKeyDown={(event: KeyboardEvent<HTMLInputElement>) => {
              if (event.key === 'Enter') {
                reloadData();
              }
            }}
          />
        </Grid.Col>
        <Grid.Col span={4}>
          <Button leftSection={<IconRefresh />} onClick={reloadData} color="violet">刷新</Button>
          <Button
            leftSection={<IconCheck />}
            onClick={handleUpdateSort}
            color="cyan"
            style={{ marginLeft: '5px' }}
          >
            保存排序
          </Button>
        </Grid.Col>
      </Grid>
      <ScrollArea h="76vh">
        <EditForm {...editParams} open={open} onClose={onCloseEditForm} />
        <ContextMenu model={childRightMenu} ref={childCm} />
        <ContextMenu model={rootRightMenu} ref={rootCm} />
        <BasicTree
          value={nodes}
          expandedKeys={expandedKeys}
          onToggle={(e) => setExpandedKeys(e.value)}
          dragdropScope="menu"
          onDragDrop={(e) => onDragNode(e.value)}
          onContextMenuSelectionChange={(e) => setSelectedNodeKey(e.value)}
          onContextMenu={(e) => {
            const nodeType = e.node.type;
            if (nodeType === 'root') {
              childCm.current.hide();
              rootCm.current.show(e.originalEvent);
            } else {
              rootCm.current.hide();
              childCm.current.show(e.originalEvent);
            }
          }}
        />
      </ScrollArea>
    </>
  );
}

const MenuTreePage: NextPage = () => (
  <>
    <AdminLayout>
      <PageWrapperCard>
        <MenuTreeBody />
      </PageWrapperCard>
    </AdminLayout>
  </>
);

export default MenuTreePage;
