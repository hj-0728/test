<template>
  <div style="min-height: 200px; width: 100%">
    <Empty class="empty-info" v-if="isNotData" :image="simpleImage" />
    <div v-show="!isNotData && !loading">
      <div
        v-show="benchmarkInfo && benchmarkInfo.valueType === 'STRING' && echartsType === 'DEPT'"
        id="echarts-container-dept-string"
        ref="echartsContainerDeptString"
        class="echarts-dept"
      ></div>
      <div
        v-show="benchmarkInfo && benchmarkInfo.valueType === 'NUM' && echartsType === 'DEPT'"
        id="echarts-container-dept-num"
        ref="echartsContainerDeptNum"
        class="echarts-dept"
      ></div>
      <div
        v-show="echartsType === 'STUDENT'"
        id="echarts-container-student"
        ref="echartsContainerStudent"
        class="echarts-student"
      ></div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import * as echarts from 'echarts';
  import { EChartsType } from 'echarts';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiGetPlanBenchmarkStatistics } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlanStatistics';
  import { Empty } from 'ant-design-vue';
  export default defineComponent({
    components: { Empty },
    props: {
      planId: {
        type: String,
        default: null,
      },
      benchmark: {
        type: Object,
        default: null,
      },
      echartsType: {
        type: String,
        default: null,
      },
      gradeDimensionDeptTreeId: {
        type: String,
        default: null,
      },
    },
    emits: ['completeEcharts'],
    setup(props) {
      const loading = ref(true);
      const myChartDeptString = ref<EChartsType | null>(null);
      const myChartDeptNum = ref<EChartsType | null>(null);
      const myChartStudent = ref<EChartsType | null>(null);
      const evaluationCriteriaPlanId = ref(props.planId);
      const benchmarkInfo = ref(props.benchmark);
      const dimensionDeptTreeId = ref(props.gradeDimensionDeptTreeId);
      const isNotData = ref(false);
      return {
        loading,
        myChartDeptString,
        myChartDeptNum,
        myChartStudent,
        evaluationCriteriaPlanId,
        benchmarkInfo,
        dimensionDeptTreeId,
        simpleImage: Empty.PRESENTED_IMAGE_SIMPLE,
        isNotData,
      };
    },
    mounted() {
      this.isNotData = false;
      this.loading = true;
      console.log(this.benchmarkInfo);
      console.log(this.echartsType);
      if (this.benchmarkInfo?.valueType === 'STRING' && this.echartsType === 'DEPT') {
        this.initChartDeptString();
      } else if (this.benchmarkInfo?.valueType === 'NUM' && this.echartsType === 'DEPT') {
        this.initChartDeptNum();
      }
      if (this.echartsType === 'STUDENT') {
        this.initChartStudent();
      }
      this.$emit('completeEcharts');
    },
    methods: {
      async getStatisticsData(data) {
        this.loading = true;
        let statisticsData = null;
        this.isNotData = false;
        await apiGetPlanBenchmarkStatistics(data)
          .then((res) => {
            if (res.code === 200) {
              statisticsData = res.data;
              if (!res.data.statisticsInfo || res.data.statisticsInfo.length === 0) {
                this.isNotData = true;
              }
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
        return statisticsData;
      },
      async getDeptStringOptions() {
        const statisticsData = await this.getStatisticsData({
          benchmarkId: this.benchmarkInfo.id,
          evaluationCriteriaPlanId: this.evaluationCriteriaPlanId,
          statisticsObjectType: 'CLASS',
          dimensionDeptTreeIdList: [this.dimensionDeptTreeId],
        });
        console.log(statisticsData);
        const scoreSymbol = statisticsData?.scoreSymbolInfo;
        const scoreSymbolOptions = scoreSymbol.limitedStringOptions
          ? scoreSymbol.limitedStringOptions
          : scoreSymbol.stringOptions;
        let className = [];
        let deptScore = {};
        statisticsData?.statisticsInfo.forEach((value) => {
          className.push(value.name);
          value.stringDistributed.forEach((item) => {
            if (!deptScore[item.stringScore]) {
              deptScore[item.stringScore] = [];
            }
            deptScore[item.stringScore].push(item.count);
          });
        });
        let seriesList = [];
        scoreSymbolOptions.forEach((value) => {
          seriesList.push({
            name: value,
            type: 'bar',
            stack: 'total',
            label: {
              show: true,
            },
            emphasis: {
              focus: 'series',
            },
            data: deptScore[value],
          });
        });
        return {
          tooltip: {
            position: 'top',
          },
          legend: {},
          grid: {
            left: '3%',
            right: '5%',
            bottom: '3%',
            containLabel: true,
          },
          xAxis: {
            name: '人数',
            type: 'value',
            position: 'top',
            minInterval: 1,
            axisLine: {
              show: true,
            },
          },
          yAxis: {
            name: '班级名称',
            type: 'category',
            data: className,
          },
          series: seriesList,
        };
      },
      async initChartDeptString() {
        // @ts-ignore
        console.log('initChartDeptString');
        const options = await this.getDeptStringOptions();
        console.log(options);
        this.myChartDeptString = echarts.init(this.$refs.echartsContainerDeptString);
        this.myChartDeptString.setOption(options);
        //增加监听事件，使得ECharts自适应外部div大小
        // eslint-disable-next-line @typescript-eslint/no-this-alias
        window.addEventListener('resize', () => {
          setTimeout(() => {
            /*
             * 事实证明，让resize() 延迟一点执行
             * 可以解决执行太快，以至于浏览器还没反应过来导致自适应不调整的问题，
             * 比如从很小的窗口尺寸一下子切换到最大化
             *
             * 试过50ms, 太快了，浏览器没反应，所以这里用了100ms
             * */
            this.myChartDeptString?.resize();
          }, 100);
        });
      },
      async getDeptNumOptions() {
        const statisticsData = await this.getStatisticsData({
          benchmarkId: this.benchmarkInfo.id,
          evaluationCriteriaPlanId: this.evaluationCriteriaPlanId,
          statisticsObjectType: 'CLASS',
          dimensionDeptTreeIdList: [this.dimensionDeptTreeId],
        });
        console.log(statisticsData);
        let data = [];
        let avgData = [];
        statisticsData?.statisticsInfo.forEach((value) => {
          avgData.push(value.numericAvg);
          value.numericDistributed.forEach((item) => {
            data.push({
              className: value.name,
              numericScore: item.numericScore,
              count: item.count,
            });
          });
        });
        // 生成散点图的数据格式
        const scatterData = data.map((item) => [item.numericScore, item.className, item.count]);

        let classList = data.map((item) => item.className);

        // 配置项
        return {
          tooltip: {
            position: 'top',
          },
          legend: {},
          xAxis: {
            type: 'value',
            name: '评分', // X 轴名称
            minInterval: 1,
            position: 'top',
            axisLine: {
              show: true,
            },
          },
          yAxis: {
            type: 'category',
            name: '班级名称', // Y 轴名称
            data: [...new Set(classList)],
          },
          series: [
            {
              name: '评分分布',
              type: 'scatter',
              data: scatterData,
              symbolSize: function (data) {
                return Math.sqrt(data[2]) * 10; // 点的大小表示人数
              },
              label: {
                show: true,
                position: 'top',
                formatter: function (param) {
                  return param.data[2]; // 点上显示人数
                },
              },
              tooltip: {
                formatter: function (params) {
                  return `<b>${params.value[1]}</b><br/>评分为 <b>${params.value[0]}</b> 的有 <b>${params.value[0]}</b> 人`;
                },
              },
            },
            {
              name: '平均分',
              type: 'line',
              data: avgData,
            },
          ],
        };
      },
      async initChartDeptNum() {
        // @ts-ignore
        const options = await this.getDeptNumOptions();
        this.myChartDeptNum = echarts.init(this.$refs.echartsContainerDeptNum);
        this.myChartDeptNum.setOption(options);
        //增加监听事件，使得ECharts自适应外部div大小
        // eslint-disable-next-line @typescript-eslint/no-this-alias
        window.addEventListener('resize', () => {
          setTimeout(() => {
            /*
             * 事实证明，让resize() 延迟一点执行
             * 可以解决执行太快，以至于浏览器还没反应过来导致自适应不调整的问题，
             * 比如从很小的窗口尺寸一下子切换到最大化
             *
             * 试过50ms, 太快了，浏览器没反应，所以这里用了100ms
             * */
            this.myChartDeptNum?.resize();
          }, 100);
        });
      },
      async getStudentOptions() {
        const statisticsData = await this.getStatisticsData({
          benchmarkId: this.benchmarkInfo.id,
          evaluationCriteriaPlanId: this.evaluationCriteriaPlanId,
          statisticsObjectType: 'STUDENT',
        });
        const scoreSymbol = statisticsData?.scoreSymbolInfo;
        let scoreSymbolOptions = [];
        let singleAxis = {};
        let data = [];
        if (scoreSymbol.valueType === 'STRING') {
          scoreSymbolOptions = scoreSymbol.limitedStringOptions
            ? scoreSymbol.limitedStringOptions
            : scoreSymbol.stringOptions;
          singleAxis = {
            left: 80,
            type: 'category',
            boundaryGap: false,
            data: scoreSymbolOptions,
            height: '30%',
          };
        } else {
          singleAxis = {
            left: 80,
            type: 'value',
            boundaryGap: false,
            height: '30%',
            minInterval: 1,
          };
        }
        statisticsData?.statisticsInfo.forEach((value) => {
          if (scoreSymbolOptions.length > 0) {
            data.push([scoreSymbolOptions.indexOf(value.stringScore), value.count]);
          } else {
            data.push([value.numericScore, value.count]);
          }
        });
        console.log('数据-------------------------------');
        console.log(data);
        console.log(statisticsData);
        return {
          tooltip: {
            position: 'top',
          },
          title: {
            textBaseline: 'middle',
            text: '评价',
            top: '30%',
          },
          singleAxis: singleAxis,
          series: {
            singleAxisIndex: 0,
            coordinateSystem: 'singleAxis',
            type: 'scatter',
            data: data,
            symbolSize: function (dataItem) {
              return dataItem[1] * 8;
            },
            tooltip: {
              formatter: function (params) {
                if (params.name) {
                  return `获得 <b>${params.name}</b> 的有 <b>${params.value[1]}</b> 人`;
                } else {
                  return `评分为 <b>${params.value[0]}</b> 的有 <b>${params.value[1]}</b> 人`;
                }
              },
            },
          },
        };
      },
      async initChartStudent() {
        // @ts-ignore
        const options = await this.getStudentOptions();
        this.myChartStudent = echarts.init(this.$refs.echartsContainerStudent);
        this.myChartStudent.setOption(options);
        //增加监听事件，使得ECharts自适应外部div大小
        // eslint-disable-next-line @typescript-eslint/no-this-alias
        window.addEventListener('resize', () => {
          setTimeout(() => {
            /*
             * 事实证明，让resize() 延迟一点执行
             * 可以解决执行太快，以至于浏览器还没反应过来导致自适应不调整的问题，
             * 比如从很小的窗口尺寸一下子切换到最大化
             *
             * 试过50ms, 太快了，浏览器没反应，所以这里用了100ms
             * */
            this.myChartDeptNum?.resize();
          }, 100);
        });
      },
      async updateChart(planId, benchmark, dimensionDeptTreeId) {
        this.isNotData = false;
        this.loading = true;
        this.evaluationCriteriaPlanId = planId;
        this.benchmarkInfo = benchmark;
        this.dimensionDeptTreeId = dimensionDeptTreeId;
        if (this.benchmarkInfo?.valueType === 'STRING' && this.echartsType === 'DEPT') {
          console.log('111');
          console.log(this.myChartDeptString);
          if (this.myChartDeptString) {
            const options = await this.getDeptStringOptions();
            console.log('myChartDeptString');
            console.log(options);
            this.myChartDeptString.setOption(options);
          } else {
            console.log('222');
            await this.initChartDeptString();
          }
        } else if (this.benchmarkInfo?.valueType === 'NUM' && this.echartsType === 'DEPT') {
          if (this.myChartDeptNum) {
            const options = await this.getDeptNumOptions();
            this.myChartDeptNum.setOption(options);
          } else {
            await this.initChartDeptNum();
          }
        }
        if (this.echartsType === 'STUDENT') {
          if (this.myChartStudent) {
            const options = await this.getStudentOptions();
            this.myChartStudent.setOption(options);
          } else {
            await this.initChartStudent();
          }
        }
        this.$emit('completeEcharts');
      },
    },
  });
</script>

<style lang="less" scoped>
  .echarts-container {
    height: fit-content;
  }

  .echarts-dept {
    width: calc(100% - 8px);
    height: 500px;
    padding-right: 20px;
  }

  .echarts-student {
    width: calc(100% - 10px);
    height: 300px;
    padding: 60px 60px 0 0;
    margin: 0;
  }

  .empty-info {
    margin: 0 !important;
    padding: 32px 0;
  }
</style>
