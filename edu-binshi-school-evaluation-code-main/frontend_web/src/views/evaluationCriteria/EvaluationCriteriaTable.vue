<template>
  <div>
    <BasicTable
      :dataSource="evaluationCriteriaList"
      :canResize="true"
      :loading="loading"
      :scroll="{ x: 0 | false, y: tableHeight }"
      :showIndexColumn="false"
      @register="registerTable"
      @change="onChange"
      :pagination="{ total: total, pageSize: pageSize, current: pageIndex + 1 }"
    >
      <template #tableTitle>
        <InputSearch
          v-model:value="searchText"
          placeholder="搜索"
          enter-button
          @search="onSearch"
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
          @click="addEvaluationCriteria"
        >
          添加
        </Button>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'statusDisplay'">
          <Tag :color="record.status ? colorData[record.status] : ''">
            {{ record.statusDisplay }}
          </Tag>
        </template>
        <template v-if="column.dataIndex === 'operation'">
          <Button
            type="primary"
            color="edit"
            :iconSize="16"
            preIcon="ant-design:edit-twotone"
            @click="toEdit(record)"
            v-if="['DRAFT', 'PUBLISHED'].indexOf(record.status) > -1"
          >
            编辑
          </Button>
          <Button
            type="primary"
            :iconSize="16"
            preIcon="ant-design:setting-filled"
            style="margin-left: 10px"
            @click="toEvaluationCriteriaTree(record)"
          >
            评价项
          </Button>
          <Button
            type="primary"
            color="green"
            :iconSize="16"
            class="ant-btn-left-margin"
            preIcon="teenyicons:tick-solid"
            v-if="['DRAFT'].indexOf(record.status) > -1"
            @click="updateEvaluationCriteriaStatus(record, 'PUBLISHED')"
          >
            发布
          </Button>
          <Button
            type="primary"
            color="error"
            :iconSize="16"
            preIcon="fe:disabled"
            class="ant-btn-left-margin"
            v-if="record.status === 'PUBLISHED'"
            @click="updateEvaluationCriteriaStatus(record, 'ABOLISHED')"
          >
            作废
          </Button>
          <Button
            hidden="hidden"
            type="primary"
            color="error"
            :iconSize="16"
            preIcon="material-symbols:delete-outline-rounded"
            class="ant-btn-left-margin"
            v-if="record.status === 'DRAFT'"
            @click="deleteEvaluationCriteria(record)"
          >
            删除
          </Button>
        </template>
      </template>
    </BasicTable>
    <EditEvaluationCriteriaModal @register="register" @save-success="saveSuccess" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/views/evaluationCriteria/evaluationCriteriaTableData';
  import { Input, Tag } from 'ant-design-vue';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import {
    apiDeleteEvaluationCriteria,
    apiGetEnumEvaluationCriteriaStatus,
    apiGetEvaluationCriteriaPage,
    apiUpdateEvaluationCriteriaStatus,
  } from '/@/api/evaluationCriteria/evaluationCriteria';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Button } from '/@/components/Button';
  import EditEvaluationCriteriaModal from '/@/views/evaluationCriteria/EditEvaluationCriteriaModal.vue';
  import { useModal } from '/@/components/Modal';
  import { cloneDeep } from 'lodash-es';
  import { colorData } from '/@/utils/helper/common';

  export default defineComponent({
    components: {
      Tag,
      BasicTable,
      InputSearch: Input.Search,
      Button,
      EditEvaluationCriteriaModal,
    },
    setup() {
      const [register, { openModal }] = useModal();
      const evaluationCriteriaList = ref([]);
      const columns = ref();
      const loading = ref(false);
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document));
      columns.value = getBasicColumns();
      const [registerTable] = useTable({
        columns: columns.value,
        bordered: true,
      });
      const params = reactive({
        pageSize: 20,
        pageIndex: 0,
        searchText: '',
        draw: 1,
        statusList: [],
        evaluationObjectCategoryList: [],
      });
      const getEnumEvaluationCriteria = () => {
        apiGetEnumEvaluationCriteriaStatus()
          .then((res) => {
            console.log('apiGetEnumEvaluationCriteriaStatus ...');
            console.log(res);
            if (res.code === 200) {
              columns.value.forEach(function (item) {
                if (item.title == '状态') {
                  item.filters = res.data;
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
          });
      };
      return {
        evaluationCriteriaList,
        getEnumEvaluationCriteria,
        registerTable,
        loading,
        total,
        tableHeight,
        params,
        colorData,
        ...toRefs(params),
        register,
        openModal,
      };
    },
    mounted() {
      this.getEnumEvaluationCriteria();
      this.getEvaluationCriteriaPage();
      // this.$router.push({
      //     path: `/evaluation-criteria/tree/0119c176-35c4-4211-bc69-7732434f1c6b`,
      //   });
    },
    methods: {
      toEvaluationCriteriaTree(data) {
        this.$router.push({
          path: `/evaluation-criteria/tree/${data.id}`,
        });
      },
      toEdit(data) {
        console.log('toEdit ...');
        console.log(data);
        this.openModal(true, {
          modalCategory: 'EDIT',
          evaluationCriteria: data,
        });
      },
      saveSuccess() {
        this.getEvaluationCriteriaPage();
      },
      addEvaluationCriteria() {
        this.openModal(true, {
          modalCategory: 'ADD',
        });
      },
      getEvaluationCriteriaPage() {
        this.loading = true;
        apiGetEvaluationCriteriaPage(this.params)
          .then((res) => {
            console.log('apiGetEvaluationCriteriaPage ...');
            console.log(res);
            if (res.code === 200) {
              this.total = res.data.filterCount;
              this.evaluationCriteriaList = res.data.data;
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
      onSearch() {
        this.pageIndex = 0;
        this.getEvaluationCriteriaPage();
      },
      onChange(pageInfo, filters) {
        console.log('filters ...');
        console.log(filters);
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.params.statusList = filters.statusDisplay ? filters.statusDisplay : [];
        this.params.evaluationObjectCategoryList = filters.evaluationObjectCategoryDisplay
          ? filters.evaluationObjectCategoryDisplay
          : [];
        this.getEvaluationCriteriaPage();
      },
      init() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
      },
      updateEvaluationCriteriaStatus(data, status) {
        const evaluationCriteria = cloneDeep(data);
        evaluationCriteria.status = status;
        const statusDisplay = status === 'PUBLISHED' ? '发布' : '作废';
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: `确定要${statusDisplay}【<text style="color: #00acc1">${data.name}</text>】吗？`,
          onOk: () => {
            this.doUpdateEvaluationCriteriaStatus(evaluationCriteria, statusDisplay);
          },
          onCancel() {},
        });
      },
      deleteEvaluationCriteria(data) {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: `确定要删除【<text style="color: #00acc1">${data.name}</text>】吗？`,
          onOk: () => {
            this.doDeleteEvaluationCriteria(data.id);
          },
          onCancel() {},
        });
      },
      doDeleteEvaluationCriteria(evaluationCriteriaId) {
        const params = {
          evaluationCriteriaId: evaluationCriteriaId,
        };
        apiDeleteEvaluationCriteria(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '成功',
                description: '删除成功',
              });
              this.getEvaluationCriteriaPage();
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
            // this.loading = false;
          });
      },
      doUpdateEvaluationCriteriaStatus(evaluationCriteria, statusDisplay) {
        this.loading = true;
        apiUpdateEvaluationCriteriaStatus(evaluationCriteria)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '成功',
                description: `${statusDisplay}成功`,
              });
              this.getEvaluationCriteriaPage();
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
            // this.loading = false;
          });
      },
    },
  });
</script>

<style scoped lang="less"></style>
