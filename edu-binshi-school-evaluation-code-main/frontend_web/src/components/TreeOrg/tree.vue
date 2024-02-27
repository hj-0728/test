<template>
  <div ref="eleRef" class="zm-tree-org">
    <!--    <div ref="zoomRef" class="zoom-container" :style="zoomStyle" @wheel="zoomWheel">-->
    <div ref="zoomRef" class="zoom-container" :style="zoomStyle">
      <Draggable
        :x="left"
        :y="top"
        :class="{ dragging: autoDragging }"
        @dragging="onDrag"
        @dragstop="onDragStop"
        :draggable="draggable"
        :drag-cancel="dragCancel"
      >
        <div ref="treeRef" class="tree-org" :class="{ horizontal, collapsable }">
          <TreeOrgNode
            :data="treeData"
            :props="keys"
            :horizontal="horizontal"
            :labelStyle="labelStyle"
            :collapsable="collapsable"
            :renderContent="renderContent"
            :selectedKey="selectedKey"
            :selectedClassName="selectedClassName"
            :labelClassName="labelClassName"
            :vNodedrag="nodeargs"
            @on-expand="handleExpand"
            @node-click="handleClick"
            @node-dblclick="handleDblclick"
            @node-mouseenter="nodeMouseenter"
            @node-mouseleave="nodeMouseleave"
            @node-contextmenu="nodeContextmenu"
            @node-focus="
              (e, data) => {
                $emit('on-node-focus', e, data);
              }
            "
            @node-blur="handleBlur"
          >
            <template #default="{ node }">
              <slot :node="node">
                <div
                  class="node-content"
                  :style="{
                    backgroundColor: '#fff',
                    color: '#000',
                    width: 'max-content',
                    position: 'relative',
                  }"
                >
                  <Tooltip placement="right">
                    <template #title v-if="node.mobile">
                      <div style="width: 200px; text-align: left">
                        <div>姓名：{{ node.title }}</div>
                        <div>电话号码：{{ node.mobile }}</div>
                        <div>现居地址：{{ node.address }}</div>
                      </div>
                    </template>
                    <div style="margin-top: -5px" v-if="node.url">
                      <Avatar
                        :size="{ xs: 14, sm: 22, md: 30, lg: 54, xl: 70, xxl: 90 }"
                        :src="node.url"
                        style=""
                      />
                      <div style="height: 5px"></div>
                    </div>
                    <div class="default-content">
                      <div style="font-weight: bold">
                        <Icon v-if="node.icon" :icon="node.icon" />
                        {{ node.title }}
                      </div>
                      <div style="font-size: 12px; margin-top: -2px">
                        <span class="node-label">{{ node.label }}</span>
                      </div>
                      <div style="height: 3px"></div>
                    </div>
                  </Tooltip>
                  <div v-if="node.children ? node.children.length <= 0 : true">
                    <div v-if="$props.horizontal" class="btn-div-horizontal">
                      <div
                        class="circle-div"
                        @click.stop="addNode(node)"
                        style="margin-top: -10px; left: 19px; position: relative"
                        v-if="$props.canEdit"
                      >
                        <Icon
                          icon="ion:add"
                          :style="{
                            color: t('sys.color.treeOrgAddBtn'),
                            top: '-2px',
                            position: 'relative',
                          }"
                        />
                      </div>
                      <div class="btn-line-right" v-if="$props.canEdit"></div>
                      <div class="btn-line-top-left" v-if="$props.canEdit"></div>
                      <Tooltip placement="right">
                        <template #title v-if="node.root && node.children">
                          <div>根节点禁止删除</div>
                        </template>
                        <div
                          class="circle-div"
                          @click.stop="!(node.root && node.children) ? deleteNode(node) : ''"
                          :style="
                            'margin-top: 20px; margin-left: -20px;' +
                            (node.root && node.children ? 'background-color: #e6e6e6' : '')
                          "
                          v-if="$props.canEdit"
                        >
                          <Icon
                            icon="ion:remove"
                            :style="{
                              color:
                                node.root && node.children
                                  ? '#aaaaaa'
                                  : t('sys.color.treeOrgRemoveBtn'),
                              top: '-2px',
                              position: 'relative',
                            }"
                          />
                        </div>
                      </Tooltip>
                    </div>
                    <div class="btn-div" v-else>
                      <div
                        class="circle-div"
                        @click.stop="addNode(node)"
                        style="margin-top: 5px"
                        v-if="$props.canEdit"
                      >
                        <Icon
                          icon="ion:add"
                          :style="{
                            color: t('sys.color.treeOrgAddBtn'),
                            top: '-2px',
                            position: 'relative',
                          }"
                        />
                      </div>
                      <div class="btn-line-left-bottom" v-if="$props.canEdit"></div>
                      <div class="btn-line-top" v-if="$props.canEdit"></div>
                      <Tooltip placement="right">
                        <template #title v-if="node.root && node.children">
                          <div>根节点禁止删除</div>
                        </template>
                        <div
                          class="circle-div"
                          @click.stop="deleteNode(node)"
                          style="margin-top: 5px"
                          v-if="$props.canEdit"
                        >
                          <Icon
                            icon="ion:remove"
                            :style="{
                              color:
                                node.root && node.children
                                  ? '#aaaaaa'
                                  : t('sys.color.treeOrgRemoveBtn'),
                              top: '-2px',
                              position: 'relative',
                            }"
                          />
                        </div>
                      </Tooltip>
                    </div>
                  </div>
                </div>
              </slot>
            </template>
            <template #expand="{ node }">
              <slot name="expand" :node="node">
                <div :style="$props.horizontal ? 'margin-left: 2px; margin-top: -5px' : ''">
                  <div
                    class="circle-div"
                    :style="
                      'position: absolute;' +
                      ($props.horizontal ? 'margin-top: -25px' : 'right: 25px')
                    "
                    @click.stop="addNode(node)"
                    v-if="$props.canEdit"
                  >
                    <Icon icon="ion:add" :style="{ color: t('sys.color.treeOrgAddBtn') }" />
                  </div>
                  <div class="circle-div" :style="$props.horizontal ? 'margin-top: 5px' : ''">
                    <Icon v-if="node.expand" icon="iconoir:nav-arrow-up" style="color: #999999" />
                    <Icon v-else icon="iconoir:nav-arrow-down" style="color: #999999" />
                  </div>
                  <div class="expand-line" v-if="!$props.horizontal && $props.canEdit"></div>
                  <div
                    class="expand-line-horizontal"
                    v-if="$props.horizontal && $props.canEdit"
                  ></div>
                  <div
                    class="circle-div"
                    :style="
                      'position: absolute;' +
                      ($props.horizontal ? 'margin-top: 5px' : 'left: 25px; top: 0')
                    "
                    @click.stop="deleteNode(node)"
                    v-if="$props.canEdit"
                  >
                    <Icon icon="ion:remove" :style="{ color: t('sys.color.treeOrgRemoveBtn') }" />
                  </div>
                </div>
              </slot>
            </template>
          </TreeOrgNode>
        </div>
      </Draggable>
    </div>
    <Tools
      v-if="tools.visible"
      :tools="tools.data"
      :scale="zoomPercent"
      @on-expand="expandChange"
      @on-scale="zoomOrgchart"
      @on-restore="restoreOrgchart"
      @on-fullscreen="handleFullscreen"
    />
    <clone-org
      v-if="nodeDraggable"
      v-model="nodeMoving"
      :props="keys"
      :data="cloneData.data"
      :horizontal="horizontal"
      :label-style="labelStyle"
      :collapsable="collapsable"
      :render-content="renderContent"
      :label-class-name="labelClassName"
    >
      <template #default="{ node }">
        <slot :node="node">
          <div class="tree-org-node__text">
            <div style="font-weight: bold">{{ node[keys.title] }}</div>
            <div style="font-size: 12px">{{ node[keys.label] }}</div>
          </div>
        </slot>
      </template>
      <template #expand="{ node }">
        <slot name="expand" :node="node">
          <span class="tree-org-node__expand-btn"></span>
        </slot>
      </template>
    </clone-org>
    <Contextmenu
      v-if="defineMenus.length"
      v-model="contextmenu"
      :x="menuX"
      :y="menuY"
      :node="menuData.data"
      :data="data"
      :props="keys"
      :menus="defineMenus"
      :disabled="disabled"
      :node-add="nodeAdd"
      :node-delete="nodeDelete"
      :node-edit="nodeEdit"
      :node-copy="nodeCopy"
      @contextmenu="
        (arg) => {
          $emit('on-contextmenu', arg);
        }
      "
      @on-node-copy="
        (txt) => {
          $emit('on-node-copy', txt);
        }
      "
      @on-node-delete="
        (txt) => {
          $emit('on-node-delete', txt);
        }
      "
    />
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, reactive } from 'vue';
  import TreeOrgNode from './components/node';
  import Tools from './components/tools';
  import Draggable from './components/draggable';
  import CloneOrg from './components/clone-org';
  import Contextmenu from './components/contextmenu';
  import drag from './directives/drag';
  import { getThis, getProps } from './directives/drag';
  import { treeProps, treeEmits } from './tree';
  import { useTree } from './use-tree';
  import './styles/index.less';
  import { Avatar, Tooltip } from 'ant-design-vue';
  import { Icon } from '/@/components/Icon';
  import { INode } from '/@/components/TreeOrg/utils/types';
  import { useI18n } from '/@/hooks/web/useI18n';
  export default defineComponent({
    name: 'Vue3TreeOrg',
    components: {
      Tools,
      CloneOrg,
      Draggable,
      Contextmenu,
      TreeOrgNode,
      Avatar,
      Tooltip,
      Icon,
    },
    directives: {
      nodedrag: drag,
    },
    props: treeProps,
    emits: treeEmits,
    setup(props, ctx) {
      const eleRef = ref<HTMLElement>();
      const treeRef = ref<HTMLElement>();
      const zoomRef = ref<HTMLElement>();
      const treeData = reactive(props.data);
      const treeOrg = useTree(props, ctx, { eleRef, treeRef, zoomRef });
      const { t } = useI18n();
      getProps(props);
      return {
        eleRef,
        treeRef,
        zoomRef,
        treeData,
        ...treeOrg,
        t,
      };
    },
    mounted() {
      getThis(this);
    },
    methods: {
      focus() {},
      addNode(parentNode) {
        parentNode.expand = true;
        const node = {
          id: new Date().getTime(),
          pid: parentNode.id,
          title: '测试-标题 ' + new Date().getTime(),
          label: '测试-label ' + new Date().getTime(),
          category: 'person',
          url: 'https://cloud.crysu.com/tmp/6.png',
          email: 'zhaodanyu@gov.cn',
          mobile: '18067697891',
          address: '浙江省缙云县五云街道镇东村1号',
          expand: true,
        };
        if (parentNode.children === undefined) {
          parentNode.children = [node];
        } else {
          parentNode.children.push(node);
        }
      },
      deleteNode(node) {
        if (node.root) {
          if (node.children !== undefined) {
            node.children = [];
          }
          return;
        }
        const oldPaNode = this.getNodeById(this.treeData, 'id', node['pid']);
        if (oldPaNode) {
          const list = oldPaNode['children'];
          for (let i = 0, len = list.length; i < len; i++) {
            if (list[i]['id'] === node['id']) {
              list.splice(i, 1);
              this.$emit('on-node-delete', node);
              break;
            }
          }
        }
      },
      getNodeById(data: INode, key: string, value: any): INode | undefined {
        if (data[key] === value) {
          return data;
        } else if (Array.isArray(data.children)) {
          const list = data.children;
          for (let i = 0, len = list.length; i < len; i++) {
            const row = list[i];
            const pNode = this.getNodeById(row, key, value);
            if (pNode) {
              return pNode;
            }
          }
        }
      },
    },
  });
</script>
<style lang="less" scoped>
  .default-content {
    background-color: #eeeeee;
    padding: 5px 10px;
    border-radius: 5px;
    white-space: pre;
    margin-top: -10px;
    min-width: 120px;
    min-height: 30px;
  }

  .node-content {
    padding: 8px 15px;
  }

  .circle-div {
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: #cccccc solid 1px;
    z-index: 9;
    transition: all 0.35s ease;
    background-color: white;
    cursor: pointer;
  }

  .circle-div:hover {
    transform: scale(1.2);
  }

  .expand-line {
    width: 55px;
    height: 1px;
    position: absolute;
    border-top: #ddd solid 1px;
    top: 9px;
    left: -10px;
    z-index: -1;
  }

  .expand-line-horizontal {
    width: 1px !important;
    height: 55px !important;
    position: absolute;
    border-left: #ddd solid 1px;
    top: -18px !important;
    left: 11px !important;
    z-index: -1;
  }

  .btn-div {
    display: flex;
    margin-top: 10px;
    left: 50%;
    margin-left: -28px;
    position: relative;
  }

  .btn-div-horizontal {
    display: flex;
    left: 100%;
    top: 50%;
    position: absolute;
    margin-top: -20px;
    margin-left: -10px;
  }

  .btn-line-left-bottom {
    width: 10px;
    height: 15px;
    border-right: #ddd solid 1px;
    border-bottom: #ddd solid 1px;
  }

  .btn-line-top {
    width: 10px;
    height: 15px;
    border-top: #ddd solid 1px;
    margin-top: 14.5px;
  }

  .btn-line-right {
    width: 10px;
    height: 15px;
    border-right: #ddd solid 1px;
    border-bottom: #ddd solid 1px;
    margin-left: -1px;
  }

  .btn-line-top-left {
    width: 10px;
    height: 15px;
    border-left: #ddd solid 1px;
    margin-top: 14.5px;
    margin-left: -1px;
  }

  .node-label {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    word-break: break-all;
    max-width: 200px;
  }
</style>
