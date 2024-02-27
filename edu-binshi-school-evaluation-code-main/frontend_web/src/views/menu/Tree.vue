<template>
  <div>
    <PageWrapper>
      <Loading :loading="loading" />
      <div class="md:flex" style="height: calc(100vh - 200px); position: relative">
        <div class="md:w-1/2 w-full h-full tree-container">
          <div style="display: flex">
            <InputSearch
              v-model:value="searchValue"
              placeholder="搜索"
              enter-button
              style="padding: 10px 0 10px 10px; flex: 1"
              @search="onSearch"
            />
            <div>
              <a-button
                color="success"
                preIcon="ci:refresh"
                @click="refreshPage"
                class="btn-toolbar btn-refresh"
                >刷新
              </a-button>
              <a-button
                color="success"
                preIcon="jam:refresh-reverse"
                class="btn-toolbar"
                @click="onSaveMenuSort"
                >保存排序
              </a-button>
            </div>
          </div>
          <BasicTree
            v-if="treeData.length"
            :beforeRightClick="getRightMenuList"
            :treeData="treeData"
            :defaultExpandAll="true"
            :clickRowToExpand="false"
            :draggable="true"
            @drop="onDrop"
            @select="onSelectedMenu"
          >
            <template #title="{ title, icon }">
              <Icon :icon="icon ? icon : 'mdi:format-list-bulleted'" style="margin-right: 5px" />
              <div v-if="title.indexOf(searchValue) > -1">
                {{ title.substr(0, title.indexOf(searchValue)) }}
                <span style="color: #f50">{{ searchValue }}</span>
                {{ title.substr(title.indexOf(searchValue) + searchValue.length) }}
              </div>
              <span v-else>{{ title }}</span>
            </template>
          </BasicTree>
        </div>
        <div class="md:w-1/2 w-full h-full">
          <Detail ref="refMenuDetail" />
        </div>
      </div>
    </PageWrapper>
    <Editor ref="refMenuEditor" @register="registerEditor" />
    <AbilityPermissionAssign @register="registerGranted" />
  </div>
</template>
<script lang="ts">
  import { createVNode, defineComponent, ref } from 'vue';
  import { BasicTree, ContextMenuItem } from '/@/components/Tree/index';
  import { Icon } from '/@/components/Icon';
  import { PageWrapper } from '/@/components/Page';
  import { apiDeleteMenu, apiGetMenuTree, apiUpdateMenuSort } from '/@/api/menu/menu';
  import Editor from './Editor.vue';
  import Detail from './Detail.vue';
  import { TreeDataItem, AntTreeNodeDropEvent } from 'ant-design-vue/es/tree/Tree';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Input, Modal } from 'ant-design-vue';
  import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
  import { useTabs } from '/@/hooks/web/useTabs';
  import AbilityPermissionAssign from '/@/components/AbilityPermissionAssign/index.vue';
  import { useModal } from '/@/components/Modal';
  import { Loading } from '/@/components/Loading';
  import { TRANSITION_NAME, MASK_TRANSITION_NAME } from '/@/settings/transitionSetting';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  export default defineComponent({
    components: {
      BasicTree,
      PageWrapper,
      Icon,
      Editor,
      Detail,
      Loading,
      AbilityPermissionAssign,
      InputSearch: Input.Search,
    },
    setup() {
      const treeData = ref([]) as any;
      const originalDeptTreeList = ref();
      const menuList = ref([]);
      const expandedKeys = ref(['#']);
      const searchValue = ref('');
      const searchText = ref('');
      const onClickMenu = ref(null);
      const { notification, createErrorModal } = useMessage();
      const { refreshPage } = useTabs();
      const [registerGranted, { openModal: openGrantedModal }] = useModal();
      const [registerEditor, { openModal: openEditorModal }] = useModal();
      const loading = ref(true);
      return {
        treeData,
        originalDeptTreeList,
        menuList,
        expandedKeys,
        searchValue,
        searchText,
        registerEditor,
        openEditorModal,
        onClickMenu,
        notification,
        createErrorModal,
        refreshPage,
        registerGranted,
        openGrantedModal,
        loading,
        TRANSITION_NAME,
        MASK_TRANSITION_NAME,
      };
    },
    created() {
      this.getMenuTree();
    },
    methods: {
      onSearch() {
        this.loading = true;
        const data = searchTree(this.searchValue, this.originalDeptTreeList);
        this.searchText = this.searchValue;
        this.treeData = data.treeData;
        this.expandedKeys = data.expandedKeys;
        this.loading = false;
      },
      getRightMenuList(node: any): ContextMenuItem[] {
        const menuId = node.eventKey;
        const actions = [
          {
            label: '添加子项',
            handler: () => {
              this.prepareEditMenu(menuId, 'create');
            },
            icon: 'bi:plus',
          },
        ];
        if (menuId !== '#') {
          actions.push(
            {
              label: '编辑',
              handler: () => {
                this.prepareEditMenu(menuId, 'edit');
              },
              icon: 'mdi:comment-edit-outline',
            },
            {
              label: '删除',
              handler: () => {
                Modal.confirm({
                  transitionName: this.TRANSITION_NAME,
                  maskTransitionName: this.MASK_TRANSITION_NAME,
                  title: () => '确定要删除该菜单及子菜单吗？',
                  centered: true,
                  icon: () => createVNode(ExclamationCircleOutlined),
                  onOk: () => {
                    this.deleteMenu(menuId);
                  },
                });
              },
              icon: 'bx:bxs-folder-open',
            },
            {
              label: '功能权限',
              handler: () => {
                this.openGrantedModal(true, { assignResourceCategory: 'MENU', id: menuId });
              },
              icon: 'ant-design:setting-filled',
            },
          );
        }
        return actions;
      },
      prepareEditMenu(menuId, action) {
        this.filterCurrentMenu(menuId);
        this.$refs.refMenuEditor.onClickMenu = this.onClickMenu;
        this.$refs.refMenuEditor.prepareFormFiledSchema(action);
        this.openEditorModal(true);
      },

      filterCurrentMenu(menuId) {
        this.menuList.map((t) => {
          if (t.key === menuId) {
            this.onClickMenu = t;
          }
        });
      },
      getMenuTree() {
        this.loading = true;
        apiGetMenuTree('WEB')
          .then((res) => {
            if (res.code === 200) {
              this.originalDeptTreeList = res.data;
              this.treeData = [
                {
                  id: '#',
                  name: '菜单树',
                  children: res.data,
                },
              ];
              this.expandMenuTree(this.treeData);
            }
          })
          .finally(() => {
            this.loading = false;
          });
      },

      expandMenuTree(tree) {
        tree.map((t) => {
          t.childList = t.children;
          t.key = t.id;
          t.title = t.name;
          this.menuList.push(t);
          this.expandedKeys.push(t.id);
          if (t.childList && t.childList.length > 0) {
            this.expandMenuTree(t.childList);
          }
        });
      },

      deleteMenu(menuId) {
        apiDeleteMenu(menuId)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '删除成功',
              });
              setTimeout(() => {
                this.refreshPage();
              }, 2000);
            } else {
              useMessage().createErrorNotification({
                message: '操作失败',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorModal({
              title: '操作失败',
              content: '网络异常，请检查您的网络连接是否正常!',
              closable: true,
              maskClosable: false,
              showOkBtn: true,
              showCancelBtn: false,
            });
          });
      },

      onDrop(info: AntTreeNodeDropEvent) {
        if (info.node.eventKey === '#') {
          return;
        }
        const dropKey = info.node.eventKey;
        const dragKey = info.dragNode.eventKey;
        const dropPos = info.node.pos.split('-');
        const dropPosition = info.dropPosition - Number(dropPos[dropPos.length - 1]);
        const loop = (data: TreeDataItem[], key: string, callback: any) => {
          data.forEach((item, index, arr) => {
            if (item.key === key) {
              return callback(item, index, arr);
            }
            if (item.children) {
              return loop(item.children, key, callback);
            }
          });
        };
        const data = [...this.treeData];
        let dragObj: TreeDataItem = {};
        loop(data, dragKey, (item: TreeDataItem, index: number, arr: TreeDataItem[]) => {
          arr.splice(index, 1);
          dragObj = item;
        });
        if (!info.dropToGap) {
          // Drop on the content
          loop(data, dropKey, (item: TreeDataItem) => {
            item.children = item.children || [];
            // where to insert 示例添加到尾部，可以是随意位置
            item.children.push(dragObj);
          });
        } else if (
          (info.node.children || []).length > 0 && // Has children
          info.node.expanded && // Is expanded
          dropPosition === 1 // On the bottom gap
        ) {
          loop(data, dropKey, (item: TreeDataItem) => {
            item.children = item.children || [];
            // where to insert 示例添加到尾部，可以是随意位置
            item.children.unshift(dragObj);
          });
        } else {
          let ar: TreeDataItem[] = [];
          let i = 0;
          loop(data, dropKey, (item: TreeDataItem, index: number, arr: TreeDataItem[]) => {
            ar = arr;
            i = index;
          });
          if (dropPosition === -1) {
            ar.splice(i, 0, dragObj);
          } else {
            ar.splice(i + 1, 0, dragObj);
          }
        }
        this.treeData = data;
      },

      onSaveMenuSort() {
        Modal.confirm({
          transitionName: this.TRANSITION_NAME,
          maskTransitionName: this.MASK_TRANSITION_NAME,
          title: () => '确定要更新排序吗？',
          centered: true,
          icon: () => createVNode(ExclamationCircleOutlined),
          onOk: () => {
            const res = [];
            this.buildMenuTreeNewSortInfo(this.treeData[0].children, null, res);
            apiUpdateMenuSort(res)
              .then((res) => {
                if (res.code === 200) {
                  useMessage().createSuccessNotification({
                    message: '操作成功',
                    description: '更新成功',
                  });
                  setTimeout(() => {
                    this.refreshPage();
                  }, 2000);
                } else {
                  useMessage().createErrorNotification({
                    message: '操作失败',
                    description: res.error.message,
                  });
                }
              })
              .catch(() => {
                useMessage().createErrorModal({
                  title: '操作失败',
                  content: '网络异常，请检查您的网络连接是否正常!',
                  closable: true,
                  maskClosable: false,
                  showOkBtn: true,
                  showCancelBtn: false,
                });
              });
          },
        });
      },

      buildMenuTreeNewSortInfo(treeData, parentId, res) {
        treeData.map((t, idx) => {
          t.parentId = parentId;
          t.seq = idx;
          res.push(t);
          if (t.children.length > 0) {
            this.buildMenuTreeNewSortInfo(t.children, t.id, res);
          }
        });
      },

      onSelectedMenu(menuIds) {
        this.$refs.refMenuDetail.onClickMenu = null;
        setTimeout(() => {
          this.filterCurrentMenu(menuIds[0]);
          this.$refs.refMenuDetail.onClickMenu = this.onClickMenu;
        });
      },
    },
  });
</script>

<style>
  .btn-toolbar {
    margin: 10px 0 10px 1px;
    padding: 6px 8px;
  }

  .btn-refresh {
    background: #4bc0c0 !important;
    border-color: #4bc0c0 !important;
  }

  .tree-container {
    background: #ffffff;
    padding: 10px 10px 60px 10px;
  }
</style>
