import { Modal } from '@mantine/core';
import { ReactNode } from 'react';

interface BasicModalProps {
  isOpen: boolean; // Modal是否打开
  onClose: () => void; // 关闭Modal的函数
  title: string; // Modal的标题
  children: ReactNode; // Modal的内容
  footer?: ReactNode; // Modal的页脚内容，可选属性
}

// 公共Modal组件
function BasicModal({ isOpen, onClose, title, children, footer }: BasicModalProps) {
  return (
    <Modal opened={isOpen} onClose={onClose} title={title} centered size="lg">
      {children}
      <div style={{ marginTop: '10px', textAlign: 'right' }}>
        {footer}
      </div>
    </Modal>
  );
}

export default BasicModal;
