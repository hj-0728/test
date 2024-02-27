import type { ModalFunc, ModalFuncProps } from 'ant-design-vue/lib/modal/Modal';

import { Modal, message as Message, notification } from 'ant-design-vue';
import { InfoCircleFilled, CheckCircleFilled, CloseCircleFilled } from '@ant-design/icons-vue';

import { NotificationArgsProps, ConfigProps } from 'ant-design-vue/lib/notification';
import { useI18n } from './useI18n';
import { isString } from '/@/utils/is';

export interface NotifyApi {
  info(config: NotificationArgsProps): void;
  success(config: NotificationArgsProps): void;
  error(config: NotificationArgsProps): void;
  warn(config: NotificationArgsProps): void;
  warning(config: NotificationArgsProps): void;
  open(args: NotificationArgsProps): void;
  close(key: String): void;
  config(options: ConfigProps): void;
  destroy(): void;
}

export declare type NotificationPlacement = 'topLeft' | 'topRight' | 'bottomLeft' | 'bottomRight';
export declare type IconType = 'success' | 'info' | 'error' | 'warning';
export interface ModalOptionsEx extends Omit<ModalFuncProps, 'iconType'> {
  iconType: 'warning' | 'success' | 'error' | 'info';
}
export type ModalOptionsPartial = Partial<ModalOptionsEx> & Pick<ModalOptionsEx, 'content'>;

interface ConfirmOptions {
  info: ModalFunc;
  success: ModalFunc;
  error: ModalFunc;
  warn: ModalFunc;
  warning: ModalFunc;
}

function getIcon(iconType: string) {
  if (iconType === 'warning') {
    return <InfoCircleFilled class="modal-icon-warning" />;
  } else if (iconType === 'success') {
    return <CheckCircleFilled class="modal-icon-success" />;
  } else if (iconType === 'info') {
    return <InfoCircleFilled class="modal-icon-info" />;
  } else {
    return <CloseCircleFilled class="modal-icon-error" />;
  }
}

function renderContent({ content }: Pick<ModalOptionsEx, 'content'>) {
  if (isString(content)) {
    return <div innerHTML={`<div>${content as string}</div>`}></div>;
  } else {
    return content;
  }
}

/**
 * @description: Create confirmation box
 */
function createConfirm(options: ModalOptionsEx): ConfirmOptions {
  const iconType = options.iconType || 'warning';
  Reflect.deleteProperty(options, 'iconType');
  const opt: ModalFuncProps = {
    centered: true,
    icon: getIcon(iconType),
    ...options,
    content: renderContent(options),
  };
  return Modal.confirm(opt) as unknown as ConfirmOptions;
}

const getBaseOptions = () => {
  const { t } = useI18n();
  return {
    okText: t('common.okText'),
    centered: true,
  };
};

function createModalOptions(options: ModalOptionsPartial, icon: string): ModalOptionsPartial {
  return {
    ...getBaseOptions(),
    ...options,
    content: renderContent(options),
    icon: getIcon(icon),
  };
}

function createSuccessModal(options: ModalOptionsPartial) {
  return Modal.success(createModalOptions(options, 'success'));
}

function createErrorModal(options: ModalOptionsPartial) {
  const modalCollection: HTMLCollection = document.getElementsByClassName(
    'ant-modal-confirm-content',
  );
  const f =
    Number(options.title?.toString().indexOf('网络')) > -1 ||
    Number(options.content?.toString().indexOf('网络')) > -1;
  for (let i = 0; i < modalCollection.length; i++) {
    const innerText = modalCollection[i]['innerText'];
    if (innerText.indexOf('网络') > -1 && f) {
      return;
    }
  }
  return Modal.error(createModalOptions(options, 'close'));
}

function createInfoModal(options: ModalOptionsPartial) {
  return Modal.info(createModalOptions(options, 'info'));
}

function createWarningModal(options: ModalOptionsPartial) {
  return Modal.warning(createModalOptions(options, 'warning'));
}
function destroyAll() {
  return Modal.destroyAll();
}

function createNotificationArgsProps(
  options: NotificationArgsProps,
  className: string,
): NotificationArgsProps {
  return {
    ...options,
    class: className,
  };
}

function createSuccessNotification(options: NotificationArgsProps) {
  return notification.success(
    createNotificationArgsProps(options, 'ant-notification-notice-for-success'),
  );
}
function createErrorNotification(options: NotificationArgsProps, styleWhiteSpace: any = null) {
  if (styleWhiteSpace !== null) {
    if (!options.style) {
      options.style = { whiteSpace: styleWhiteSpace };
    } else {
      options.style.whiteSpace = styleWhiteSpace;
    }
  }

  const modalCollection: HTMLCollection = document.getElementsByClassName(
    'ant-modal-confirm-content',
  );
  const f =
    Number(options.message?.toString().indexOf('网络')) > -1 ||
    Number(options.description?.toString().indexOf('网络')) > -1;
  for (let i = 0; i < modalCollection.length; i++) {
    const innerText = modalCollection[i]['innerText'];
    if (innerText.indexOf('网络') > -1 && f) {
      return;
    }
  }

  return notification.error(
    createNotificationArgsProps(options, 'ant-notification-notice-for-error'),
  );
}
function createInfoNotification(options: NotificationArgsProps) {
  return notification.info(
    createNotificationArgsProps(options, 'ant-notification-notice-for-info'),
  );
}
function createWarningNotification(options: NotificationArgsProps) {
  return notification.warning(
    createNotificationArgsProps(options, 'ant-notification-notice-for-warning'),
  );
}

notification.config({
  placement: 'topRight',
  duration: 3,
});

/**
 * @description: message
 */
export function useMessage() {
  return {
    createMessage: Message,
    notification: notification as NotifyApi,
    createConfirm: createConfirm,
    createSuccessModal,
    createErrorModal,
    createInfoModal,
    createWarningModal,
    createSuccessNotification,
    createErrorNotification,
    createInfoNotification,
    createWarningNotification,
    destroyAll,
  };
}
