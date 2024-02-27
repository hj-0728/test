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
        <span> 快捷评语设置 </span>
      </template>
      <!--      <Loading :loading="fullScreenLoading" :absolute="false" />-->
      <BasicTable
        :dataSource="tableData"
        :canResize="true"
        :loading="loading"
        :scroll="{ y: tableHeight }"
        :showIndexColumn="false"
        @register="registerTable"
        :pagination="{ total: total, pageSize: pageSize, current: pageIndex + 1 }"
      >
        <template #tableTitle>
          <InputSearch
            v-model:value="searchText"
            placeholder="搜索"
            enter-button
            style="padding: 5px 0; width: 30%"
          />
        </template>
        <template #toolbar>
          <Button
            type="primary"
            color="success"
            :iconSize="18"
            preIcon="ant-design:plus-outlined"
            class="ant-btn-left-margin"
            @click="toAdd"
          >
            添加
          </Button>
        </template>
        <template #bodyCell="{ column, record }">
          <template v-if="column.dataIndex === 'isActive'">
            <Switch
              v-model:checked="record.isActive"
              checked-children="启用"
              un-checked-children="禁用"
              @change="onChangeStatus(record)"
            />
          </template>
          <template v-if="column.dataIndex === 'operation'">
            <Button
              type="primary"
              color="edit"
              :iconSize="16"
              preIcon="ant-design:setting-filled"
              @click="setSubject(record)"
            >
              编辑
            </Button>
            <Button
              type="primary"
              color="error"
              :iconSize="16"
              preIcon="material-symbols:delete-outline-rounded"
              class="ant-btn-left-margin"
              @click="deleteEvaluationCriteria(record)"
            >
              删除
            </Button>
          </template>
        </template>
      </BasicTable>
      <EditShorLanguage @register="registerEdit" @saveSuccess="save" />
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
      </template>
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicModal, useModal, useModalInner } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiDeleteBenchmark } from '/@/api/benchmark/benchmark';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { benchmarkStrategySourceCategory } from '/@/utils/helper/common';
  import { BasicTable, useTable } from '/@/components/Table';
  import { Button } from '/@/components/Button';
  import { Input, Switch } from 'ant-design-vue';
  import { Icon } from '/@/components/Icon';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { getBasicColumns } from '/@/views/evaluationCriteriaTree/components/shortLanguageTableData';
  import { apiK12TeacherListPage } from '/@/api/k12TeacherSubject/k12TeacherSubject';
  import EditShorLanguage from '/@/views/evaluationCriteriaTree/components/EditShorLanguage.vue';
  export default defineComponent({
    components: {
      Switch,
      Button,
      BasicTable,
      BasicModal,
      InputSearch: Input.Search,
      Icon,
      EditShorLanguage,
    },
    emit: ['saveSuccess', 'saveError'],
    setup() {
      const formRef = ref();
      const fullScreenLoading = ref(false);
      const readonly = ref(false);
      const evaluationCriteriaTreeNode = ref();
      const modalCategory = ref('ADD');
      const errorMessage = ref(null);

      const [register, { closeModal }] = useModalInner((data) => {
        modalCategory.value = data.modalCategory;
        // fullScreenLoading.value = true;
        evaluationCriteriaTreeNode.value = data.evaluationCriteriaTreeNode;
        getStudentPage();
      });
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document));
      const loading = ref(false);
      const tableData = ref([]);
      const params = reactive({
        pageSize: 20,
        pageIndex: 0,
        searchText: '',
        draw: 1,
      });
      const columns = ref();
      columns.value = getBasicColumns();
      const [registerTable] = useTable({
        columns: columns.value,
        bordered: true,
      });

      const getStudentPage = () => {
        loading.value = true;
        apiK12TeacherListPage(params)
          .then((res) => {
            if (res.code === 200) {
              res.data.data = [
                {
                  id: 1,
                  content: '学习态度积极，勤奋好学，积极参与课堂讨论',
                  isActive: true,
                },
                {
                  id: 2,
                  content: '学业成绩优异，常获奖学金，值得表扬',
                  isActive: true,
                },
                {
                  id: 3,
                  content: '作业认真仔细，能够独立完成任务',
                  isActive: true,
                },
                {
                  id: 4,
                  content: '对待挑战态度积极，勇于接受新知识',
                  isActive: true,
                },
                {
                  id: 5,
                  content: '与同学相处和谐，善于团队合作',
                  isActive: true,
                },
              ];
              total.value = 5;
              tableData.value = res.data.data;
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
            loading.value = false;
          });
      };
      const [registerEdit, { openModal }] = useModal();
      return {
        formRef,
        fullScreenLoading,
        modalCategory,
        register,
        closeModal,
        params,
        ...toRefs(params),
        evaluationCriteriaTreeNode,
        total,
        tableHeight,
        loading,
        tableData,
        registerTable,
        readonly,
        benchmarkStrategySourceCategory,
        errorMessage,
        openModal,
        registerEdit,
        getStudentPage,
      };
    },
    methods: {
      onCloseModal() {
        this.closeModal();
      },
      doDeleteBenchmark() {
        apiDeleteBenchmark({})
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '删除成功',
              });
              setTimeout(() => {
                this.$emit('saveSuccess');
              }, 1000);
              this.onCloseModal();
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
      setSubject(data) {
        this.openModal(true, {
          modalCategory: 'EDIT',
          content: data.content,
          isActive: data.isActive,
          id: data.id,
        });
      },
      deleteEvaluationCriteria(data) {
        console.log(data);
      },
      save(data) {
        console.log(data);
        this.getStudentPage();
      },
      toAdd() {
        this.openModal(true, { modalCategory: 'ADD' });
      },
      onChangeStatus(record) {
        this.tableData.forEach((item) => {
          if (item.id === record.id) {
            if (item.isActive) {
              item.isActive = false;
            } else {
              item.isActive = true;
            }
          }
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
