<template>
  <div class="dept-student">
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
              <StudentUserTable
                :key="dimensionDeptTreeId"
                :dimension-dept-tree-id="dimensionDeptTreeId"
                :dept-name="deptName"
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
  import DeptTree from '/@/components/K12DeptTree/DeptTree.vue';
  import { Row, Col } from 'ant-design-vue';
  import StudentUserTable from '/@/views/accountManage/studentAccount/components/StudentUserTable.vue';

  export default defineComponent({
    components: {
      PageWrapper,
      DeptTree,
      Row,
      Col,
      StudentUserTable,
    },
    setup() {
      const dimensionDeptTreeId = ref();
      const deptName = ref();
      return {
        dimensionDeptTreeId,
        deptName,
      };
    },
    methods: {
      onSelectDept(data) {
        console.log(data);
        const node = data.node;
        this.dimensionDeptTreeId = node.dimensionDeptTreeId;
        this.deptName = node.name;
      },
    },
  });
</script>

<style scoped lang="less">
  .dept-student {
    .content {
      //background-color: #fff;
      height: 100%;
    }
  }
</style>
