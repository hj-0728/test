import { useMessage } from '/@/hooks/web/useMessage';
import { createVNode } from 'vue';
import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { apiResetUserPassword } from '/@/api/user/user';
import { clearAuthCache } from '/@/utils/auth';
import { PageEnum } from '/@/enums/pageEnum';
import { apiChangeActivated } from '/@/api/sys/user';

export function resetUserPassword(user, that) {
  const title = '点击确定会生成新密码，是否要重置？';
  useMessage().createConfirm({
    iconType: 'info',
    title: () => title,
    centered: true,
    icon: () => createVNode(ExclamationCircleOutlined),
    onOk: () => {
      that.setLoading(true);
      apiResetUserPassword(user)
        .then((res) => {
          if (res.code === 200) {
            setTimeout(() => {
              useMessage().createInfoModal({
                content:
                  '<div style="padding: 0 40px">' +
                  ' <div style="font-size: 16px; color: black">' +
                  '   <span>用户</span>' +
                  '   <span style="font-weight: bold">' +
                  user.name +
                  '</span>' +
                  '   <span>的密码重置成功</span>' +
                  ' </div>' +
                  ' <div style="height: 10px"></div>' +
                  ' <div>' +
                  '   <span>新密码为：</span>' +
                  '   <span style="font-weight: bold">' +
                  res.data +
                  '</span>' +
                  ' </div>' +
                  ' <div style="height: 5px"></div>' +
                  ' <div>' +
                  '   <span>关闭弹窗后将不再显示</span>' +
                  ' </div>' +
                  '</div>',
                closable: true,
                maskClosable: false,
                showOkBtn: true,
                showCancelBtn: false,
                okText: '复制到剪贴板',
                onOk: () => {
                  navigator.clipboard.writeText(res.data).then(() => {
                    useMessage().createSuccessNotification({
                      message: '操作成功',
                      description: '复制成功',
                    });
                    if (user.id === that.currentUserId) {
                      clearAuthCache();
                      that.$router.push(PageEnum.BASE_LOGIN);
                    } else {
                      that.setLoading(false);
                    }
                  });
                },
                onCancel: () => {
                  if (user.id === that.currentUserId) {
                    clearAuthCache();
                    that.$router.push(PageEnum.BASE_LOGIN);
                  } else {
                    that.setLoading(false);
                  }
                },
              } as any);
              that.getUserList();
            }, 1000);
          } else {
            useMessage().createErrorNotification({
              message: '操作失败',
              description: res.error.message,
            });
            that.setLoading(false);
          }
        })
        .catch(() => {
          useMessage().createErrorNotification({
            message: '保存失败',
            description: '网络错误',
          });
          that.setLoading(false);
        });
    },
  });
}

export function changeUserActivated(user, that) {
  that.setLoading(true);
  that.switchDisabled = true;
  apiChangeActivated(user)
    .then((res) => {
      if (res.code === 200) {
        useMessage().createSuccessNotification({
          message: '修改成功',
        });
        setTimeout(() => {
          if (user.id === that.currentUserId) {
            clearAuthCache();
            that.setLoading(false);
            that.$router.push(PageEnum.BASE_LOGIN);
          } else {
            that.getUserList();
          }
          that.switchDisabled = false;
        }, 1000);
      } else {
        useMessage().createErrorNotification({
          message: '错误',
          description: res.error.message,
        });
        that.setLoading(false);
      }
    })
    .catch(() => {
      useMessage().createErrorNotification({
        message: '错误',
        description: '网络错误',
      });
      that.setLoading(false);
    });
}
