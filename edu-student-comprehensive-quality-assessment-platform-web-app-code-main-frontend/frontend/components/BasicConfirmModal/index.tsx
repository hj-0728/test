import { modals } from '@mantine/modals';
import { Text } from '@mantine/core';
import React from 'react';

interface ConfirmModalProps {
  title?: string;
  message?: string | React.ReactNode;
  onConfirm: () => void;
  onCancel?: () => void;
  confirmLabel?: string;
  cancelLabel?: string;
}

const openConfirmModal = ({
                            title = '提示',
                            message,
                            onConfirm,
                            onCancel,
                            confirmLabel = '确定',
                            cancelLabel = '取消',
                          }: ConfirmModalProps) => {
  modals.openConfirmModal({
    title,
    centered: true,
    zIndex: 300,
    withCloseButton: false,
    closeOnClickOutside: false,
    closeOnEscape: false,
    children: message || (
      <Text size="sm">
        确定要提交吗？
      </Text>
    ),
    labels: { confirm: confirmLabel, cancel: cancelLabel },
    onConfirm,
    onCancel,
  });
};

export default openConfirmModal;
