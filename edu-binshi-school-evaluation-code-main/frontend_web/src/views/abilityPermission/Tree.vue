<template>
  <div>
    <PageWrapper>
      <Loading :loading="loading" />
      <div class="md:flex tree">
        <div class="md:w-1/2 w-full h-full tree-container">
          <div style="display: flex">
            <InputSearch
              v-model:value="searchValue"
              placeholder="搜索"
              enter-button
              class="input-search"
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
                @click="onSaveAbilityPermissionSort"
                class="btn-toolbar"
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
            @select="onSelectedPermission"
          >
            <template #title="{ title, node_type }">
              <Icon
                :icon="
                  node_type === 'ABILITY_PERMISSION_GROUP'
                    ? 'mdi:folder-open-outline'
                    : node_type === 'ABILITY_PERMISSION'
                    ? 'mdi:square-medium'
                    : 'mdi:format-list-bulleted-square'
                "
                style="margin-right: 5px"
              />
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
          <Detail ref="refAbilityPermissionDetail" />
        </div>
      </div>
    </PageWrapper>
    <Editor ref="refAbilityPermissionEditor" @register="registerEditor" />
  </div>
</template>
<script lang="ts">
  import { createVNode, defineComponent, ref } from 'vue';
  import { BasicTree, ContextMenuItem } from '/@/components/Tree/index';
  import { Icon } from '/@/components/Icon';
  import { PageWrapper } from '/@/components/Page';
  import { useTabs } from '/@/hooks/web/useTabs';
  import Editor from './Editor.vue';
  import Detail from './Detail.vue';
  import { DropEvent, TreeDataItem } from 'ant-design-vue/es/tree/Tree';
  import { useMessage } from '/@/hooks/web/useMessage';
  import {
    apiDeleteAbilityPermission,
    apiGetAbilityPermissionTree,
    apiUpdateAbilityPermissionSort,
  } from '/@/api/abilityPermission/abilityPermission';
  import { cloneDeep } from 'lodash-es';
  import { Input, Modal } from 'ant-design-vue';
  import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
  import { abilityPermissionTree } from '/@/api/abilityPermission/model/abilityPermissionModel';
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
      InputSearch: Input.Search,
    },
    setup() {
      const treeData = ref([]) as any;
      const originalDeptTreeList = ref();
      const permissionList = ref([]);
      const dragPermissionList = ref([]);
      const expandedKeys = ref(['#']);
      const searchValue = ref('');
      const searchText = ref('');
      const onClickPermission = ref(null);
      const { refreshPage } = useTabs();
      const { notification, createErrorModal } = useMessage();
      const [registerEditor, { openModal: openEditorModal }] = useModal();
      const loading = ref(true);
      return {
        treeData,
        originalDeptTreeList,
        permissionList,
        expandedKeys,
        searchValue,
        searchText,
        onClickPermission,
        refreshPage,
        createErrorModal,
        notification,
        dragPermissionList,
        registerEditor,
        openEditorModal,
        loading,
        TRANSITION_NAME,
        MASK_TRANSITION_NAME,
      };
    },

    created() {
      this.getAbilityPermissionTree();
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
        let permission: abilityPermissionTree = this.filterCurrentPermission(node.eventKey);
        let actions = [];
        const btnAddChild = {
          label: '添加子项',
          handler: () => {
            this.prepareEditAbilityPermission(permission, 'create');
          },
          icon: 'bi:plus',
        };
        const btnEdit = {
          label: '编辑',
          handler: () => {
            this.prepareEditAbilityPermission(permission, 'edit');
          },
          icon: 'mdi:comment-edit-outline',
        };
        const btnDel = {
          label: '删除',
          handler: () => {
            Modal.confirm({
              transitionName: this.TRANSITION_NAME,
              maskTransitionName: this.MASK_TRANSITION_NAME,
              title: () => '确定要删除该功能权限吗？',
              centered: true,
              icon: () => createVNode(ExclamationCircleOutlined),
              onOk: () => {
                this.deleteAbilityPermission(permission);
              },
            });
          },
          icon: 'bx:bxs-folder-open',
        };
        if (permission.node_type === 'root') {
          actions.push(btnAddChild);
        } else if (permission.node_type === 'ABILITY_PERMISSION_GROUP') {
          actions.push(btnAddChild);
          actions.push(btnEdit);
          actions.push(btnDel);
        } else if (permission.node_type === 'ABILITY_PERMISSION') {
          actions.push(btnEdit);
          actions.push(btnDel);
        }
        return actions;
      },
      prepareEditAbilityPermission(permission, action) {
        this.onClickPermission = permission;
        this.$refs.refAbilityPermissionEditor.onClickAbilityPermission = this.onClickPermission;
        this.$refs.refAbilityPermissionEditor.prepareFormFiledSchema(action);
        this.openEditorModal();
      },

      filterCurrentPermission(permissionId) {
        let permission = {};
        this.permissionList.map((t) => {
          if (t.key === permissionId) {
            permission = t;
            this.onClickPermission = t;
          }
        });
        return permission;
      },
      getAbilityPermissionTree() {
        apiGetAbilityPermissionTree()
          .then((res) => {
            if (res.code === 200) {
              this.originalDeptTreeList = res.data;
              this.treeData = [
                {
                  id: '#',
                  name: '功能权限树',
                  children: res.data,
                  node_type: 'root',
                },
              ];
              this.expandAbilityPermissionTree(this.treeData);
              this.dragPermissionList = cloneDeep(this.permissionList);
            }
          })
          .finally(() => {
            this.loading = false;
          });
      },

      expandAbilityPermissionTree(tree) {
        tree.map((t) => {
          t.key = t.id;
          t.title = t.name;
          t.nodeDesc =
            t.node_type === 'root'
              ? '根'
              : t.node_type === 'ABILITY_PERMISSION'
              ? '功能权限'
              : '功能权限分组';
          this.permissionList.push(t);
          this.expandedKeys.push(t.id);
          console.log(t);
          if (t.children && t.children.length > 0) {
            this.expandAbilityPermissionTree(t.children);
          }
        });
      },

      onCloseEditor() {
        this.$refs.refAbilityPermissionEditor.onClickAbilityPermission = null;
      },

      deleteAbilityPermission(permission) {
        apiDeleteAbilityPermission(permission.id)
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

      onDrop(info: DropEvent) {
        const dropKey = info.node.eventKey;
        const dragKey = info.dragNode.eventKey;
        const dropPos = info.node.pos.split('-');
        const dropPosition = info.dropPosition - Number(dropPos[dropPos.length - 1]);
        const dropPermission = this.filerFromDragPermission(dropKey);
        const dropParentPermission = this.filerFromDragPermission(dropPermission.parent_id);
        const dragPermission = this.filerFromDragPermission(dragKey);
        // console.log('\n\n');
        // console.log(cloneDeep(dragPermission));
        // console.log(cloneDeep(dropPermission));
        // console.log(cloneDeep(dropParentPermission));
        // console.log(cloneDeep(dropPosition));
        console.log(dragPermission);
        let canDrag = false;
        if (dragPermission.node_type === 'ABILITY_PERMISSION') {
          if (dropPermission.node_type === 'root') {
            // 直接拖动到最上层的情况，即根目录位置
            canDrag = false;
          } else if (dragPermission.parent_id === dropPermission.id && dropParentPermission.id) {
            canDrag = true;
          } else if (
            dropPermission.node_type === 'ABILITY_PERMISSION' &&
            dropParentPermission.node_type === 'ABILITY_PERMISSION_GROUP' &&
            dropPosition !== 0
          ) {
            canDrag = true;
          } else if (dropPermission.node_type === 'ABILITY_PERMISSION_GROUP') {
            if (
              (dropPermission.parent_id && dropParentPermission.id) ||
              (!dropPermission.parent_id && !dropParentPermission.id)
            ) {
              canDrag = true;
            }
          }
        }
        if (dragPermission.node_type === 'ABILITY_PERMISSION_GROUP') {
          // 如果拖动是文件夹，不是拖动到权限下面都可以允许
          if (dropPermission.node_type !== 'ABILITY_PERMISSION') {
            canDrag = true;
          }
        }
        if (!canDrag) {
          return;
        }
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
        const res = [];
        this.buildAbilityPermissionTreeNewSortInfo(this.treeData[0].children, null, res);
        this.dragPermissionList = cloneDeep(res);
      },

      filerFromDragPermission(permissionId) {
        let permission = {};
        this.dragPermissionList.map((t) => {
          if (t.id === permissionId) {
            permission = t;
          }
        });
        return permission;
      },

      onSaveAbilityPermissionSort() {
        Modal.confirm({
          transitionName: this.TRANSITION_NAME,
          maskTransitionName: this.MASK_TRANSITION_NAME,
          title: () => '确定要更新排序吗？',
          centered: true,
          icon: () => createVNode(ExclamationCircleOutlined),
          onOk: () => {
            const res = [];
            this.buildAbilityPermissionTreeNewSortInfo(this.treeData[0].children, null, res);
            apiUpdateAbilityPermissionSort(res)
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
                  howCancelBtn: false,
                });
              });
          },
        });
      },

      buildAbilityPermissionTreeNewSortInfo(treeData, parentId, res) {
        treeData.map((t, idx) => {
          t.parent_id = parentId;
          t.seq = idx + 1;
          res.push(t);
          if (t.children.length > 0) {
            this.buildAbilityPermissionTreeNewSortInfo(t.children, t.id, res);
          }
        });
      },

      onSelectedPermission(permissionIds) {
        this.$refs.refAbilityPermissionDetail.onClickPermission = null;
        setTimeout(() => {
          this.filterCurrentPermission(permissionIds[0]);
          this.$refs.refAbilityPermissionDetail.onClickPermission = this.onClickPermission;
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

  .tree {
    height: calc(100vh - 200px);
    position: relative;
  }

  .tree-container {
    background: #ffffff;
    padding: 10px 10px 60px 10px;
  }

  .input-search {
    padding: 10px 0 10px 10px;
    flex: 1;
  }
</style>
