<template>
  <div>
    <List :loading="loading" item-layout="horizontal" :data-source="tableData">
      <template #renderItem="{ item }">
        <ListItem>
          <Checkbox @change="onChange" v-model:checked="item.isSelected" :id="item.id">
            {{ item.name }}
          </Checkbox>
        </ListItem>
      </template>
    </List>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiGetEvaluationCriteriaBoundTagItemList } from '/@/api/evaluationCriteriaTree/evaluationCriteriaTree';
  import { List, ListItem, Checkbox } from 'ant-design-vue';
  export default defineComponent({
    components: {
      List,
      ListItem,
      Checkbox,
    },
    props: {
      evaluationCriteriaId: {
        type: String,
        default: '',
      },
      tagName: {
        type: String,
        default: '',
      },
      level: {
        type: Number,
        default: 1,
      },
      selected: {
        type: Boolean,
        default: false,
      },
    },
    emits: ['on-select-evaluation-criteria-item'],
    setup(props, { emit }) {
      const [registerEvaluationItemSelectModal, { openModal: openEvaluationItemSelectModal }] =
        useModal();
      const selectType = 'checkbox';
      const selectedEvaluationCriteriaItemKeys = ref<string[]>([]);
      const canSelectFirstLevel = ref(false);
      const canSelectSecondLevel = ref(false);
      const loading = ref(false);
      const tableData = ref([]);
      const needRefresh = ref(false);
      const params = reactive({
        evaluationCriteriaId: props.evaluationCriteriaId,
        tagName: props.tagName,
        level: props.level,
        isSelected: props.selected,
      });
      const getEvaluationCriteriaBoundTagItemPage = () => {
        if (props.evaluationCriteriaId) {
          loading.value = true;
          console.log(params, 'params.isSelected');
          selectedEvaluationCriteriaItemKeys.value = [];
          apiGetEvaluationCriteriaBoundTagItemList(params)
            .then((res) => {
              if (res.code === 200) {
                tableData.value = res.data;
                selectedEvaluationCriteriaItemKeys.value = [];
                emit(
                  'on-select-evaluation-criteria-item',
                  selectedEvaluationCriteriaItemKeys.value,
                );
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
        }
      };
      getEvaluationCriteriaBoundTagItemPage();
      return {
        loading,
        selectedEvaluationCriteriaItemKeys,
        selectType,
        ...toRefs(params),
        params,
        tableData,
        getEvaluationCriteriaBoundTagItemPage,
        registerEvaluationItemSelectModal,
        openEvaluationItemSelectModal,
        canSelectFirstLevel,
        canSelectSecondLevel,
        needRefresh,
      };
    },
    methods: {
      onChange(data) {
        this.onSelect(data['target']);
      },
      onRowClick(record, _index, _event) {
        console.log('onRowClick');
        this.onSelect(record);
      },
      onSelectAll(_selected, _selectedRows, changeRows) {
        console.log('onSelectAll');
        for (const row of changeRows) {
          this.selectEvaluationCriteriaTree(row);
        }
      },
      onSelect(record) {
        this.selectEvaluationCriteriaTree(record);
      },
      selectEvaluationCriteriaTree(row) {
        console.log(row, 'row');
        const idx = this.selectedEvaluationCriteriaItemKeys.indexOf(row.id);
        if (idx < 0) {
          if (this.selectType === 'radio') {
            this.selectedEvaluationCriteriaItemKeys = [row.id];
          } else {
            this.selectedEvaluationCriteriaItemKeys.push(row.id);
          }
        } else {
          this.selectedEvaluationCriteriaItemKeys.splice(idx, 1);
        }
        this.$emit('on-select-evaluation-criteria-item', this.selectedEvaluationCriteriaItemKeys);
      },
    },
  });
</script>

<style scoped lang="less">
  ::v-deep(.vben-basic-table-header__toolbar) {
    margin-right: 0;
  }
</style>
