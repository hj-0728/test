import { notifications } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons-react';

export const showErrorNotification = (message: string) => {
    notifications.show({
        autoClose: 3000,
        title: '失败',
        message,
        color: 'red',
        icon: <IconX />,
    });
};

export const showSuccessNotification = (message: string) => {
    notifications.show({
        autoClose: 3000,
        title: '成功',
        message,
        color: 'teal',
        icon: <IconCheck />,
    });
};
