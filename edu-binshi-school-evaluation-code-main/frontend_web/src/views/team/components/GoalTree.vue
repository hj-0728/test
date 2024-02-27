<template>
  <div class="goal-tree">
    <div style="height: 50px; padding: 5px 10px">
      <InputSearch v-model:value="searchValue" placeholder="搜索" enter-button @search="onSearch" />
    </div>
    <div style="padding: 0 0 0 8px; height: 100%">
      <BasicTree
        ref="goalTreeRef"
        :treeData="goalTreeList"
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
            <span v-if="node.disableCheckbox" style="margin-left: 25px; color: darkgrey">
              {{ node.name }}<span>(不可选，已被【{{ node.teamName }}】设为小组目标)</span></span
            >
            <span v-else style="margin-left: 25px">{{ node.name }}</span>
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
  import { apiGetTeamGoalTree } from '/@/api/team/team';
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
      checkedGoalKeys: {
        type: Array,
        default: () => [],
      },
      teamId: {
        type: String,
        default: '',
      },
      teamCategoryId: {
        type: String,
        default: '',
      },
    },
    setup() {
      const searchAfter = ref(false);
      const searchBefore: Ref<object[]> = ref([]);
      const checkedNodes: Ref<object[]> = ref([]);
      const loading = ref(false);
      const searchValue = ref();
      const goalTreeRef = ref();
      const goalTreeList = ref<object[]>([]);
      const originalGoalTreeList = ref<object[]>([]);
      const expandedKeys = ref<string[]>([]);
      const selectedKeys = ref([]);
      const checkedDeptKeys: Ref<string[]> = ref([]);

      return {
        checkedNodes,
        searchBefore,
        searchAfter,
        loading,
        searchValue,
        goalTreeRef,
        goalTreeList,
        originalGoalTreeList,
        expandedKeys,
        selectedKeys,
        checkedDeptKeys,
        organizationImg,
        schoolImg,
        periodImg,
        gradeImg,
        classImg,
      };
    },
    mounted() {
      this.searchAfter = false;
      this.getGoalTree();
      this.checkedNodes = [];
    },
    methods: {
      getGoalTree() {
        if (this.$props.teamCategoryId) {
          this.loading = true;
          apiGetTeamGoalTree({
            teamId: this.$props.teamId,
            teamCategoryId: this.$props.teamCategoryId,
          })
            .then((res) => {
              if (res.code === 200) {
                this.goalTreeList = res.data;
                this.originalGoalTreeList = res.data;
                this.checkedDeptKeys = this.$props.checkedGoalKeys as string[];
                this.checkedNodes = this.checkedDeptKeys.map((key) =>
                  this.getNode(this.goalTreeList, key),
                );
                this.$emit('onCheckGoal', this.checkedNodes);
                this.$nextTick(() => {
                  unref(this.goalTreeRef)?.expandAll(true);
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
        }
      },
      onExpand(keys, _event) {
        this.expandedKeys = keys;
      },
      onSelect(_selectedKeys, e) {
        this.$emit('onSelectGoal', { node: e.node });
      },
      getLeafNodes(node) {
        if (!node.children || node.children.length === 0) {
          return [node.key];
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
          const nodeKey = e.node.key;
          if (this.checkedDeptKeys.includes(nodeKey)) {
            this.checkedDeptKeys = this.checkedDeptKeys.filter((key) => key !== nodeKey);
          } else {
            this.checkedDeptKeys.push(nodeKey);
          }
        }

        const checkedNodes = this.checkedDeptKeys.map((key) =>
          this.getNode(this.originalGoalTreeList, key),
        );
        this.$emit('onCheckGoal', checkedNodes);
      },
      getNode(tree, id) {
        for (const node of tree) {
          if (node.key === id) {
            return {
              key: node.key,
              name: node.name,
              parentName: node.parentName,
              deptCategory: node.deptCategoryCode,
              disableCheckbox: node.disableCheckbox,
              teamName: node.teamName,
              children: node.children,
            };
          } else if (node.children) {
            const result = this.getNode(node.children, id);
            if (result) return result;
          }
        }
        return null;
      },
      onSearch() {
        this.searchAfter = true;
        this.loading = true;
        const data = searchTree(this.searchValue, this.originalGoalTreeList);
        this.goalTreeList = data.treeData;
        // this.expandedKeys = data.expandedKeys;
        if (this.checkedDeptKeys) {
          const checkedNodes = this.checkedDeptKeys.map((key) =>
            this.getNode(this.originalGoalTreeList, key),
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
  .goal-tree {
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
