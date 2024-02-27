<template>
  <div ref="editBenchmarkModalRef" class="edit-benchmark-modal">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.editBenchmarkModalRef"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      width="80vw"
    >
      <template #title>
        <Icon icon="ri:file-list-2-line" />
        <span> {{ readonly ? '查看' : modalCategory === 'ADD' ? '添加' : '编辑' }}快捷评价语 </span>
      </template>
      <!--      <Loading :loading="fullScreenLoading" :absolute="false" />-->
      <Skeleton :loading="fullScreenLoading" style="margin: 100px">
        <div class="content">
          <Form
            :model="params"
            name="form"
            autocomplete="off"
            ref="formRef"
            layout="horizontal"
            :label-col="{ span: 6 }"
            :wrapper-col="{ span: 14 }"
            style="margin-top: 20px"
          >
            <FormItem
              name="name"
              label="评价语"
              :rules="[
                {
                  required: true,
                  trigger: ['blur', 'change'],
                  whitespace: true,
                },
              ]"
            >
              <span v-if="readonly">{{ name }}</span>
              <TextArea
                v-else
                v-model:value="name"
                show-count
                :readonly="readonly"
                :maxlength="10"
                :autoSize="{ minRows: 4, maxRows: 6 }"
              />
            </FormItem>
            <FormItem
              name="name"
              label="是否启用"
              :rules="[
                {
                  required: true,
                  trigger: ['blur', 'change'],
                  whitespace: true,
                },
              ]"
            >
              <Checkbox v-model:checked="isActive"> 启用 </Checkbox>
            </FormItem>
          </Form>
        </div>
      </Skeleton>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          v-if="!readonly"
          :type="'primary'"
          color="edit"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          @click="onClickSubmit"
        >
          提交
        </Button>
      </template>
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import { Checkbox, Form, Input, Skeleton } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { benchmarkStrategySourceCategory } from '/@/utils/helper/common';

  export default defineComponent({
    components: {
      BasicModal,
      Icon,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      Button,
      Checkbox,
      Skeleton,
    },
    emit: ['saveSuccess', 'saveError'],
    setup() {
      const formRef = ref();
      const fullScreenLoading = ref(false);
      const readonly = ref(false);
      const evaluationCriteriaTreeNode = ref();
      const modalCategory = ref('ADD');
      const errorMessage = ref(null);
      const isActive = ref(true);

      const [register, { closeModal }] = useModalInner((data) => {
        modalCategory.value = data.modalCategory;
        clearPrams();
        // fullScreenLoading.value = true;
        evaluationCriteriaTreeNode.value = data.evaluationCriteriaTreeNode;
        if (modalCategory.value === 'EDIT') {
          params.name = data.content;
          isActive.value = data.isActive;
        }
      });
      const params = reactive({
        id: null,
        name: null,
        version: 1,
        guidance: null,
      });
      // 当前节点可选择的benchmark Strategy List
      const benchmarkStrategyList = ref([]);
      // 当前选择的benchmark Strategy
      const benchmarkStrategy = ref();
      // 当前选择的benchmark componentList
      const componentList = ref([]);
      //
      const computedTagList = ref([]);
      //
      const selectTag = ref();
      const refreshScoreSymbolKey = ref(new Date().getTime());
      const limitedStringOptions = ref([]);
      const scoreSymbolRef = ref();
      const componentsRef = ref([]);
      const filterOption = (input: string, option: any) => {
        if (option.value) {
          return JSON.parse(option.value).name.toLowerCase().indexOf(input.toLowerCase()) >= 0;
        }
      };
      const clearPrams = () => {
        params.id = null;
        params.name = null;
        params.version = 1;
        params.guidance = null;
        // benchmarkStrategyList.value = [];
        benchmarkStrategy.value = null;
        componentList.value = [];
        // computedTagList.value = [];
        selectTag.value = null;
      };

      return {
        formRef,
        fullScreenLoading,
        modalCategory,
        register,
        closeModal,
        params,
        ...toRefs(params),
        evaluationCriteriaTreeNode,
        clearPrams,
        benchmarkStrategyList,
        benchmarkStrategy,
        filterOption,
        componentList,
        refreshScoreSymbolKey,
        selectTag,
        computedTagList,
        limitedStringOptions,
        componentsRef,
        scoreSymbolRef,
        readonly,
        benchmarkStrategySourceCategory,
        errorMessage,
        isActive,
      };
    },
    methods: {
      onCloseModal() {
        this.closeModal();
        this.clearPrams();
      },
      onClickSubmit() {
        this.formRef.validateFields().then(() => {
          useMessage().createConfirm({
            iconType: 'info',
            title: '提示',
            content: '确定要提交吗？',
            onOk: () => {
              this.$emit('saveSuccess', { content: this.name, isActive: this.isActive });
              this.onCloseModal();
            },
            onCancel() {},
          });
        });
      },
    },
  });
</script>

<style scoped lang="less">
  .edit-benchmark-modal {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;

      .scroll-container .scrollbar__wrap {
        margin-bottom: 0 !important;
      }

      .scrollbar__view {
        //height: calc(100% - 50px);
        height: 80vh;
        overflow: hidden;
      }

      .ant-modal-body {
        height: 100%;
        //background-color: #f0f2f5;
        .scrollbar {
          padding: 0 !important;
          overflow: hidden;
        }
      }

      .content {
        //height: 100%;
        height: 80vh;
        //background-color: #00acc1;
        overflow-y: auto;
        padding: 16px;
      }
    }
  }

  ::v-deep(.ant-card-body) {
    padding: 0 24px;
  }

  .list-enter-active,
  .list-leave-active {
    transition: opacity 0.5s;
  }

  .list-enter,
  .list-leave-to {
    opacity: 0;
  }
</style>
