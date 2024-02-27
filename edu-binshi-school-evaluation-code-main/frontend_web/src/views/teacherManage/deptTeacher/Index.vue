<template>
  <div class="dept-teacher">
    <PageWrapper :content-style="{ height: 'calc(100vh - 80px)' }">
      <div class="content">
        <Row :gutter="[16, 0]" style="height: 100%">
          <Col :span="6" style="height: 100%">
            <div style="background-color: #fff; height: calc(100% + 16px); margin-top: -16px">
              <DeptTree @on-select-dept="onSelectDept" />
            </div>
          </Col>
          <Col :span="18">
            <div style="height: 100%; width: 100%; background-color: #fff">
              <TeacherTable
                :key="dimensionDeptTreeId"
                :dimension-dept-tree-id="dimensionDeptTreeId"
              />
            </div>
          </Col>
        </Row>
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import DeptTree from '/src/components/K12DeptTree/DeptTree.vue';
  import { Row, Col } from 'ant-design-vue';
  import TeacherTable from '/@/views/teacherManage/deptTeacher/TeacherTable.vue';

  export default defineComponent({
    components: {
      PageWrapper,
      DeptTree,
      Row,
      Col,
      TeacherTable,
    },
    setup() {
      const dimensionDeptTreeId = ref();
      return {
        dimensionDeptTreeId,
      };
    },
    methods: {
      onSelectDept(data) {
        console.log(data);
        const node = data.node;
        this.dimensionDeptTreeId = node.dimensionDeptTreeId;
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
</style>
