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
      </Col>
    </Row>
    <div style="height: calc(100% - 60px); overflow: hidden">
      <img
        src="../../assets/svg/treeEmpty.svg"
        width="300"
        v-if="evaluationCriteriaTreeList.length === 0 && !loading"
        style="margin: 0 auto"
        alt="empty"
      />
      <Tree
        v-else-if="evaluationCriteriaTreeList?.length > 0"
        ref="evaluationCriteriaTreeRef"
        :treeData="evaluationCriteriaTreeList"
        :loading="loading"
        :clickRowToExpand="false"
        :selectable="false"
        :delete-default-height="true"
        :defaultExpandAll="true"
        style="overflow-x: auto; white-space: no-wrap"
        @expand="onExpand"
      >
        <template #switcherIcon="{ switcherCls, expanded }">
          <MinusSquareOutlined v-if="expanded" :class="[switcherCls, 'open-switcher-icon']" />
          <PlusSquareOutlined v-else :class="[switcherCls, 'close-switcher-icon']" />
        </template>
        <template #title="node">
          <div class="tree-title-wrapper">
            <div
              :class="[
                'tree-title',
                'inline-flex-center',
                selectedKeys.includes(node.key) ? 'tree-title-selected' : '',
              ]"
            >
              <div class="node-name">
                <SvgIcon v-if="node.tag === 'X（变量）'" name="xIcon" size="18px" />
                <SvgIcon v-else-if="node.tag === 'N（常量）'" name="nIcon" size="18px" />
                <Icon v-else icon="ph:ruler-bold" color="#58a76e" size="20px" />
                <span class="node-name-span">{{ node.name }} </span>
              </div>
              <div
                v-if="
                  (node.benchmarkList && node.benchmarkList.length > 0) ||
                  evaluationCriteria?.status !== 'ABOLISHED'
                "
                class="benchmark-div inline-flex-center"
              >
                <Icon icon="material-symbols:label-outline" color="#aeaeaf" />
                <div
                  v-for="benchmark in node.benchmarkList"
                  :key="benchmark.id"
                  @click.stop="clickOpenEditBenchmarkModal(node, 'EDIT', benchmark)"
                  class="benchmark-edit-span inline-flex-center"
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
                style="margin-left: 10px; cursor: pointer"
                @click.stop="toEdit(node)"
              />
              <Dropdown :trigger="['focus', 'click']" :autoAdjustOverflow="true">
                <Icon
                  v-if="evaluationCriteria?.status !== 'ABOLISHED'"
                  icon="ri:more-2-fill"
                  color="#777777"
                  style="margin-left: 10px; cursor: pointer"
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
                    <MenuItem @click.stop="toShortLanguage(node)"
                      ><Icon icon="mdi:air-filter" color="#2a7dc9" style="margin-right: 5px" />
                      快捷评语配置
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
  </div>
  <EditEvaluationCriteriaTreeModal
    ref="refEvaluationCriteriaTree"
    @register="register"
    @save-success="saveSuccess"
    @save-error="saveError"
  />
  <EditBenchmarkModal
    ref="refEditBenchmarkModal"
    @register="registerEditBenchmarkModal"
    @save-success="saveSuccess"
    @save-error="saveError"
  />
  <BindTagModal
    ref="refBindTagModal"
    @register="registerBindTagModal"
    @save-success="saveSuccess"
    @save-error="saveError"
  />
  <ShortLanguage
    ref="refShortcutLanguageConfigurationModal"
    @register="registerShortcutLanguageConfiguration"
  />
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Button, Row, Col, Dropdown, Menu, Tree, Tooltip } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { getAuthCache } from '/@/utils/auth';
  import { UserInfo } from '/#/store';
  import {
    apiDeleteEvaluationCriteriaTree,
    apiGetEvaluationCriteriaTree,
  } from '/@/api/evaluationCriteriaTree/evaluationCriteriaTree';
  import { Icon, SvgIcon } from '/@/components/Icon';
  import EditEvaluationCriteriaTreeModal from '/@/views/evaluationCriteriaTree/EditEvaluationCriteriaTreeModal.vue';
  import { useModal } from '/@/components/Modal';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { apiGetEvaluationCriteriaDetail } from '/@/api/evaluationCriteria/evaluationCriteria';
  import EditBenchmarkModal from '/@/views/evaluationCriteriaTree/components/EditBenchmarkModal.vue';
  import { SoftTag } from '/@/components/Tag';
  import { benchmarkStrategySourceCategory } from '/@/utils/helper/common';
  import BindTagModal from '/@/views/evaluationCriteriaTree/bindTagComponents/BindTagModal.vue';
  import { PlusSquareOutlined, MinusSquareOutlined } from '@ant-design/icons-vue';
  import ShortLanguage from '/@/views/evaluationCriteriaTree/components/ShortLanguage.vue';
  export default defineComponent({
    components: {
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
      Tree,
      Tooltip,
      PlusSquareOutlined,
      MinusSquareOutlined,
      ShortLanguage,
    },
    emits: ['onSelectEvaluationCriteriaTreeNode', 'getEvaluationCriteria'],
    setup() {
      const [register, { openModal }] = useModal();
      const [registerBindTagModal, { openModal: openBindTagModal }] = useModal();
      const [registerEditBenchmarkModal, { openModal: openEditBenchmarkModal }] = useModal();
      const [
        registerShortcutLanguageConfiguration,
        { openModal: openShortcutLanguageConfiguration },
      ] = useModal();
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
        registerShortcutLanguageConfiguration,
        openShortcutLanguageConfiguration,
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
              if (this.evaluationCriteria.status === 'ABOLISHED') {
                this.$refs.refEvaluationCriteriaTree.onCloseModal();
                this.$refs.refEditBenchmarkModal.onCloseModal();
                this.$refs.refBindTagModal.onCloseModalParent();
              }
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
      toShortLanguage(node) {
        this.refreshKey = new Date().getTime();
        this.openShortcutLanguageConfiguration(true, {
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
              this.expandedKeys = [];
              this.evaluationCriteriaTreeList.forEach((item) => {
                this.expandedKeys.push(item.key);
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
      saveError() {
        this.loading = true;
        this.getEvaluationCriteriaDetail();
        this.getEvaluationCriteriaTree();
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
      width: 100%;
      flex: 0 0 auto;
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

    ::v-deep(.ant-tree-switcher_close) {
      svg {
        transform: rotate(0deg);
      }
    }

    .open-switcher-icon {
      margin-right: 8px;
      justify-content: center;
      align-items: center;
      margin-left: 2px;
      font-size: 18px;
    }

    .close-switcher-icon {
      margin-right: 8px;
      justify-content: center;
      align-items: center;
      margin-left: 2px;
      font-size: 18px;
      transform: rotate(180deg);
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

    ::v-deep(.tree-title:hover) {
      //border: 0 0 0 1px #5248dd;
      box-shadow: 0 0 0 1px #5248dd;
    }

    ::v-deep(.ant-tree-switcher-noop) {
      visibility: hidden;
    }
  }

  ::v-deep(.ant-tree .ant-tree-node-content-wrapper) {
    cursor: auto;
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
    width: 100%;
    //height: 100%;
    height: auto;
    //border: 1px solid #a8d3f8;
    padding: 0 10px;
    background: #f7f7f9;
    border-radius: 8px;
    top: 0;
    left: 0;
    transition: transform 0.3s, box-shadow 0.3s;
    z-index: 1;
    overflow: hidden;
    white-space: nowrap;
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
    cursor: pointer;
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
</style>
