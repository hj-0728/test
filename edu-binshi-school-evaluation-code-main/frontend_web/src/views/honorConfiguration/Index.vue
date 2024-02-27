<template>
  <div class="dept-teacher">
    <PageWrapper :content-style="{ height: 'calc(100vh - 80px)' }">
      <template #headerContent>
        <div class="select-period">
          <div class="select-item-wrapper">
            <span> <ClockCircleOutlined /> <label class="select-label">周期</label> </span>
            <Select
              :options="periodList"
              v-model:value="periodInfoId"
              style="min-width: 250px"
              placeholder="请选择周期"
              @change="onChangePeriod"
              :allowClear="false"
              :fieldNames="{ label: 'name', value: 'id' }"
            />
            <Icon
              icon="ant-design:plus-outlined"
              @click="addPeriod"
              size="20"
              style="margin-left: 10px"
              color="#1890ff"
            />
          </div>
        </div>
      </template>
      <div class="content">
        <Row :gutter="[16, 0]" style="height: 100%">
          <Col :span="6" style="height: 100%">
            <div style="background-color: #fff; height: calc(100% + 16px); margin-top: -16px">
              <DeptTree
                :key="periodInfoId"
                :periodId="periodInfoId"
                @on-select-dept="onSelectDept"
              />
            </div>
          </Col>
          <Col :span="18">
            <div style="height: 100%; width: 100%; background-color: #fff">
              <TeacherTable
                :key="dimensionDeptTreeId + periodInfoId"
                :periodId="periodInfoId"
                :dimension-dept-tree-id="dimensionDeptTreeId"
              />
            </div>
          </Col>
        </Row>
      </div>
      <AddPeriod @register="registerAddModal" @save-success="saveSuccess" />
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import DeptTree from '/src/views/honorConfiguration/DeptTree.vue';
  import { Row, Col, Select } from 'ant-design-vue';
  import TeacherTable from '/@/views/honorConfiguration/TeacherTable.vue';
  import { ClockCircleOutlined } from '@ant-design/icons-vue';
  import Icon from '/@/components/Icon/src/Icon.vue';
  import AddPeriod from '/@/views/honorConfiguration/AddPeriod.vue';
  import { useModal } from '/@/components/Modal';

  export default defineComponent({
    components: {
      Icon,
      Select,
      ClockCircleOutlined,
      PageWrapper,
      DeptTree,
      Row,
      Col,
      TeacherTable,
      AddPeriod,
    },
    setup() {
      const dimensionDeptTreeId = ref();
      const periodInfoId = ref('7a18fac8-5402-47fe-9445-32a234e7ac16');
      const [registerAddModal, { openModal: openAddModal }] = useModal();
      const periodList = ref([
        {
          id: '7a22a673-42a0-4bb1-850d-76d640b0fd80',
          version: 1,
          handlerCategory: 'ROBOT',
          handlerId: '1273fbb4-66b3-4b60-a61f-f31ed7de9ee0',
          handledAt: '2023-07-24T17:06:52.219557+08:00',
          remark: null,
          periodCategoryId: 'da1fce60-4a34-475f-a4e7-18779420f63f',
          name: '2023-2024学年上学期',
          code: null,
          startAt: '2023-07-03T00:00:00+08:00',
          finishAt: '2024-02-01T00:00:00+08:00',
          parentId: '0fe6afde-30d6-4228-a0bb-555eec18e6be',
          categoryCode: null,
          categoryName: null,
        },
        {
          id: '74a03bba-14d1-4945-bb91-48d75e386043',
          version: 1,
          handlerCategory: 'ROBOT',
          handlerId: '1273fbb4-66b3-4b60-a61f-f31ed7de9ee0',
          handledAt: '2023-07-24T17:06:52.219557+08:00',
          remark: null,
          periodCategoryId: 'da1fce60-4a34-475f-a4e7-18779420f63f',
          name: '2022-2023学年上学期',
          code: null,
          startAt: '2022-09-01T00:00:00+08:00',
          finishAt: '2023-02-01T00:00:00+08:00',
          parentId: '3c5b011e-fe1f-4853-ac91-38750e4b554b',
          categoryCode: null,
          categoryName: null,
        },
        {
          id: '7a18fac8-5402-47fe-9445-32a234e7ac16',
          version: 1,
          handlerCategory: 'ROBOT',
          handlerId: '1273fbb4-66b3-4b60-a61f-f31ed7de9ee0',
          handledAt: '2023-07-24T17:06:52.219557+08:00',
          remark: null,
          periodCategoryId: 'da1fce60-4a34-475f-a4e7-18779420f63f',
          name: '2022-2023学年下学期',
          code: null,
          startAt: '2022-03-01T00:00:00+08:00',
          finishAt: '2023-07-01T00:00:00+08:00',
          parentId: '3c5b011e-fe1f-4853-ac91-38750e4b554b',
          categoryCode: null,
          categoryName: null,
        },
      ]);
      return {
        dimensionDeptTreeId,
        periodList,
        periodInfoId,
        registerAddModal,
        openAddModal,
      };
    },
    methods: {
      onSelectDept(data) {
        console.log(data);
        const node = data.node;
        this.dimensionDeptTreeId = node.dimensionDeptTreeId;
      },
      onChangePeriod(_value, option) {
        // this.periodInfoId = option;
        // this.changeCurrentPeriod();
        this.periodInfoId = option.id;
      },
      addPeriod() {
        this.openAddModal(true, {});
      },
      saveSuccess() {
        this.periodList.push();
      },
    },
  });
</script>

<style scoped lang="less">
  .dept-teacher {
    .content {
      //background-color: #fff;
      height: 100%;
    }
  }

  .select-item-wrapper {
    margin: 0 10px 0 0;
  }

  .select-period {
    width: 100%;
    display: flex;
    background: white;
    flex: 1;
    justify-content: flex-start;
  }

  .select-label {
    color: black;
    margin-right: 10px;
  }
</style>
