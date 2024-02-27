<template>
  <div class="dept-tree">
    <!--    <Loading :loading="fullScreenLoading" :absolute="false" />-->
    <Row>
      <Col :span="4" />
      <Col :span="16">
        <div class="evaluation-criteria-name">
          <span>{{ evaluationCriteria?.name }}</span>
        </div>
      </Col>
      <Col :span="4" class="tree-title-operate">
        <Button
          color="edit"
          type="primary"
          @click="toAdd()"
          class="add-operate-button"
          v-if="evaluationCriteria?.status !== 'ABOLISHED'"
        >
          <template #icon> <SvgIcon name="ruleAddWhite" size="26" /></template>
          添加评价项
        </Button>
      </Col>
    </Row>

    <!--    <div style="height: 50px; padding: 8px">-->
    <!--      <InputSearch-->
    <!--        v-model:value="searchValue"-->
    <!--        placeholder="搜索"-->
    <!--        enter-button-->
    <!--        @search="onSearch"-->
    <!--        style="width: 30%"-->
    <!--      />-->
    <!--    </div>-->
    <!--    <Skeleton :loading="loading">-->
    <div style="height: calc(100% - 68px)">
      <img
        src="../../assets/svg/treeEmpty.svg"
        width="300"
        v-if="evaluationCriteriaTreeList.length === 0 && !loading"
        style="margin: 0 auto"
      />
      <BasicTree
        v-else
        ref="evaluationCriteriaTreeRef"
        :treeData="evaluationCriteriaTreeList"
        :clickRowToExpand="true"
        @select="onSelect"
        :selectedKeys="selectedKeys"
        :expandedKeys="expandedKeys"
        :loading="loading"
        :draggable="true"
        :selectable="false"
        @expand="onExpand"
        :delete-default-height="true"
        @dragenter="onDragEnter"
        @drop="onDrop"
      >
        <template #title="node">
          <div class="tree-title-wrapper">
            <div :class="['tree-title', 'inline-flex-center', 'tree-title-' + node.level]">
              <div class="tree-node-content inline-flex-center">
                <!--                <SvgIcon name="standard"/>-->
                <div class="node-name" :style="{ width: getNodeNameWidth(node.level) }"
                  ><Icon icon="ph:ruler-bold" color="#58a76e" style="margin-right: 5px" />
                  <span class="node-name-span">{{ node.name }} </span>
                  <span class="node-edit-button" >
                    <Button
                      v-if="evaluationCriteria?.status !== 'ABOLISHED'"
                      shape="round"
                      size="small"
                      style="margin: 5px"
                      @click.stop="toAdd(node)"

                    >
                      <template #icon><SvgIcon name="ruleAdd" size="16" /> </template>
                    </Button>
                    <Button
                      shape="round"
                      size="small"
                      style="margin: 5px"
                      @click.stop="toEdit(node)"
                    >
                      <template #icon
                        ><Icon v-if="evaluationCriteria?.status !== 'ABOLISHED'" icon="ant-design:edit-twotone" color="#0960bd"
                      /><Icon v-else icon="mdi:eye-outline" color="#0960bd"
                      />
                      </template>
                    </Button>
                    <Button
                      v-if="evaluationCriteria?.status !== 'ABOLISHED'"
                      shape="round"
                      size="small"
                      style="margin: 5px"
                      @click.stop="toDelete(node)"
                    >
                      <template #icon
                        ><Icon icon="material-symbols:delete-outline" color="#ff4d4f"
                      /></template>
                    </Button>
                  </span>
                </div>
                <div class="benchmark-div inline-flex-center">
                  <div
                    v-if="evaluationCriteria?.status !== 'ABOLISHED'"
                    class="benchmark-edit-span inline-flex-center"
                    @click.stop="clickOpenEditBenchmarkModal(node, 'ADD')"
                  >
                    <Tag color="success" class="benchmark-edit-button benchmark-tag">
                      <PlusCircleOutlined />
                    </Tag>
                  </div>
                  <div
                    class="benchmark-edit-span inline-flex-center"
                    v-for="benchmark in node.benchmarkList"
                    @click.stop="clickOpenEditBenchmarkModal(node, 'EDIT', benchmark)"
                  >
                    <Tag
                      :color="benchmarkStrategy[benchmark.benchmarkStrategyCode]"
                      class="benchmark-tag"
                      >{{ benchmark.name }}
                      <span class="benchmark-delete-icon" v-if="evaluationCriteria?.status !== 'ABOLISHED'" @click.stop="toDeleteBenchmark(benchmark)"
                        ><CloseOutlined
                      /></span>
                    </Tag>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </BasicTree>
    </div>
    <!--    </Skeleton>-->
    <EditEvaluationCriteriaTreeModal @register="register" @save-success="saveSuccess" />
    <EditBenchmarkModal @register="registerEditBenchmarkModal" @save-success="saveSuccess" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Button, Tag, Row, Col } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { getAuthCache } from '/@/utils/auth';
  import { UserInfo } from '/#/store';
  import {
    apiDeleteEvaluationCriteriaTree,
    apiGetEvaluationCriteriaTree,
    apiUpdateEvaluationCriteriaTreeSeq,
  } from '/@/api/evaluationCriteriaTree/evaluationCriteriaTree';
  import { Icon, SvgIcon } from '/@/components/Icon';
  import EditEvaluationCriteriaTreeModal from '/@/views/evaluationCriteriaTree/EditEvaluationCriteriaTreeModal.vue';
  import { useModal } from '/@/components/Modal';
  // import { Loading } from '/@/components/Loading';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { cloneDeep } from 'lodash-es';
  import { apiGetEvaluationCriteriaDetail } from '/@/api/evaluationCriteria/evaluationCriteria';
  import EditBenchmarkModal from '/@/views/evaluationCriteriaTree/components/EditBenchmarkModal.vue';
  import { CloseOutlined, PlusCircleOutlined } from '@ant-design/icons-vue';
  import { apiDeleteBenchmark } from '/@/api/benchmark/benchmark';
  export default defineComponent({
    components: {
      BasicTree,
      Icon,
      EditEvaluationCriteriaTreeModal,
      // Loading,
      SvgIcon,
      EditBenchmarkModal,
      PlusCircleOutlined,
      Button,
      Tag,
      Row,
      Col,
      CloseOutlined,
    },
    emits: ['onSelectEvaluationCriteriaTreeNode', 'getEvaluationCriteria'],
    setup() {
      const [register, { openModal }] = useModal();
      const [registerEditBenchmarkModal, { openModal: openEditBenchmarkModal }] = useModal();
      const currentUserInfo: UserInfo = getAuthCache(USER_INFO_KEY);
      const currentRoleCode = currentUserInfo.currentRole?.code;
      const loading = ref(false);
      const searchValue = ref('');
      const evaluationCriteria = ref();
      const evaluationCriteriaTreeRef = ref();
      const evaluationCriteriaTreeList = ref<object[]>([]);
      const originalEvaluationCriteriaTreeList = ref<object[]>([]);
      const expandedKeys = ref<string[]>([]);
      const selectedKeys = ref([]);
      const params = {
        getDutyTeacherDept: currentRoleCode === 'TEACHER',
      };
      const refreshKey = ref();
      const hoveredNodeKey = ref();

      const titleColor = ['#5248DD', '#427AF7', '#6498F8', '#86B5F8', '#A8D3F8', '#CAF0F8'];
      const benchmarkStrategy = {
        // 本人
        SELF: '#E48586',
        // 小组
        ONLY_ONE_TEAM_CATEGORY: '#FCBAAD',
        // 班主任
        ONLY_ONE_HEAD_TEACHER: '#916DB3',
        // 同班同学-固定人数参数
        CLASSMATES_FIXED_NUMBER: '#7895CB',
        // 一种科目的任课老师参与
        ONLY_ONE_TEACHER: '#D8BBFF',
        // 子级分值聚合
        SUB_LEVEL_AGGREGATED: '#54C2FF',
        // 子级分值聚合
        SAME_LEVEL_AGGREGATED: '#F0B86E',
        // 等级
        GRADE: '#A8DF8E',
      };
      const getNodeNameWidth = (level) => {
        const baseIndent = 24;
        return `calc(45vw - ${level - 1} * ${baseIndent}px)`;
      };
      const getTreeTitleStyles = (node) => {
        const color =
          node.level <= titleColor.length
            ? titleColor[node.level - 1]
            : titleColor[titleColor.length];
        let style = {
          borderLeftColor: color,
        };
        if (hoveredNodeKey.value === node.key) {
          style.background = color;
          style.color = 'white';
        }
        return style;
      };
      return {
        register,
        openModal,
        registerEditBenchmarkModal,
        openEditBenchmarkModal,
        loading,
        searchValue,
        evaluationCriteriaTreeRef,
        evaluationCriteriaTreeList,
        originalEvaluationCriteriaTreeList,
        expandedKeys,
        selectedKeys,
        params,
        evaluationCriteria,
        refreshKey,
        getNodeNameWidth,
        getTreeTitleStyles,
        hoveredNodeKey,
        benchmarkStrategy,
      };
    },
    mounted() {
      this.getEvaluationCriteriaDetail();
      this.getEvaluationCriteriaTree();
    },
    methods: {
      getEvaluationCriteriaDetail() {
        apiGetEvaluationCriteriaDetail(this.$route.params.evaluationCriteriaId)
          .then((res) => {
            if (res.code === 200) {
              this.evaluationCriteria = res.data;
              this.$emit('getEvaluationCriteria', res.data);
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((error) => {
            console.log(error);
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {});
      },
      onDragEnter(e) {
        // console.log('on drag enter e ...');
        // console.log(e);
      },
      onDrop(e) {
        if (this.evaluationCriteria?.status === 'ABOLISHED') {
          useMessage().createErrorNotification({
            message: '提示',
            description: '评价标准已废弃，不可修改评价项。',
          });
          return;
        }
        const dragNode = e.dragNode;
        let node = e.node;
        const dropPos = e.node.pos.split('-');
        const position = e.dropPosition - Number(dropPos[dropPos.length - 1]);
        console.log(e);
        console.log(position);
        if ((!e.dropToGap || position === 0) && node.indicatorId !== dragNode.parentIndicatorId) {
          useMessage().createErrorNotification({
            message: '提示',
            description: '不可跨父节点排序',
          });
          return;
        }
        // 非根节点的移到顶部
        if (node.level !== dragNode.level || !node.parentIndicatorId) {
          node = { seq: 0 };
        }
        this.handleDrag(dragNode, node, position);
      },
      getParentNode(data, node) {
        for (const item of data) {
          if (item['indicatorId'] === node.parentIndicatorId) {
            return item;
          }
          if (item.children && item.children.length > 0) {
            const parent = this.getParentNode(item.children, node);
            if (parent) {
              return parent;
            }
          }
        }
        return null;
      },
      handleDrag(dragNode, node, position) {
        const parentNode = this.getParentNode(this.originalEvaluationCriteriaTreeList, dragNode);
        let children = parentNode?.children;
        if (!parentNode) {
          children = this.originalEvaluationCriteriaTreeList;
        }
        const newChildren = cloneDeep(children);
        let newDragSeq = cloneDeep(node.seq);
        let message = `是否将【<text style="color: #00acc1">${dragNode.name}</text>】移动到`;
        console.log(newChildren);
        for (const child of newChildren) {
          console.log(`seq: ${dragNode.seq}/${child.seq}/${node.seq}}`);
          if (child.seq > node.seq && child.seq < dragNode.seq) {
            child.seq++;
          } else if (dragNode.seq < child.seq && child.seq <= node.seq) {
            child.seq--;
          }
          if (child.indicatorId === dragNode.indicatorId) {
            if (child.seq > node.seq) {
              newDragSeq++;
            }
            child.seq = newDragSeq;
          }
        }
        if (node.name && position !== -1) {
          message += `【<text style="color: #00acc1">${node.name}</text>】之<text style="color: #ff0000; font-weight: bold">后</text>？`;
        } else {
          message += `<text style="color: #ff0000; font-weight: bold">顶部</text>？`;
        }
        console.log(newChildren);
        this.toUpdateSeq(newChildren, message);
      },
      toUpdateSeq(updateSeqList, message) {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: message,
          onOk: () => {
            this.doUpdateSeq(updateSeqList);
          },
          onCancel() {},
        });
      },
      doUpdateSeq(updateSeqList) {
        const params = {
          updateSeqList: updateSeqList,
          parentIndicatorId: updateSeqList[0].parentIndicatorId,
        };
        this.loading = true;
        apiUpdateEvaluationCriteriaTreeSeq(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '更新排序成功',
              });
              this.getEvaluationCriteriaTree();
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
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
      onContextMenuClick(node, menuKey) {
        delete node.title;
        if (menuKey === 'ADD') {
          this.toAdd(node);
        } else if (menuKey === 'EDIT') {
          this.toEdit(node);
        } else {
          this.toDelete(node);
        }
      },
      toAdd(node) {
        this.refreshKey = new Date().getTime();
        this.openModal(true, {
          modalCategory: 'ADD',
          evaluationCriteriaTreeNode: node,
        });
      },
      toEdit(node) {
        this.refreshKey = new Date().getTime();
        this.openModal(true, {
          modalCategory: 'EDIT',
          evaluationCriteriaTreeNode: node,
          readonly: this.evaluationCriteria?.status === 'ABOLISHED',
        });
      },
      getEvaluationCriteriaTreeChildren(node) {
        const children: object[] = [];
        if (node?.title) {
          delete node.title;
        }
        children.push(node);
        for (const child of node?.children) {
          if (child?.title) {
            delete child.title;
          }
          children.push(...this.getEvaluationCriteriaTreeChildren(child));
        }
        return children;
      },
      toDelete(node) {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: `确定要<text style="color: #f00; font-weight: bold">删除</text>【<text style="color: #00acc1">${
            node.name
          }】${node.hasMetricUnit ? '' : '及其子节点'}</text>吗？`,
          onOk: () => {
            this.doDelete(node);
          },
          onCancel() {},
        });
      },
      toDeleteBenchmark(benchmark) {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: `确定要<text style="color: #f00; font-weight: bold">删除评价分类</text>【<text style="color: #00acc1">${benchmark.name}】</text>吗？`,
          onOk: () => {
            this.doDeleteBenchmark(benchmark);
          },
          onCancel() {},
        });
      },
      doDelete(node) {
        const params = {
          indicatorId: node.indicatorId,
          evaluationCriteriaId: this.$route.params.evaluationCriteriaId,
          deleteList: this.getEvaluationCriteriaTreeChildren(node),
        };
        apiDeleteEvaluationCriteriaTree(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '删除成功',
              });
              this.getEvaluationCriteriaTree();
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
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {
            // this.loading = false;
          });
      },
      doDeleteBenchmark(benchmark) {
        const params = {
          benchmarkId: benchmark.id,
          benchmarkVersion: benchmark.version,
        };
        apiDeleteBenchmark(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '删除成功',
              });
              this.getEvaluationCriteriaTree();
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
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {
            // this.loading = false;
          });
      },
      saveSuccess() {
        this.getEvaluationCriteriaTree();
      },
      getEvaluationCriteriaTree() {
        this.loading = true;
        apiGetEvaluationCriteriaTree(this.$route.params.evaluationCriteriaId)
          .then((res) => {
            if (res.code === 200) {
              this.evaluationCriteriaTreeList = res.data;
              this.originalEvaluationCriteriaTreeList = res.data;
              this.$nextTick(() => {
                if (this.expandedKeys.length === 0) {
                  unref(this.evaluationCriteriaTreeRef)?.expandAll(true);
                }
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
        this.$emit('onSelectEvaluationCriteriaTreeNode', { node: e.node });
      },
      onSearch() {
        this.loading = true;
        const data = searchTree(this.searchValue, this.originalEvaluationCriteriaTreeList);
        this.evaluationCriteriaTreeList = data.treeData;
        this.expandedKeys = data.expandedKeys;
        this.loading = false;
      },
      clickOpenEditBenchmarkModal(node, modalCategory, benchmark) {
        this.openEditBenchmarkModal(true, {
          modalCategory: modalCategory,
          evaluationCriteriaTreeNode: node,
          benchmark: benchmark,
          readonly: this.evaluationCriteria?.status === 'ABOLISHED',
        });
      },
    },
  });
</script>

<style scoped lang="less">
  .dept-tree {
    height: 100%;

    ::v-deep(.vben-tree .ant-tree-node-content-wrapper .ant-tree-title) {
      // tree 横向滚动自适应
      width: 100%;
    }

    ::v-deep(.ant-tree-title) {
      // tree 节点换行
      position: relative !important;
      //white-space: normal !important;
    }
    ::v-deep(.ant-tree-list) {
      padding: 5px 4% 50px 2.5%;
    }
    ::v-deep(.ant-tree-treenode) {
      padding: 5px 0;
    }
  }
  .node-edit-button {
    display: none;
    padding-left: 20px;
  }
  .tree-title-wrapper {
    position: relative;
    width: 100%; /* 根据需要调整 */
    min-height: 40px;
    padding: 5px;
  }
  //本来应该动态计算样式的，但是频繁操作DOM计算页面开销大容易卡顿
  .tree-title {
    width: 100%;
    //height: 100%;
    height: auto;
    //border: 1px solid #f7f7f9;
    //padding: 5px;
    background: #f7f7f9;
    border-radius: 8px;
    border-left-width: 10px;
    position: absolute;
    top: 0;
    left: 0;
    transition: transform 0.3s, box-shadow 0.3s;
    z-index: 1;
    overflow: hidden;
  }
  //const titleColor = ['#5248DD', '#427AF7', '#6498F8', '#86B5F8', '#A8D3F8', '#CAF0F8'];
  .tree-title-1 {
    border-left-color: #5248dd;
  }
  .tree-title-1:hover {
    border-left-color: #5248dd;
    background: #5248dd;
  }
  .tree-title-2 {
    border-left-color: #427af7;
  }
  .tree-title-2:hover {
    border-left-color: #427af7;
    background: #427af7;
  }
  //从左到右填充背景的样式 先留着
  //.tree-title-2::before {
  //  content: '';
  //  position: absolute;
  //  top: 0;
  //  left: 0;
  //  right: 100%; /* This ensures it starts from the left edge */
  //  bottom: 0;
  //  background: #427af7;
  //  z-index: -1; /* To keep it behind the content */
  //  transition: right 0.5s; /* This creates the animation effect */
  //}
  //
  //.tree-title-2:hover::before {
  //  right: 0; /* This fills the background color from left to right */
  //}
  .tree-title-3 {
    border-left-color: #6498f8;
  }
  .tree-title-3:hover {
    border-left-color: #6498f8;
    background: #6498f8;
  }
  .tree-title-4 {
    border-left-color: #86b5f8;
  }
  .tree-title-4:hover {
    border-left-color: #86b5f8;
    background: #86b5f8;
  }
  .tree-title-5 {
    border-left-color: #a8d3f8;
  }
  .tree-title-5:hover {
    border-left-color: #a8d3f8;
    background: #a8d3f8;
  }
  .tree-title-6 {
    border-left-color: #caf0f8;
  }
  .tree-title-6:hover {
    border-left-color: #caf0f8;
    background: #caf0f8;
  }
  .tree-title:hover {
    color: white;
    transform: scale(1.1);
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);
    height: auto;
    z-index: 99;
  }
  .benchmark-name:hover {
    //color: white;
    transform: scale(1.2);
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);
  }
  .benchmark-tag:hover {
    //color: white;
    transform: scale(1.2);
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);
  }

  .tree-title:hover .node-edit-button {
    display: inline-block;
    padding-left: 20px;
    min-width: 200px;
  }

  .tree-title:hover .node-name-span {
    height: auto;
    display: -webkit-box !important;
    -webkit-box-orient: vertical !important;
    -webkit-line-clamp: 2 !important;
    white-space: normal;
  }
  .benchmark-edit-button {
    display: none;
  }
  .tree-title:hover .benchmark-edit-button {
    display: inline-block;
  }
  .benchmark-delete-icon {
    display: none;
  }
  .tree-title:hover .benchmark-delete-icon {
    display: inline-block;
  }
  .node-name {
    display: inline-flex;
    margin: 0 10px 0 0;
    width: 400px;
    height: 100%;
    align-items: center;
    white-space: pre-wrap;
  }
  .node-name-span {
    margin: 10px 0;
    height: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .benchmark-name {
    margin-right: 10px;
  }
  .benchmark-tag {
    margin: 3px 5px;
  }
  .evaluation-criteria-name {
    height: 60px;
    font-weight: bolder;
    font-size: 24px;
    width: 100%;
    align-items: center;
    display: flex;
    justify-content: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .tree-title-operate {
    display: flex;
    align-items: center;
    justify-content: right;
    padding: 0 10px;
  }
  .add-operate-button {
    background: #3661ea;
    border-color: #3661ea;
  }
  .benchmark-edit-span {
    height: 100%;
  }
  .benchmark-div {
    height: 100%;
  }
  .tree-title:hover .benchmark-div {
    flex-wrap: wrap;
  }
  .full-height {
    height: 100%;
  }
  .tree-node-content {
    margin-left: 5px;
    height: 100%;
  }
</style>
