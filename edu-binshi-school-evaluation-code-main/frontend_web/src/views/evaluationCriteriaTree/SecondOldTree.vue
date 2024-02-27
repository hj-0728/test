<template>
  <div class="dept-tree">
    <!--    <Loading :loading="fullScreenLoading" :absolute="false" />-->
    <Row>
      <Col :span="7">

<!--        <div v-for="item in Object.keys(benchmarkStrategySourceCategory)">-->
<!--          <SoftTag-->

<!--            :color="benchmarkStrategySourceCategory[item].color"-->
<!--            :backgroundColor="benchmarkStrategySourceCategory[item].backgroundColor"-->
<!--            class="benchmark-tag translate-and-shadow"-->
<!--            >{{ benchmarkStrategySourceCategory[item].name }}-->
<!--          </SoftTag>-->
<!--        </div>-->
      </Col>
      <Col :span="10">
        <Tooltip>
          <template #title>{{ evaluationCriteria?.name }}</template>
          <div class="evaluation-criteria-name">
            <span class="evaluation-criteria-span">
              {{ evaluationCriteria?.name }}
            </span>
          </div>
        </Tooltip>
      </Col>
      <Col :span="7" class="tree-title-operate">
        <Button
          color="edit"
          type="primary"
          @click="toAdd()"
          class="add-operate-button"
          v-if="evaluationCriteria?.status !== 'ABOLISHED'"
          style="background: #5248dd"
        >
          <template #icon> <SvgIcon name="ruleAddWhite" size="20" /></template>
          添加第一级评价项
        </Button>

        <Button
          color="edit"
          type="primary"
          @click="bindTag()"
          class="ant-btn-left-margin"
          v-if="evaluationCriteria?.status !== 'ABOLISHED'"
        >
          <template #icon>
            <Icon icon="material-symbols:carpenter-outline-sharp" size="16"
          /></template>
          绑定标签
        </Button>
        <Popover title="评价项引导">
          <template #content>
            1
          </template>
          <SvgIcon name="question" size="24" style="margin: 5px" />
        </Popover>
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
    <div style="height: calc(100% - 68px); overflow: hidden">
      <img
        src="../../assets/svg/treeEmpty.svg"
        width="300"
        v-if="evaluationCriteriaTreeList.length === 0 && !loading"
        style="margin: 0 auto"
      />
      <Tree
        v-else-if="evaluationCriteriaTreeList?.length > 0"
        ref="evaluationCriteriaTreeRef"
        :treeData="evaluationCriteriaTreeList"
        :clickRowToExpand="true"
        @select="onSelect"
        :selectedKeys="selectedKeys"
        :loading="loading"
        :draggable="true"
        :selectable="false"
        :show-line="true"
        @expand="onExpand"
        :delete-default-height="true"
        :defaultExpandAll="true"
        @dragenter="onDragEnter"
        @drop="onDrop"
        style="overflow-x: scroll; white-space: no-wrap"
      >
        <template #switcherIcon="{ children, switcherCls, data }">
<!--          <Icon-->
<!--            icon="material-symbols:arrow-drop-down-circle"-->
<!--            :color="titleColor[data.level <= 6 ? data.level - 1 : 5]"-->
<!--            :class="[switcherCls]"-->
<!--            style="margin-right: 5px"-->
<!--            v-if="children.length > 0"-->
<!--          />-->
<DownCircleTwoTone :two-tone-color="titleColor[data.level <= 6 ? data.level - 1 : 5]" :class="[switcherCls]"
            style="margin-right: 8px; justify-content: center; align-items: center;margin-left: 2px;font-size: 14px;"
            v-if="children.length > 0" />
        </template>
        <template #title="node">
<!--          <DownCircleTwoTone :color="titleColor[node.level <= 6 ? node.level - 1 : 5]"-->
<!--            style="margin-right: 8px; justify-content: center; align-items: center"-->
<!--            v-if="node.children.length === 0"/>-->
<!--          <Icon-->
<!--            icon="ic:outline-circle"-->
<!--            :color="titleColor[node.level <= 6 ? node.level - 1 : 5]"-->
<!--            style="margin-right: 8px; justify-content: center; align-items: center"-->
<!--            v-if="node.children.length === 0"-->
<!--          />-->
          <div class="tree-title-wrapper">
            <div
              :class="[
                'tree-title',
                selectedKeys.includes(node.key) ? 'tree-title-selected' : '',
                'inline-flex-center',
                'tree-title-' + node.level,
              ]"
            >
              <!--              <div class="eye-icon">-->
              <!--              <Icon icon="ic:round-remove-red-eye" color="#ffffff" size="12"/>-->
              <!--              </div>-->
              <!--                <SvgIcon name="standard"/>-->
              <div class="node-name"
                >

                <SvgIcon name="xIcon" v-if="node.tag === 'X（变量）'" />
                <SvgIcon name="nIcon" v-else-if="node.tag === 'N（常量）'" />
                <Icon v-else icon="ph:ruler-bold" color="#58a76e" />
                <span class="node-name-span">{{ node.name }} </span>
              </div>
              <div class="benchmark-div inline-flex-center">
                <Icon icon="material-symbols:label-outline" color="#aeaeaf" />
                <div
                  class="benchmark-edit-span inline-flex-center"
                  v-for="benchmark in node.benchmarkList"
                  @click.stop="clickOpenEditBenchmarkModal(node, 'EDIT', benchmark)"
                >
                  <SoftTag
                    :color="benchmarkStrategySourceCategory[benchmark.sourceCategory].color"
                    :backgroundColor="
                      benchmarkStrategySourceCategory[benchmark.sourceCategory].backgroundColor
                    "
                    class="benchmark-tag translate-and-shadow"
                    >{{ benchmark.name }}
                  </SoftTag>
                </div>
                <div
                  v-if="evaluationCriteria?.status !== 'ABOLISHED'"
                  class="benchmark-edit-span benchmark-edit-button inline-flex-center translate-and-shadow"
                  @click.stop="clickOpenEditBenchmarkModal(node, 'ADD')"
                >
                  <Icon icon="material-symbols:add" /><span>添加评价分类</span>
                </div>
              </div>
              <Icon
                v-if="evaluationCriteria?.status === 'ABOLISHED'"
                icon="mdi:eye-outline"
                color="#80ce8d"
                style="margin-left: 10px"
                @click.stop="toEdit(node)"
              />
              <Dropdown :trigger="['focus', 'click']" :autoAdjustOverflow="true">
                <Icon
                  v-if="evaluationCriteria?.status !== 'ABOLISHED'"
                  icon="ri:more-2-fill"
                  color="#777777"
                  style="margin-left: 10px"
                  @click.stop
                  class="more-icon translate-with-no-shadow"
                />
                <template #overlay>
                  <Menu>
                    <MenuItem @click.stop="toAdd(node)">
                      <SvgIcon name="ruleAdd" size="16" style="margin-right: 5px" /> 添加子级评价项
                    </MenuItem>
                    <MenuItem @click.stop="toEdit(node)">
                      <Icon
                        icon="ant-design:edit-twotone"
                        color="#0960bd"
                        style="margin-right: 5px"
                      />
                      编辑此评价项
                    </MenuItem>
                    <MenuItem @click.stop="toDelete(node)"
                      ><Icon
                        icon="material-symbols:delete-outline"
                        color="#ff4d4f"
                        style="margin-right: 5px"
                      />
                      删除此评价项
                    </MenuItem>
                  </Menu>
                  <span class="node-edit-button"> </span>
                </template>
              </Dropdown>
            </div>
          </div>
        </template>
      </Tree>
    </div>
    <!--    </Skeleton>-->
  </div>
  <EditEvaluationCriteriaTreeModal @register="register" @save-success="saveSuccess" />
  <EditBenchmarkModal @register="registerEditBenchmarkModal" @save-success="saveSuccess" />
  <BindTagModal @register="registerBindTagModal" @save-success="saveSuccess" />
</template>

<script lang="ts">
  import { defineComponent, ref, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Button, Row, Col, Dropdown, Menu, Tree, Tooltip, Popover } from 'ant-design-vue';
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
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { cloneDeep } from 'lodash-es';
  import { apiGetEvaluationCriteriaDetail } from '/@/api/evaluationCriteria/evaluationCriteria';
  import EditBenchmarkModal from '/@/views/evaluationCriteriaTree/components/EditBenchmarkModal.vue';
  import { SoftTag } from '/@/components/Tag';
  import { benchmarkStrategySourceCategory } from '/@/utils/helper/common';
  import BindTagModal from '/@/views/evaluationCriteriaTree/bindTagComponents/BindTagModal.vue';
  import {DownCircleTwoTone, DownOutlined} from '@ant-design/icons-vue';
  export default defineComponent({
    components: {
      BasicTree,
      Icon,
      EditEvaluationCriteriaTreeModal,
      // Loading,
      SvgIcon,
      EditBenchmarkModal,
      Button,
      SoftTag,
      Row,
      Col,
      Dropdown,
      Menu,
      MenuItem: Menu.Item,
      BindTagModal,
      DownOutlined,
      Tree,
      Tooltip,
      DownCircleTwoTone,
      Popover,
    },
    emits: ['onSelectEvaluationCriteriaTreeNode', 'getEvaluationCriteria'],
    setup() {
      const [register, { openModal }] = useModal();
      const [registerBindTagModal, { openModal: openBindTagModal }] = useModal();
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

      const titleColor = ['#5248DD', '#4A61EA', '#427AF7', '#6498F8', '#86B5F8', '#A8D3F8'];
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
        openBindTagModal,
        registerBindTagModal,
        benchmarkStrategySourceCategory,
        titleColor,
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
          content: `确定要<text style="color: #cc563d; font-weight: bold">删除</text>【<text>${
            node.name
          }</text>】评价项<text>${
            node.hasMetricUnit ? '' : '、其所有子节点以及评价项相关的评价分类'
          }</text>吗？`,
          onOk: () => {
            this.doDelete(node);
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
                this.expandedKeys = []
                this.evaluationCriteriaTreeList.forEach((item)=>{
                  this.expandedKeys.push(item.key)
                })
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
        this.selectedKeys = _selectedKeys;
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
      bindTag() {
        this.openBindTagModal(true, {
          evaluationCriteriaId: this.$route.params.evaluationCriteriaId,
        });
      },
    },
  });
</script>

<style scoped lang="less">
  @keyframes animated-border {
    0% {
      box-shadow: 0 0 0 0 rgba(82, 72, 221, 0.4);
    }
    100% {
      box-shadow: 0 0 0 10px rgba(255, 255, 255, 0);
    }
  }
  .dept-tree {
    height: 100%;
    width: 100%;
    ::v-deep(.vben-tree .ant-tree-node-content-wrapper) {
      // tree 横向滚动自适应
      //width: fit-content;
      //flex: 0 0 auto;
    }
    ::v-deep(.scrollbar__view) {
      height: 100%;
    }

    ::v-deep(.ant-tree) {
      height: 100%;
    }

    ::v-deep(.ant-tree-title) {
      // tree 节点换行
      position: relative !important;
      display: flex;
      //white-space: normal !important;
    }

    ::v-deep(.ant-tree-switcher) {
      align-items: center;
      display: inline-flex;
      justify-content: flex-end;
    }

    ::v-deep(.ant-tree-treenode.dragging::after) {
      border: none !important;
    }
    ::v-deep(.ant-tree-node-content-wrapper:hover) {
      background-color: white;
    }
    ::v-deep(.ant-tree-list) {
      height: 100%;
      padding: 5px 4% 50px 2.5%;
    }
    //::v-deep(.ant-tree-node-selected) {
    //  //padding: 0;
    //  background: white;
    //}
    //::v-deep(.ant-tree-node-selected .tree-title) {
    //  border-left-width: 8px;
    //  box-shadow: 0 0 0 1px #a8d3f8;
    //}
    //::v-deep(.ant-tree-node-selected .tree-title-1) {
    //  box-shadow: 0 0 0 1px #5248dd;
    //}
    //::v-deep(.ant-tree-node-selected .tree-title-2) {
    //  box-shadow: 0 0 0 1px #4a61ea;
    //}
    //::v-deep(.ant-tree-node-selected .tree-title-3) {
    //  box-shadow: 0 0 0 1px #427af7;
    //}
    //::v-deep(.ant-tree-node-selected .tree-title-4) {
    //  box-shadow: 0 0 0 1px #6498f8;
    //}
    //::v-deep(.ant-tree-node-selected .tree-title-5) {
    //  box-shadow: 0 0 0 1px #86b5f8;
    //}
    //::v-deep(.ant-tree-node-selected .tree-title-6) {
    //  box-shadow: 0 0 0 1px #a8d3f8;
    //}
    ::v-deep(.tree-title:hover) {
      border-left-width: 8px;
      box-shadow: 0 0 0 1px #a8d3f8;
    }
    ::v-deep(.tree-title-1:hover ) {
      box-shadow: 0 0 0 1px #5248dd;
    }
    ::v-deep(.tree-title-2:hover) {
      box-shadow: 0 0 0 1px #4a61ea;
    }
    ::v-deep(.tree-title-3:hover) {
      box-shadow: 0 0 0 1px #427af7;
    }
    ::v-deep(.tree-title-4:hover) {
      box-shadow: 0 0 0 1px #6498f8;
    }
    ::v-deep(.tree-title-5:hover) {
      box-shadow: 0 0 0 1px #86b5f8;
    }
    ::v-deep(.tree-title-6:hover) {
      box-shadow: 0 0 0 1px #a8d3f8;
    }
    ::v-deep(.ant-tree-switcher-noop) {
      visibility: hidden;
    }
  }
  .node-edit-button {
    display: none;
    padding-left: 20px;
  }
  .tree-title-wrapper {
    position: relative;
    width: 100%; /* 根据需要调整 */
    height: 40px;
  }
  //本来应该动态计算样式的，但是频繁操作DOM计算页面开销大容易卡顿
  .tree-title {
    width: auto;
    //height: 100%;
    height: auto;
    //border: 1px solid #f7f7f9;
    padding: 0 10px;
    background: #f7f7f9;
    border-radius: 8px;
    border-left-width: 8px;
    top: 0;
    left: 0;
    transition: transform 0.3s, box-shadow 0.3s;
    z-index: 1;
    overflow: hidden;
    border-left-color: #a8d3f8;
    white-space: nowrap;
  }

  .tree-title:hover {
    //transform: scale(1.1);
    //box-shadow: 0 0 10px 3px rgba(0, 0, 0, 0.2);
    //height: auto;
    //z-index: 99;
    //box-shadow: 0 0 10px 3px rgba(202, 240, 248, 0.9);
  }
  //const titleColor = ['#5248DD', '#4A61EA', '#427AF7', '#6498F8', '#86B5F8', '#A8D3F8'];
  .tree-title-1 {
    border-left-color: #5248dd;
  }
  .tree-title-1:hover {
    //box-shadow: 0 0 10px 3px rgba(82, 72, 221, 0.4);
  }
  .tree-title-2 {
    border-left-color: #4a61ea;
  }
  .tree-title-2:hover {
    //box-shadow: 0 0 10px 3px rgba(66, 122, 247, 0.4);
  }
  .tree-title-3 {
    border-left-color: #427af7;
  }
  .tree-title-3:hover {
    //box-shadow: 0 0 10px 3px rgba(100, 152, 248, 0.4);
  }
  .tree-title-4 {
    border-left-color: #6498f8;
  }
  .tree-title-4:hover {
    //box-shadow: 0 0 10px 3px rgba(134, 181, 248, 0.9);
  }
  .tree-title-5 {
    border-left-color: #86b5f8;
  }
  .tree-title-5:hover {
    //box-shadow: 0 0 10px 3px rgba(168, 211, 248, 0.9);
  }
  .tree-title-6 {
    border-left-color: #a8d3f8;
  }
  .tree-title-6:hover {
    //box-shadow: 0 0 10px 3px rgba(202, 240, 248, 0.9);
  }
  .benchmark-name:hover {
    //color: white;
    //transform: scale(1.2);
    //box-shadow: 0 0 10px 3px rgba(0, 0, 0, 0.4);
  }
  .benchmark-edit-button {
    //display: none;
    color: #80ce8d;
    padding: 0 5px;
    font-size: 10px;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    border-radius: 8px;
  }
  .benchmark-delete-icon {
    display: none;
  }
  .node-name {
    display: inline-flex;
    margin: 0 10px 0 0;
    height: 100%;
    align-items: center;
    white-space: pre-wrap;
  }
  .node-name-span {
    margin: 7px;
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
    font-size: 22px;
    width: 100%;
    align-items: center;
    display: flex;
    justify-content: center;
  }
  .evaluation-criteria-span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  //.evaluation-criteria-span:hover {
  //  background: white;
  //  white-space: normal;
  //}
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
    background: white;
    border-radius: 10px;
    padding: 0 10px;
    border: 1px solid #efeff0;
  }
  .tree-node-content {
    margin-left: 5px;
    height: 100%;
  }
  .more-icon:hover {
    color: #aeaeaf !important;
  }
  .translate-and-shadow {
    transition: transform 0.2s ease-in-out, box-shadow 0.3s ease-in-out;
  }
  .translate-with-no-shadow {
    transition: transform 0.2s ease-in-out, box-shadow 0.3s ease-in-out;
  }
  .translate-and-shadow:hover {
    -webkit-transform: translateY(calc(-0.9rem / 5));
    transform: translateY(calc(-0.9rem / 5));
    -webkit-box-shadow: 0 5px 10px rgba(30, 32, 37, 0.12);
    box-shadow: 0 5px 10px rgba(30, 32, 37, 0.12);
  }
  .translate-with-no-shadow:hover {
    -webkit-transform: translateY(calc(-0.9rem / 5));
    transform: translateY(calc(-0.9rem / 5));
  }
</style>
