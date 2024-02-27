import { Box, Button, Group, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconCheck } from '@tabler/icons-react';
import React, { useEffect } from 'react';
import BasicModal from '@/components/BasicModal';
import { apiGetMenuInfo, apiSaveMenu } from '@/api/MenuApi';
import { Menu } from '@/model/Menu.model';
import openConfirmModal from '@/components/BasicConfirmModal';
import { showErrorNotification, showSuccessNotification } from '@/components/BasicNotifications';

interface TreeEditFormProps {
  open: boolean; // Modal是否打开
  onClose: () => void; // 关闭Modal
  menuId?: string; // 菜单ID
  parentId?: string; // 父菜单ID
}

const TreeEditForm = ({ open, onClose, menuId, parentId }: TreeEditFormProps) => {
  const form = useForm<Menu>({
    initialValues: {
      parentId: null,
      version: 1,
      name: '',
      path: '',
      icon: '',
    },

    validate: {
      name: (value) => (value.trim() ? null : '名称不能为空'),
      path: (value) => (value.trim() ? null : '路径不能为空'),
      icon: (value) => (value.trim() ? null : '图标不能为空'),
    },

  });

  const onLoadMenuInfo = async () => {
    if (menuId) {
      const res = await apiGetMenuInfo(menuId);
      if (res.code === 200) {
        form.setValues({ ...res.data });
      }
    }
  };

  useEffect(() => {
    onLoadMenuInfo();
  }, [menuId]);

  const onCloseModal = () => {
    form.reset();
    onClose();
  };

  const handleAccept = async () => {
    const menu = form.values;
    if (parentId) {
      menu.parentId = parentId;
    }
    const res = await apiSaveMenu(menu);
    if (res.code === 200) {
      showSuccessNotification('保存成功');
      onCloseModal();
    } else {
      showErrorNotification(res.error!.message);
    }
  };

  const onSubmitToBackend = () => {
    openConfirmModal({
      message: '确定要提交吗？',
      onConfirm: () => handleAccept(),
    });
  };

  const formBody = (
    <Box maw={500} mx="auto">
      <form onSubmit={form.onSubmit(() => onSubmitToBackend())}>
        <TextInput
          withAsterisk
          label="名称"
          placeholder="请输入菜单名称"
          {...form.getInputProps('name')}
        />

        <TextInput
          withAsterisk
          label="路径"
          placeholder="请输入路径"
          {...form.getInputProps('path')}
        />

        <TextInput
          withAsterisk
          label="图标"
          placeholder="请输入图标"
          {...form.getInputProps('icon')}
        />

        <Group justify="right" mt="md">
          <Button leftSection={<IconCheck />} type="submit">提交</Button>
        </Group>
      </form>
    </Box>
  );

  return (
    <>
      <BasicModal isOpen={open} onClose={onCloseModal} title={menuId ? '编辑菜单' : '添加菜单'}>
        {formBody}
      </BasicModal>
    </>
  );
};

export default TreeEditForm;
