<template>
  <div>
    <span style="padding: 0 10px"
      ><ProfileOutlined /> <label class="select-label">评价计划</label>
    </span>
    <Select
      ref="select"
      style="width: 40%"
      v-model:value="evaluationCriteriaPlanId"
      :options="evaluationCriteriaPlanList"
      :searchValue="planParams.searchText"
      @change="evaluationCriteriaPlanChange"
      :fieldNames="{ label: 'name', value: 'id' }"
      :maxTagCount="1"
      :maxTagTextLength="5"
      :placeholder="placeholder"
      show-search
      :filter-option="false"
      @search="handleInput"
      :autoClearSearchValue="false"
      @focus="focusSelect"
      @blur="blurSelect"
    >
      <template #dropdownRender="{ menuNode: menu }">
        <div
          style="
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: 9;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f9fafb50;
          "
          v-if="evaluationCriteriaPlanLoading"
        >
          <Spin v-if="evaluationCriteriaPlanLoading" />
        </div>
        <VNodes :vnodes="menu" />
        <Divider
          style="margin: 4px 0"
          v-if="evaluationCriteriaPlanList.length < evaluationCriteriaPlanFilterTotal"
        />
        <div
          @mousedown="(e) => e.preventDefault()"
          style="text-align: center; color: #1890ff"
          v-if="evaluationCriteriaPlanList.length < evaluationCriteriaPlanFilterTotal"
          @click="loadMoreEvaluationCriteriaPlan"
        >
          <div style="cursor: pointer">加载更多</div>
        </div>
      </template>
    </Select>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref } from 'vue';
  import { Divider, Select, Spin } from 'ant-design-vue';
  import { ProfileOutlined } from '@ant-design/icons-vue';
  import { apiGetEvaluationPlanList } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { usePeriodStore } from '/@/store/modules/period';
  import { cloneDeep } from 'lodash-es';

  export default defineComponent({
    components: {
      ProfileOutlined,
      Spin,
      Select,
      Divider,
      VNodes: (_, { attrs }) => {
        return attrs.vnodes;
      },
    },
    emits: ['selectPlanId', 'selectPlanCallback'],
    setup() {
      const evaluationCriteriaPlanLoading = ref(false);
      const evaluationCriteriaPlanList = ref<object[]>([]);
      const evaluationCriteriaPlanFilterTotal = ref(0);
      const evaluationCriteriaPlanId = ref<String | null>(null);
      const searchValue = ref('');
      const isBlur = ref(false);
      const planParams = reactive({
        searchText: '', //搜索框中的内容
        pageSize: 20, //页面显示条数
        pageIndex: 0, //当前显示的第几页
        draw: 1, //默认显示第一页
        statusList: ['PUBLISHED', 'ARCHIVED'], //状态筛选列表
        finished: true, //已完成的
        isCurrentPeriod: true, // 是否只获取当前选择的周期的计划
      });
      const placeholder = ref('选择评价标准进行过滤');

      const debounceTimer = ref();
      return {
        evaluationCriteriaPlanLoading,
        evaluationCriteriaPlanList,
        evaluationCriteriaPlanFilterTotal,
        planParams,
        evaluationCriteriaPlanId,
        placeholder,
        debounceTimer,
        searchValue,
        isBlur,
      };
    },
    computed: {
      periodId() {
        return usePeriodStore().getPeriodId;
      },
    },
    watch: {
      periodId(newVal, oldVal) {
        if (newVal !== oldVal && oldVal) {
          this.initPlan();
        }
      },
    },
    mounted() {
      this.getEvaluationCriteriaPlan();
    },
    methods: {
      getEvaluationCriteriaPlan() {
        this.evaluationCriteriaPlanLoading = true;
        apiGetEvaluationPlanList(this.planParams)
          .then((res) => {
            if (res.code === 200 && this.planParams.draw === res.data.draw) {
              this.evaluationCriteriaPlanFilterTotal = res.data.filterCount;
              this.evaluationCriteriaPlanList.push(...res.data.data);
              if (res.data.filterCount === 0) {
                this.placeholder = '暂无数据';
                if (!this.evaluationCriteriaPlanId) {
                  this.$emit('selectPlanId', null);
                  this.$emit('selectPlanCallback', null);
                }
              } else {
                if (!this.evaluationCriteriaPlanId) {
                  this.evaluationCriteriaPlanId = this.evaluationCriteriaPlanList[0].id;
                  this.$emit('selectPlanId', this.evaluationCriteriaPlanList[0].id);
                  this.$emit('selectPlanCallback', this.evaluationCriteriaPlanList[0]);
                }
                this.planParams.pageIndex += 1;
              }
              this.planParams.draw += 1;
            }
            if (res.code !== 200) {
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
            this.evaluationCriteriaPlanLoading = false;
          });
      },
      evaluationCriteriaPlanChange(_value, option) {
        this.planParams.searchText = cloneDeep(this.searchValue);
        if (this.evaluationCriteriaPlanId) {
          this.$emit('selectPlanId', this.evaluationCriteriaPlanId);
          this.$emit('selectPlanCallback', option);
        }
      },
      searchEvaluationCriteriaPlan(searchText) {
        this.planParams.pageIndex = 0;
        this.planParams.searchText = searchText;
        if (!this.isBlur) {
          this.searchValue = cloneDeep(searchText);
        }
        console.log('searchEvaluationCriteriaPlan');
        console.log(this.searchValue);
        this.evaluationCriteriaPlanList = [];
        this.evaluationCriteriaPlanFilterTotal = 0;
        this.getEvaluationCriteriaPlan();
      },
      handleInput(searchText) {
        clearTimeout(this.debounceTimer);

        this.debounceTimer = setTimeout(() => {
          this.searchEvaluationCriteriaPlan(searchText);
        }, 100);
      },
      loadMoreEvaluationCriteriaPlan() {
        this.getEvaluationCriteriaPlan();
      },
      initPlan() {
        this.planParams.pageIndex = 0;
        this.planParams.searchText = '';
        this.evaluationCriteriaPlanList = [];
        this.evaluationCriteriaPlanFilterTotal = 0;
        this.evaluationCriteriaPlanId = null;
        this.getEvaluationCriteriaPlan();
      },
      focusSelect() {
        console.log('focusSelect');
        console.log(this.searchValue);
        this.planParams.searchText = cloneDeep(this.searchValue);
        this.isBlur = false;
      },
      blurSelect() {
        console.log('blurSelect');
        this.isBlur = true;
      },
    },
  });
</script>
