<template>
  <div>
    <PageWrapper>
      <div style="height: calc(100vh - 85px); background: white">
        <BasicTable
          :dataSource="tableData"
          :canResize="true"
          :loading="loading"
          :scroll="{ y: tableHeight }"
          :showIndexColumn="false"
          @register="registerTable"
          @change="onChange"
        >
          <template #tableTitle>
            <InputSearch
              v-model:value="searchText"
              placeholder="搜索"
              enter-button
              @search="onSearch"
              style="padding: 10px 0 10px 0; width: 30%"
            />
          </template>
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'categoryName'">
              <span>{{ record.categoryName }}</span>
            </template>
            <template v-if="column.dataIndex === 'roleNameList'">
              <div
                v-if="record.accessStrategy === 'CONTROLLED'"
                style="display: flex; flex-direction: column; align-items: center"
              >
                <Tag
                  v-for="item in record.roleNameList"
                  :key="item"
                  style="margin: 2px; width: fit-content"
                  color="blue"
                >
                  {{ item }}
                </Tag>
              </div>
            </template>
            <template v-if="column.dataIndex === 'accessStrategyName'">
              <span>{{ record.accessStrategyName }}</span>
            </template>
            <template v-if="column.dataIndex === 'abilityPermissionList'">
              <div style="display: flex; flex-direction: column; align-items: center">
                <Tag
                  v-for="item in record.abilityPermissionList"
                  :key="item"
                  style="margin: 2px; width: fit-content"
                  color="purple"
                >
                  {{ item }}
                </Tag>
              </div>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <Button
                type="primary"
                color="edit"
                preIcon="ant-design:edit-twotone"
                :iconSize="16"
                title="编辑"
                @click="edit(record)"
              >
                编辑
              </Button>
            </template>
          </template>
        </BasicTable>
        <Edit @register="register" ref="refRouteEditor" />
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { InputSearch, Tag } from 'ant-design-vue';
  import { PageWrapper } from '/@/components/Page';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from './routeTableData';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Button } from '/@/components/Button';
  import { apiGetPathList } from '/@/api/route/route';
  import { routeQueryParamsModel } from '/@/api/route/routeModel';
  import Edit from './Edit.vue';
  import { useModal } from '/@/components/Modal';

  export default defineComponent({
    components: {
      PageWrapper,
      BasicTable,
      InputSearch,
      Button,
      Edit,
      Tag,
    },
    setup() {
      const loading = ref(false);
      const tableData = ref<any>([]);
      const total = ref(0);
      const tableHeight = ref<Number>(getTableHeight(document));
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: getBasicColumns(),
        bordered: true,
      });
      const setPaginationInfo = () => {
        setPagination({
          total: total.value,
          pageSize: params.pageSize,
          current: params.pageIndex + 1,
        });
      };
      const params: routeQueryParamsModel = reactive<routeQueryParamsModel>({
        searchText: '',
        pageSize: 10,
        pageIndex: 0,
        draw: 1,
        category: null,
        accessStrategy: null,
      });
      const [register, { openModal }] = useModal();
      const getRouteList = () => {
        apiGetPathList(params)
          .then((res) => {
            if (res.code === 200) {
              total.value = res.data.filterCount;
              tableData.value = res.data.data;
              setPaginationInfo();
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
              description: '网络异常',
            });
          })
          .finally(() => {
            setLoading(false);
          });
      };
      getRouteList();
      return {
        loading,
        total,
        tableData,
        tableHeight,
        ...toRefs(params),
        registerTable,
        setPaginationInfo,
        setLoading,
        getRouteList,
        register,
        openModal,
      };
    },
    methods: {
      onSearch() {
        this.init();
        this.pageIndex = 0;
        this.getRouteList();
      },
      init() {
        this.setLoading(true);
        this.draw += 1;
        this.total = 0;
      },
      onChange(pageInfo, filters) {
        this.init();
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.category = null;
        if (filters['categoryName'] && filters['categoryName'][0]) {
          this.category = filters['categoryName'][0];
        }
        this.accessStrategy = null;
        if (filters['accessStrategyName'] && filters['accessStrategyName'][0]) {
          this.accessStrategy = filters['accessStrategyName'][0];
        }
        this.getRouteList();
      },
      edit(route) {
        this.openModal(true, route);
      },
    },
  });
</script>

<style lang="less" scoped>
  ::v-deep(.zebra-highlight) {
    background: #fafafa;
  }
</style>
