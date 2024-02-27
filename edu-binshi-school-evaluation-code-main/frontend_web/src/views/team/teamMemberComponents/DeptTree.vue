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
              <img :src="dept1Img" v-if="node.level === 1" class="icon" />
              <img :src="dept2Img" v-if="node.level === 2" class="icon" />
              <img :src="dept3Img" v-if="node.level === 3" class="icon" />
              <img :src="dept4Img" v-if="node.level >= 4" class="icon" />
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
  import { defineComponent, ref, toRefs, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Input } from 'ant-design-vue';
  import { apiGetDeptTree } from '/@/api/dept/dept';
  import { useMessage } from '/@/hooks/web/useMessage';
  import organizationImg from '/@/assets/icons/organization.svg';
  import schoolImg from '/@/assets/icons/school.svg';
  import periodImg from '/@/assets/icons/period.svg';
  import gradeImg from '/@/assets/icons/grade.png';
  import classImg from '/@/assets/icons/class.png';
  import dept1Img from '/@/assets/icons/school.svg';
  import dept2Img from '/@/assets/icons/dept2.png';
  import dept3Img from '/@/assets/icons/dept3.png';
  import dept4Img from '/@/assets/icons/dept4.png';

  export default defineComponent({
    components: {
      BasicTree,
      InputSearch: Input.Search,
    },
    props: {
      dimensionCategory: {
        type: String,
        default: '',
      },
    },
    setup(props) {
      const loading = ref(false);
      const searchValue = ref('');
      const searchText = ref('');
      const deptTreeRef = ref();
      const deptTreeList = ref<object[]>([]);
      const originalDeptTreeList = ref<object[]>([]);
      const expandedKeys = ref<string[]>([]);
      const selectedKeys = ref([]);
      const { dimensionCategory } = toRefs(props);
      const dimensionCode = ref('DINGTALK_EDU');
      if (dimensionCategory.value === 'ADMINISTRATION') {
        dimensionCode.value = 'DINGTALK_INNER';
      }
      console.log('dimensionCategory.value ...', dimensionCategory.value);
      const params = {
        getDutyTeacherDept: false,
        dimensionCategory: props.dimensionCategory,
        dimensionCode: dimensionCode.value,
      };
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
        dept1Img,
        dept2Img,
        dept3Img,
        dept4Img,
      };
    },
    mounted() {
      this.getDeptTree();
    },
    methods: {
      getDeptTree() {
        apiGetDeptTree(this.params)
          .then((res) => {
            if (res.code === 200) {
              this.deptTreeList = res.data;
              this.originalDeptTreeList = res.data;
              console.log('this.deptTreeList ...');
              console.log(this.deptTreeList);
              if (res.data.length > 0) {
                const selectedKeys = [];
                selectedKeys.push(res.data[0].key);
                this.selectedKeys = selectedKeys;
              }
              this.$nextTick(() => {
                unref(this.deptTreeRef)?.expandAll(true);
              });
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误',
            });
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
    height: 67vh;

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
