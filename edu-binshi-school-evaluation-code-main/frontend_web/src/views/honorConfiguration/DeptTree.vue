<template>
  <div class="dept-tree">
    <div style="height: 16px"></div>
    <div style="height: 50px; padding: 8px">
      <InputSearch v-model:value="searchValue" placeholder="搜索" enter-button @search="onSearch" />
    </div>
    <div style="height: calc(100% - 68px); padding: 0 0 0 8px">
      <BasicTree
        ref="deptTreeRef"
        :treeData="deptTreeList"
        :clickRowToExpand="false"
        @select="onSelect"
        :selectedKeys="selectedKeys"
        :expandedKeys="expandedKeys"
        :loading="loading"
        @expand="onExpand"
        :delete-default-height="true"
      >
        <template #title="node">
          <div style="width: fit-content">
            <template v-if="node['deptCategoryCode']">
              <img
                :src="organizationImg"
                v-if="node['deptCategoryCode'] === 'ORGANIZATION'"
                class="icon"
              />
              <img :src="schoolImg" v-if="node['deptCategoryCode'] === 'CAMPUS'" class="icon" />
              <img :src="periodImg" v-if="node['deptCategoryCode'] === 'PERIOD'" class="icon" />
              <img :src="gradeImg" v-if="node['deptCategoryCode'] === 'GRADE'" class="icon" />
              <img :src="classImg" v-if="node['deptCategoryCode'] === 'CLASS'" class="icon" />
            </template>
            <template v-else>
              <img :src="organizationImg" v-if="node.level === 0" class="icon" />
              <img :src="schoolImg" v-if="node.level === 1" class="icon" />
              <img :src="periodImg" v-if="node.level === 2" class="icon" />
              <img :src="gradeImg" v-if="node.level === 3" class="icon" />
              <img :src="classImg" v-if="node.level === 4" class="icon" />
            </template>
            <span style="margin-left: 25px" v-if="node.name.indexOf(searchText) > -1">
              {{ node.name.substr(0, node.name.indexOf(searchText)) }}
              <span style="color: #f50">{{ searchText }}</span>
              {{ node.name.substr(node.name.indexOf(searchText) + searchText.length) }}
            </span>
            <span style="margin-left: 25px" v-else>{{ node.name }}</span>
          </div>
        </template>
      </BasicTree>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Input } from 'ant-design-vue';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { getAuthCache } from '/@/utils/auth';
  import { UserInfo } from '/#/store';
  import organizationImg from '/@/assets/icons/organization.svg';
  import schoolImg from '/@/assets/icons/school.svg';
  import periodImg from '/@/assets/icons/period.svg';
  import gradeImg from '/@/assets/icons/grade.png';
  import classImg from '/@/assets/icons/class.png';
  import { getDeptTreeData } from '/@/views/honorConfiguration/deptTree';

  export default defineComponent({
    components: {
      BasicTree,
      InputSearch: Input.Search,
    },
    props: {
      periodId: {
        type: String,
        default: '',
      },
    },
    setup(props) {
      const currentUserInfo: UserInfo = getAuthCache(USER_INFO_KEY);
      const currentRoleCode = currentUserInfo.currentRole?.code;
      const loading = ref(false);
      const searchValue = ref('');
      const searchText = ref('');
      const deptTreeRef = ref();
      const deptTreeList = ref<object[]>([]);
      const originalDeptTreeList = ref<object[]>([]);
      const expandedKeys = ref<string[]>([]);
      const selectedKeys = ref([]);
      const params = {
        getDutyTeacherDept: currentRoleCode === 'TEACHER',
      };
      const deptTreeData = getDeptTreeData(props.periodId);
      return {
        loading,
        searchValue,
        searchText,
        deptTreeRef,
        deptTreeList,
        originalDeptTreeList,
        expandedKeys,
        selectedKeys,
        params,
        organizationImg,
        schoolImg,
        periodImg,
        gradeImg,
        classImg,
        deptTreeData,
      };
    },
    mounted() {
      this.getDeptTree();
    },
    methods: {
      getDeptTree() {
        const resData = this.deptTreeData;
        this.deptTreeList = resData;
        this.originalDeptTreeList = resData;
        if (resData.length > 0) {
          const selectedKeys = [];
          selectedKeys.push(resData[0].key);
          this.selectedKeys = selectedKeys;
        }
        this.$nextTick(() => {
          unref(this.deptTreeRef)?.expandAll(true);
        });
      },
      onExpand(keys, _event) {
        this.expandedKeys = keys;
      },
      onSelect(_selectedKeys, e) {
        this.$emit('onSelectDept', { node: e.node });
      },
      onSearch() {
        this.loading = true;
        const data = searchTree(this.searchValue, this.originalDeptTreeList);
        this.searchText = this.searchValue;
        this.deptTreeList = data.treeData;
        this.expandedKeys = data.expandedKeys;
        this.loading = false;
      },
    },
  });
</script>

<style scoped lang="less">
  .dept-tree {
    height: 100%;

    ::v-deep(.vben-tree .ant-tree-node-content-wrapper .ant-tree-title) {
      // tree 横向滚动自适应
      width: fit-content;
    }

    ::v-deep(.ant-tree-title) {
      // tree 节点换行
      //position: relative !important;
      //white-space: normal !important;
    }

    .icon {
      width: 16px;
      height: 16px;
      position: absolute;
      top: 4px;
    }
  }
</style>
