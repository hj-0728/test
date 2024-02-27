<template>
  <div class="select-item-wrapper">
    <span> <ProfileOutlined /> <label class="select-label">周期类型</label> </span>
    <Select
      v-model:value="periodCategory"
      :options="periodCategoryList"
      placeholder="请选择周期类型"
      style="min-width: 150px"
      @change="onChangePeriodCategory"
      :allowClear="false"
    />
  </div>
  <div class="select-item-wrapper">
    <span> <ClockCircleOutlined /> <label class="select-label">周期</label> </span>
    <Select
      :disabled="periodItemDisabled"
      :options="periodList"
      v-model:value="periodInfoId"
      style="min-width: 250px"
      placeholder="请选择周期"
      @change="onChangePeriod"
      :allowClear="false"
      :fieldNames="{ label: 'name', value: 'id' }"
    />
  </div>
</template>

<script lang="ts">
  import { Select } from 'ant-design-vue';
  import { ClockCircleOutlined, ProfileOutlined } from '@ant-design/icons-vue';
  import { defineComponent, ref } from 'vue';
  import { PeriodCategoryEnum } from '/@/enums/periodCategoryEnum';
  import {
    apiGetCurrentPeriod,
    apiGetPeriodListByCategory,
    apiChangeCurrentPeriod,
  } from '/@/api/period/period';
  import { usePeriodStoreWithOut } from '/@/store/modules/period';
  export default defineComponent({
    name: 'SelectPeriod',
    components: {
      Select,
      ClockCircleOutlined,
      ProfileOutlined,
    },
    setup() {
      const periodList = ref([]);
      const enumToDictionary = (enumObj: any) => {
        return Object.keys(enumObj).map((key) => ({
          value: key,
          label: enumObj[key],
        }));
      };
      const periodCategoryList = enumToDictionary(PeriodCategoryEnum);
      const periodCategory = ref('');
      const periodItemDisabled = ref(false);
      const periodInfo = ref({});
      const periodInfoId = ref('');
      return {
        periodCategory,
        periodItemDisabled,
        periodList,
        periodCategoryList,
        periodInfo,
        periodInfoId,
      };
    },
    created() {
      this.getCurrentPeriod();
    },
    methods: {
      getCurrentPeriod() {
        apiGetCurrentPeriod().then((res) => {
          if (res.code === 200) {
            this.periodInfo = res.data;
            this.periodCategory = res.data.categoryCode;
            this.changePeriodStore({
              id: this.periodInfo.id,
              name: this.periodInfo.name,
              periodCategory: this.periodCategory,
            });
            this.getPeriodList(false);
            this.periodInfoId = res.data.id;
            this.periodList = [res.data];
          }
        });
      },
      getPeriodList(isUpdatePeriod) {
        apiGetPeriodListByCategory(this.periodCategory).then((res) => {
          if (res.code === 200) {
            this.periodList = res.data;
            if (isUpdatePeriod) {
              this.periodInfo = res.data[0];
              this.periodInfoId = res.data[0].id;
              this.changeCurrentPeriod();
            }
          }
        });
      },
      onChangePeriodCategory(value, _option) {
        this.periodItemDisabled = !value;
        this.getPeriodList(true);
      },
      onChangePeriod(_value, option) {
        this.periodInfo = option;
        this.changeCurrentPeriod();
      },
      changeCurrentPeriod() {
        let params = {
          id: this.periodInfo.id,
          name: this.periodInfo.name,
          categoryCode: this.periodCategory,
        };
        apiChangeCurrentPeriod(params).then((res) => {
          if (res.code === 200) {
            console.log('修改成功');
            this.changePeriodStore(params);
          }
        });
      },
      changePeriodStore(periodInfo) {
        const periodStore = usePeriodStoreWithOut();
        periodStore.setPeriod(periodInfo);
      },
    },
  });
</script>

<style scoped lang="less">
  .select-label {
    color: black;
    margin-right: 10px;
  }

  .select-item-wrapper {
    margin: 0 10px 0 0;
  }
</style>
