<template>
  <div ref="modal">
    <BasicModal
      v-bind="$attrs"
      @register="register"
      :showCancelBtn="false"
      :showOkBtn="false"
      width="60%"
      :getContainer="() => $refs.modal"
    >
      <template #title>
        <div>
          <AuditOutlined />
          功能权限授权
        </div>
      </template>
      <div class="md:w-full">
        <div style="display: flex">
          <InputSearch
            v-model:value="searchValue"
            placeholder="搜索"
            enter-button
            @search="onSearch"
            style="padding: 10px 0"
          />
          <a-button
            type="primary"
            preIcon="akar-icons:circle-check-fill"
            :iconSize="18"
            style="background: #48ce7d; border-color: #48ce7d; margin: 10px 0"
            @click="saveGranted"
            title="保存授权"
          >
            保存授权
          </a-button>
        </div>
        <BasicTree
          ref="basicTree"
          v-if="treeData.length > 0"
          :checkable="true"
          :fieldNames="{ title: 'name', key: 'id' }"
          :loading="loading"
          :expandedKeys="expandedKeys"
          :checkedKeys="checkedKeys"
          :treeData="treeData"
          :defaultExpandAll="true"
          :clickRowToExpand="false"
          :defaultExpandLevel="1"
          @check="handleCheck"
          style="margin-bottom: 20px"
        >
          <template #name="{ name, node_type }">
            <Icon
              :icon="
                node_type === 'ability_permission_folder'
                  ? 'mdi:folder-open-outline'
                  : node_type === 'ability_permission'
                  ? 'mdi:square-medium'
                  : 'mdi:format-list-bulleted-square'
              "
              style="margin-right: 5px"
            />
            <div v-if="name.indexOf(searchText) > -1">
              {{ name.substr(0, name.indexOf(searchText)) }}
              <span style="color: #f50">{{ searchText }}</span>
              {{ name.substr(name.indexOf(searchText) + searchText.length) }}
            </div>
            <span v-else>{{ name }}</span>
          </template>
        </BasicTree>
      </div>
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { Icon } from '/@/components/Icon';
  import { TreeDataItem, AntTreeNodeDropEvent } from 'ant-design-vue/lib/tree/Tree';
  import { defineComponent, nextTick, ref, unref, watch } from 'vue';
  import {
    apiGetAbilityPermissionAssignTree,
    apiSaveAbilityPermissionAssign,
  } from '/@/api/abilityPermission/abilityPermission';
  import {
    GrantedResponseModel,
    SaveGrantedResponseModel,
  } from '/@/api/abilityPermission/model/abilityPermissionModel';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicTree } from '/@/components/Tree';
  import { AuditOutlined } from '@ant-design/icons-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import _ from 'lodash-es';
  import { apiGetRouteAbilityPermissionAssignTree } from '/@/api/route/route';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Input } from 'ant-design-vue';

  export default defineComponent({
    components: { BasicModal, BasicTree, Icon, AuditOutlined, InputSearch: Input.Search },
    emits: ['saveGranted'],
    setup() {
      const assignResourceCategory = ref('');
      const treeData = ref<any>([]);
      const permittedResourceIds = ref([]);
      const assignResourceId = ref<string>('');
      const [register, { closeModal, setModalProps }] = useModalInner(async (data) => {
        console.log('call back data ...');
        console.log(data);
        checkedKeys.value = [];
        assignResourceId.value = data.id;
        assignResourceCategory.value = data.assignResourceCategory;
        category.value = data.category;
        routeId.value = data.routeId;
        if (data.category === 'route') {
          category.value = data.category;
          routeId.value = data.routeId;
          permittedResourceIds.value = data.permittedResourceIds;
        } else {
          assignResourceId.value = data.id;
          assignResourceCategory.value = data.assignResourceCategory;
        }
        await onLoadTreeData();
      });
      // const replaceFields = {
      //   title: 'name',
      //   key: 'id',
      // };
      const routeId = ref('');
      const searchValue = ref<string>('');
      const autoExpandParent = ref<boolean>(true);
      const loading = ref<boolean>(true);
      const expandedKeys = ref<string[]>(['#']);
      const checkedKeys = ref<string[]>([]);
      // const abilityPermissionFolderIdList = ref([]);
      const basicTree = ref<HTMLDivElement | null>(null);
      const category = ref('');
      const deptTreeList = ref<object[]>([]);
      const searchText = ref('');
      const originalDeptTreeList = ref<object[]>([]);
      const onLoadTreeData = async () => {
        const params: GrantedResponseModel = {
          assignResourceCategory: assignResourceCategory.value,
          assignResourceId: assignResourceId.value,
        };
        let res;
        if (category.value === 'route') {
          res = await apiGetRouteAbilityPermissionAssignTree(routeId.value).finally(() => {
            loading.value = false;
          });
          if (permittedResourceIds.value.length) {
            selectedIdList(res.data);
          }
        } else {
          res = await apiGetAbilityPermissionAssignTree(params).finally(() => {
            loading.value = false;
          });
        }
        console.log('abilityPermissionTree ***');
        console.log(res);
        originalDeptTreeList.value = res.data;
        treeData.value = [
          {
            id: '#',
            name: '权限树',
            children: res.data,
          },
        ];

        generateList(treeData.value);
        await nextTick();
        unref(basicTree)?.filterByLevel(100);
        if (expandedKeys.value.length > 0) {
          unref(basicTree)?.setExpandedKeys(expandedKeys.value);
        }
      };

      /*async function getAbilityPermissionFolderIdList() {
        const res = await apiGetAbilityPermissionFolderIdList();
        if (res.code === 200) {
          abilityPermissionFolderIdList.value = res.data;
        }
      }

      onMounted(() => {
        getAbilityPermissionFolderIdList();
      });*/
      const dataList: TreeDataItem[] = [];
      const generateList = (data: TreeDataItem[]) => {
        for (let i = 0; i < data.length; i++) {
          const node = data[i];
          const id = node.id;
          expandedKeys.value.push(node.id);
          dataList.push({ id, name: node.name as string });
          if (node.granted) {
            checkedKeys.value.push(node.id);
          }
          if (node.children) {
            generateList(node.children);
          }
        }
      };
      watch(expandedKeys, () => {
        console.log('expandedKeys', expandedKeys);
      });
      const selectedIdList = (data: TreeDataItem[]) => {
        for (let i = 0; i < data.length; i++) {
          const node = data[i];
          permittedResourceIds.value.includes(node.id)
            ? (node.granted = true)
            : (node.granted = false);

          if (node.children) {
            selectedIdList(node.children);
          }
        }
      };
      return {
        loading,
        treeData,
        register,
        closeModal,
        setModalProps,
        expandedKeys,
        checkedKeys,
        autoExpandParent,
        searchValue,
        assignResourceId,
        assignResourceCategory,
        basicTree,
        category,
        searchText,
        deptTreeList,
        originalDeptTreeList,
        // abilityPermissionFolderIdList,
      };
    },
    mounted() {
      // console.log('功能权限授权 ...');
    },
    methods: {
      onDrop(info: AntTreeNodeDropEvent) {
        const dropKey = info.node.eventKey;
        const dragKey = info.dragNode.eventKey;
        const dropPos = info.node.pos.split('-');
        const dropPosition = info.dropPosition - Number(dropPos[dropPos.length - 1]);
        const loop = (data: TreeDataItem[], id: string, callback: any) => {
          data.forEach((item, index, arr) => {
            if (item.id === id) {
              return callback(item, index, arr);
            }
            if (item.children) {
              return loop(item.children, id, callback);
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
      saveGranted() {
        /*let temp = this.abilityPermissionFolderIdList as Array<any>;
        function checkKey(key) {
          return !temp.includes(key);
        }*/
        const selectedIdList = this.checkedKeys;
        const params: SaveGrantedResponseModel = {
          assignResourceCategory: this.assignResourceCategory,
          assignResourceId: this.assignResourceId,
          abilityPermissionIdList: selectedIdList,
        };
        if (this.category) {
          this.$emit('saveGranted', {
            permittedResourceCategory: 'ABILITY_PERMISSION',
            permittedResourceIds: this.checkedKeys,
          });
          this.closeModal();
          return;
        }
        apiSaveAbilityPermissionAssign(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '保存授权成功',
              });
            } else {
              useMessage().createErrorNotification({
                message: '操作失败',
                description: '保存角色授权，请检查网络',
              });
            }
          })
          .catch(() => {
            useMessage().createErrorModal({
              title: '操作失败',
              content: '保存角色授权，请检查网络',
              closable: true,
              maskClosable: false,
              showOkBtn: true,
              showCancelBtn: false,
            });
          });
        this.closeModal();
      },
      handleCheck(e) {
        this.checkedKeys = e;
      },
      onSearch() {
        this.loading = true;
        const data = searchTree(this.searchValue, this.originalDeptTreeList);
        this.searchText = this.searchValue;
        this.treeData = data.treeData;
        this.expandedKeys = data.expandedKeys;
        this.loading = false;
      },
      // onSaveMenuSort() {
      //   const res = [];
      //   this.buildMenuTreeNewSortInfo(this.treeData[0].children, null, res);
      //   apiUpdateMenuSort(res).then((res) => {
      //     if (res.code === 200) {
      //       useMessage().notification.success({
      //         message: '保存成功',
      //         duration: 3,
      //       });
      //       setTimeout(() => {
      //         this.$router.go(0);
      //       }, 3000);
      //     } else {
      //       useMessage().createErrorModal({
      //         title: '提示',
      //         content: res.error.message,
      //       });
      //     }
      //   });
      // },
      // buildMenuTreeNewSortInfo(treeData, parentId, res) {
      //   treeData.map((t, idx) => {
      //     t.parent_id = parentId;
      //     t.seq = idx;
      //     res.push(t);
      //     if (t.children.length > 0) {
      //       this.buildMenuTreeNewSortInfo(t.children, t.id, res);
      //     }
      //   });
      // },
    },
  });
</script>

<style scoped lang="less">
  ::v-deep(.ant-modal-body) {
    .scrollbar {
      height: 70vh;
      padding: 0 20px !important;
    }
  }

  ::v-deep(.scroll-container .scrollbar__wrap) {
    margin-bottom: 0 !important;
  }
</style>
