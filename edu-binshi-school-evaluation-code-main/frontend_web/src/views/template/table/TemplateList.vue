<template>
  <PageWrapper title="模板管理">
    <div>
      <BasicTable
        :dataSource="tableData"
        @register="registerTable"
        :showIndexColumn="false"
        :loading="loading"
        bordered
        @change="onChange"
      >
        <template #tableTitle>
          <InputSearch
            v-model:value="params.searchText"
            placeholder="搜索"
            enter-button
            @search="onSearch"
            style="padding: 10px 0 10px 0; width: 30%"
          />
        </template>
        <template #toolbar>
          <Dropdown>
            <template #overlay>
              <Menu>
                <MenuItem key="1">
                  <Icon icon="ion:settings-outline" :size="16" style="margin-right: 5px" />
                  1st menu item
                </MenuItem>
                <MenuItem key="2">
                  <Icon icon="ion:settings-outline" :size="16" style="margin-right: 5px" />
                  2nd menu item
                </MenuItem>
                <MenuItem key="3">
                  <Icon icon="ion:settings-outline" :size="16" style="margin-right: 5px" />
                  3rd item
                </MenuItem>
              </Menu>
            </template>
            <Button :iconSize="18" title="Button"
              >Button<Icon icon="ion:ios-arrow-down" :size="16"
            /></Button>
          </Dropdown>
          <Button
            type="primary"
            color="success"
            :iconSize="18"
            preIcon="ant-design:plus-outlined"
            class="ant-btn-left-margin"
            title="添加"
            @click="addTemplate"
            >添加</Button
          >
          <Button
            type="primary"
            color="purple"
            :iconSize="18"
            preIcon="ph:download-simple"
            class="ant-btn-left-margin"
            title="导出"
            @click="addTemplate"
            >导出</Button
          >
        </template>
        <template #is_activated="{ record }">
          <Switch
            v-model:checked="record.is_activated"
            @change="handleChange(record)"
            checked-children="已启用"
            un-checked-children="已禁用"
          />
        </template>
        <template #operation="{ record }">
          <!-- 一般情况下查看和编辑只会出现一种，因此底色使用相同色 -->
          <!-- <Button
            type="primary"
            preIcon="ant-design:eye-outlined"
            :iconSize="16"
            @click="edit(record)"
            color="edit"
          >
            查看
          </Button> -->
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
          <Button
            type="primary"
            color="error"
            :iconSize="16"
            preIcon="mi:delete"
            class="ant-btn-left-margin"
            title="删除"
            @click="deleteTemplate(record)"
          >
            删除
          </Button>
          <Button
            type="primary"
            :iconSize="16"
            preIcon="ion:settings-outline"
            class="ant-btn-left-margin"
            title="设置"
            @click="deleteTemplate(record)"
          >
            设置
          </Button>
          <Button
            type="primary"
            color="orange"
            :iconSize="16"
            preIcon="ion:settings-outline"
            class="ant-btn-left-margin"
            title="备用1"
            @click="deleteTemplate(record)"
          >
            备用1
          </Button>
          <Button
            type="primary"
            color="blue"
            :iconSize="16"
            preIcon="ion:settings-outline"
            class="ant-btn-left-margin"
            title="备用2"
            @click="deleteTemplate(record)"
          >
            备用2
          </Button>
          <Button
            type="primary"
            color="green"
            :iconSize="16"
            preIcon="ion:settings-outline"
            class="ant-btn-left-margin"
            title="备用备用"
            @click="deleteTemplate(record)"
          >
            备用备用
          </Button>
        </template>
      </BasicTable>
      <TemplateAddModel @register="registerModel" />
    </div>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive, ref } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { Button } from '/@/components/Button';
  import { getBasicColumns, getBasicData } from './tableData';
  import { apiGetTemplateList } from '/@/api/template/template.ts';
  import { BasicPageQueryParamsModel } from '/@/api/model/baseModel.ts';
  import { Switch, InputSearch, Dropdown, Menu } from 'ant-design-vue';
  import TemplateAddModel from '../model/TemplateAddModel.vue';
  import { useModal } from '/@/components/Modal';
  import { PageWrapper } from '/@/components/Page';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Icon } from '/@/components/Icon';
  import { useI18n } from '/@/hooks/web/useI18n';
  export default defineComponent({
    components: {
      BasicTable,
      Switch,
      InputSearch,
      Button,
      TemplateAddModel,
      PageWrapper,
      Dropdown,
      Menu,
      MenuItem: Menu.Item,
      Icon,
    },
    setup() {
      const tableData = ref([]);
      const params: BasicPageQueryParamsModel = reactive({
        searchText: '',
        pageSize: 10,
        pageIndex: 0,
        draw: 1,
      });
      const total = ref(0);
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: getBasicColumns(),
      });

      const getTemplateList = () => {
        tableData.value = getBasicData();
        apiGetTemplateList(params)
          .then((res) => {
            if (res.code === 200) {
              total.value = res.data.length;
              // tableData.value = res.data.slice(
              //   params.pageIndex,
              //   params.pageIndex + params.pageSize,
              // );

              setPaginationInfo();
            }
          })
          .finally(() => {
            setLoading(false);
          });
      };
      getTemplateList();

      const [registerModel, { openModal }] = useModal();

      const { t } = useI18n();
      const setPaginationInfo = () => {
        setPagination({
          current: params.currentPage,
          total: total,
          pageSize: params.pageSize,
        });
      };
      const loading = ref(true);
      return {
        registerTable,
        tableData,
        params,
        registerModel,
        openModal,
        t,
        getTemplateList,
        setPaginationInfo,
        total,
        loading,
        setLoading,
      };
    },
    methods: {
      addTemplate() {
        this.openModal(true, true);
      },
      onSearch() {},
      edit() {},
      deleteTemplate() {
        useMessage().createConfirm({
          iconType: 'warning',
          title: this.t('sys.confirm.deleteTitle'),
          content: this.t('sys.confirm.deleteContent'),
        });
      },
      init() {
        this.params.currentPage = 1;
        this.params.draw += 1;
        this.loading = true;
        this.total = 0;
      },
      onChange(pageInfo) {
        this.init();
        this.params.pageSize = pageInfo.pageSize;
        this.params.pageIndex = (pageInfo.current - 1) * pageInfo.pageSize;
        this.params.currentPage = pageInfo.current;
        console.log(this.params);
        this.setLoading(true);
        this.getTemplateList();
      },
    },
  });
</script>
<style scoped></style>
