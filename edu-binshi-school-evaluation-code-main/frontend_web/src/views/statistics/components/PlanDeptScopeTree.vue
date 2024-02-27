<template>
  <div class="dept-tree">
    <div style="height: 50px">
      <InputSearch v-model:value="searchValue" placeholder="搜索" enter-button @search="onSearch" />
    </div>
    <div style="padding: 0 0 0 8px; height: 100%">
      <BasicTree
        ref="deptTreeRef"
        :treeData="deptTreeList"
        :clickRowToExpand="false"
        @select="onSelect"
        @check="onCheck"
        :selectedKeys="selectedKeys"
        :expandedKeys="expandedKeys"
        :checkedKeys="checkedDeptKeys"
        :loading="loading"
        @expand="onExpand"
        :checkable="checkAble"
        :delete-default-height="true"
        :fieldNames="{ key: 'id' }"
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
            <span style="margin-left: 25px">{{ node.name }}</span>
          </div>
        </template>
      </BasicTree>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, Ref, ref, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Input } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiGetPlanRankingFilterDeptTree } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlanStatistics';
  import organizationImg from '/@/assets/icons/organization.svg';
  import schoolImg from '/@/assets/icons/school.svg';
  import periodImg from '/@/assets/icons/period.svg';
  import gradeImg from '/@/assets/icons/grade.png';
  import classImg from '/@/assets/icons/class.png';

  export default defineComponent({
    components: {
      BasicTree,
      InputSearch: Input.Search,
    },
    props: {
      checkAble: {
        type: Boolean,
        default: false,
      },
      checkedKeys: {
        type: Array,
        default: () => [],
      },
      planId: {
        type: String,
        default: null,
      },
    },
    setup(props) {
      const loading = ref(false);
      const searchValue = ref();
      const deptTreeRef = ref();
      const deptTreeList = ref<object[]>([]);
      const originalDeptTreeList = ref<object[]>([]);
      const expandedKeys = ref<string[]>([]);
      const selectedKeys = ref([]);
      const params = {
        evaluationCriteriaPlanId: props.planId,
      };
      const checkedDeptKeys: Ref<string[]> = ref([]);

      return {
        loading,
        searchValue,
        deptTreeRef,
        deptTreeList,
        originalDeptTreeList,
        expandedKeys,
        selectedKeys,
        params,
        checkedDeptKeys,
        organizationImg,
        schoolImg,
        periodImg,
        gradeImg,
        classImg,
      };
    },
    mounted() {
      this.getDeptTree();
    },
    methods: {
      getDeptTree() {
        this.loading = true;
        apiGetPlanRankingFilterDeptTree(this.params)
          .then((res) => {
            if (res.code === 200) {
              this.deptTreeList = res.data;
              this.originalDeptTreeList = res.data;
              this.checkedDeptKeys = this.$props.checkedKeys as string[];
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
          })
          .finally(() => {
            this.loading = false;
          });
      },
      onExpand(keys, _event) {
        this.expandedKeys = keys;
      },
      onSelect(_selectedKeys, e) {
        this.$emit('onSelectDept', { node: e.node });
      },
      getLeafNodes(node) {
        if (!node.children || node.children.length === 0) {
          return [node.id];
        }

        let leafNodesKeys = [];
        for (const childNode of node.children) {
          leafNodesKeys.push(...(this.getLeafNodes(childNode) as []));
        }

        return leafNodesKeys;
      },
      onCheck(_checkedKeys, e) {
        if (e.node.children.length) {
          const leafNodesKeys = this.getLeafNodes(e.node);
          for (const leafNodesKey of leafNodesKeys) {
            if (!e.node.checked && !this.checkedDeptKeys.includes(leafNodesKey)) {
              this.checkedDeptKeys.push(leafNodesKey);
            } else if (e.node.checked && this.checkedDeptKeys.includes(leafNodesKey)) {
              this.checkedDeptKeys = this.checkedDeptKeys.filter((key) => key !== leafNodesKey);
            }
          }
        } else {
          const nodeKey = e.node.id;
          if (this.checkedDeptKeys.includes(nodeKey)) {
            this.checkedDeptKeys = this.checkedDeptKeys.filter((key) => key !== nodeKey);
          } else {
            this.checkedDeptKeys.push(nodeKey);
          }
        }
        const checkedNodes = this.checkedDeptKeys.map((key) =>
          this.getNode(this.originalDeptTreeList, key),
        );
        this.$emit('onCheckDept', checkedNodes);
      },
      getNode(tree, id) {
        for (const node of tree) {
          if (node.id === id) {
            return { key: node.id, name: node.name, children: node.children };
          } else if (node.children) {
            const result = this.getNode(node.children, id);
            if (result) return result;
          }
        }
        return null;
      },
      onSearch() {
        this.loading = true;
        const data = searchTree(this.searchValue, this.originalDeptTreeList);
        this.deptTreeList = data.treeData;
        this.expandedKeys = data.expandedKeys;
        if (this.checkedDeptKeys) {
          const checkedNodes = this.checkedDeptKeys.map((key) =>
            this.getNode(this.originalDeptTreeList, key),
          );

          this.checkedDeptKeys = [];
          this.checkedDeptKeys = checkedNodes.map((node) => node.key);
          this.$emit('onCheckDept', checkedNodes);
        }
        this.loading = false;
      },
      getImageSource(node) {
        let srcPrefix = '/src/assets/icons/';
        let srcMap = {
          ORGANIZATION: 'organization.svg',
          CAMPUS: 'school.svg',
          PERIOD: 'period.svg',
          GRADE: 'grade.png',
          CLASS: 'class.png',
        };

        if (node['deptCategoryCode']) {
          return srcPrefix + srcMap[node['deptCategoryCode']];
        } else {
          let levelMap = ['organization.svg', 'school.svg', 'period.svg', 'grade.png', 'class.png'];
          return srcPrefix + levelMap[node.level];
        }
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

    .icon {
      width: 16px;
      height: 16px;
      position: absolute;
      top: 4px;
    }
  }
</style>
