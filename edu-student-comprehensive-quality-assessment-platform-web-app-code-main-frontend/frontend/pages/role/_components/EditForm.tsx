import { Box, Button, Group, Input, Switch, Textarea, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconCheck } from '@tabler/icons-react';
import React, { useEffect, useState } from 'react';
import BasicModal from '@/components/BasicModal';
import { Role } from '@/model/Role.model';
import { apiGetRoleInfo, apiSaveRole } from '@/api/RoleApi';
import { showErrorNotification, showSuccessNotification } from '@/components/BasicNotifications';
import openConfirmModal from '@/components/BasicConfirmModal';

interface RoleEditFormProps {
    open: boolean; // Modal是否打开
    onClose: () => void; // 关闭Modal
    roleId?: any;
}

const EditForm = ({ open, roleId, onClose }: RoleEditFormProps) => {
    const [checked, setChecked] = useState(true);
    const form = useForm<Role>({
        initialValues: {
            id: null,
            version: 1,
            name: '',
            code: '',
            comments: '',
            isActivated: true,
        },

        validate: {
            name: (value) => (value.trim() ? null : '名称不能为空'),
            code: (value) => (value.trim() ? null : '编码不能为空'),
        },

    });

    const onLoadRoleInfo = () => {
        apiGetRoleInfo(roleId).then((res) => {
            if (res.code === 200) {
                const { id, version, name, code, comments, isActivated } = res.data;
                form.setValues({ id, version, name, code, comments, isActivated });
                setChecked(isActivated);
            } else {
                showErrorNotification(res.error!.message);
            }
        });
    };

    useEffect(() => {
        if (open && roleId) {
            onLoadRoleInfo();
        }
    }, [open]);

    const onCloseModal = () => {
        form.reset();
        onClose();
    };

    const handleAccept = async () => {
        const role = form.values;
        role.isActivated = checked;
        const res = await apiSaveRole(role);
        if (res.code === 200) {
            showSuccessNotification('保存成功');
            onCloseModal();
        } else {
            showErrorNotification(res.error!.message);
        }
    };

    const onSaveRole = () => {
        openConfirmModal({
            message: '确定要提交吗？',
            onConfirm: () => handleAccept(),
        });
    };

    const formBody = (
        <Box maw={500} mx="auto">
            <form onSubmit={form.onSubmit(() => onSaveRole())}>
                <TextInput
                  withAsterisk
                  label="名称"
                  placeholder="请输入角色名称"
                  {...form.getInputProps('name')}
                />

                <TextInput
                  withAsterisk
                  label="编码"
                  placeholder="请输入编码"
                  {...form.getInputProps('code')}
                />

                <Input.Wrapper label="状态">
                    <Switch
                      onLabel="启用"
                      offLabel="禁用"
                      checked={checked}
                      onChange={(event) => setChecked(event.currentTarget.checked)}
                    />
                </Input.Wrapper>

                <Textarea
                  label="描述"
                  placeholder="请输入描述"
                  {...form.getInputProps('comments')}
                />

                <Group justify="right" mt="md">
                    <Button leftSection={<IconCheck />} type="submit">提交</Button>
                </Group>
            </form>
        </Box>
    );

    return (
        <>
            <BasicModal isOpen={open} onClose={onCloseModal} title={roleId ? '编辑角色' : '添加角色'}>
                {formBody}
            </BasicModal>
        </>
    );
};

export default EditForm;
