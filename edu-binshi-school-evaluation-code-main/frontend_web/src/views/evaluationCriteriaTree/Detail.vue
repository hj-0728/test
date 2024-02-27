<template>
  <div class="evaluation-criteria-detail">
    <Loading :loading="loading" :absolute="true" />
    <template v-if="!loading">
      <template v-if="!evaluationCriteriaTree">
        <div v-if="evaluationCriteria?.status === 'PUBLISHED'">
          <Icon icon="ph:info" color="#4278ba" size="26" style="position: relative; top: 2px" />
          <span style="margin-left: 9px; font-size: 20px; color: #f00">
            评价标准已发布，不可修改评价项。
          </span>
        </div>
        <div>
          <Icon icon="ph:info" color="#4278ba" size="26" style="position: relative; top: 2px" />
          <span style="margin-left: 9px; font-size: 20px"> 点击最小子节点查看详情。</span>
        </div>
        <div>
          <Icon icon="ph:info" color="#4278ba" size="26" style="position: relative; top: 2px" />
          <span style="margin-left: 9px; font-size: 20px">
            按住鼠标左键可在同一父节点下拖动排序。
          </span>
        </div>
        <div style="margin-left: 5px">
          <Icon icon="ph:ruler-bold" color="#58a76e" size="20" />
          <span style="margin-left: 9px; font-size: 20px"> 指标 </span>
        </div>
        <div style="margin-left: 5px">
          <SvgIcon name="standard" size="20" />
          <span style="margin-left: 9px; font-size: 20px"> 评价项 </span>
        </div>
      </template>
      <div v-else>
        <div class="title-content">
          {{ evaluationCriteriaTree.name }}
        </div>

        <DetailDescriptions :evaluationCriteriaTree="evaluationCriteriaTree"/>
        <Button
          type="primary"
          color="success"
          :iconSize="18"
          preIcon="ant-design:plus-outlined"
          class="ant-btn-left-margin"
          title="添加"
          @click="addAggregatedBenchmark"
          >添加综合评价
        </Button>
        <Button
          type="primary"
          color="success"
          :iconSize="18"
          preIcon="ant-design:plus-outlined"
          class="ant-btn-left-margin"
          title="添加"
          @click="addAggregatedBenchmark"
          >添加等级评价
        </Button>
        <!--        <div class="content">-->
        <!--          <div>-->
        <!--            <div>-->
        <!--              <Icon-->
        <!--                icon="mdi:arrow-down-thin-circle-outline"-->
        <!--                size="24"-->
        <!--                color="#0960bd"-->
        <!--                style="position: relative; top: 2px"-->
        <!--              />-->
        <!--              <span style="margin-left: 10px; color: #0960bd">-->
        <!--                <text class="item-title">最小分值：</text>-->
        <!--                <text class="item-number">-->
        <!--                  {{ evaluationCriteriaTree.benchmark.minScore }}-->
        <!--                </text>-->
        <!--              </span>-->
        <!--            </div>-->
        <!--            <div style="height: 30px"></div>-->
        <!--            <div>-->
        <!--              <Icon-->
        <!--                icon="mdi:arrow-up-thin-circle-outline"-->
        <!--                size="24"-->
        <!--                color="#009a61"-->
        <!--                style="position: relative; top: 2px"-->
        <!--              />-->
        <!--              <span style="margin-left: 10px; color: #009a61">-->
        <!--                <text class="item-title">最大分值：</text>-->
        <!--                <text class="item-number">-->
        <!--                  {{ evaluationCriteriaTree.benchmark.maxScore }}-->
        <!--                </text>-->
        <!--              </span>-->
        <!--            </div>-->
        <!--          </div>-->
        <!--        </div>-->
      </div>
    </template>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { Icon, SvgIcon } from '/@/components/Icon';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { apiGetEvaluationCriteriaTreeDetail } from '/@/api/evaluationCriteriaTree/evaluationCriteriaTree';
  import { Button } from 'ant-design-vue';
  import { Loading } from '/@/components/Loading';
  import DetailDescriptions
    from "/@/views/evaluationCriteriaTree/components/DetailDescriptions.vue";

  export default defineComponent({
    components: {
      Icon,
      Button,
      Loading,
      SvgIcon,
      DetailDescriptions,
    },
    props: {
      evaluationCriteriaTreeId: {
        type: String,
        default: null,
      },
    },
    setup() {
      const loading = ref(false);
      const evaluationCriteriaTree = ref();
      const evaluationCriteria = ref();
      return {
        evaluationCriteriaTree,
        evaluationCriteria,
        loading,
      };
    },
    mounted() {
      this.getEvaluationCriteriaTreeDetail();
    },
    methods: {
      getEvaluationCriteriaTreeDetail() {
        if (this.$props.evaluationCriteriaTreeId) {
          this.loading = true;
          apiGetEvaluationCriteriaTreeDetail(this.$props.evaluationCriteriaTreeId)
            .then((res) => {
              console.log('getEvaluationCriteriaTreeDetail ...');
              console.log(res);
              if (res.code === 200) {
                this.evaluationCriteriaTree = res.data;
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
                description: ErrorNotificationEnum.networkExceptionMsg,
              });
            })
            .finally(() => {
              this.loading = false;
            });
        }
      },
    },
  });
</script>

<style scoped lang="less">
  .evaluation-criteria-detail {
    padding: 16px;
    width: 100%;
    height: calc(100vh - 80px);
    overflow-y: auto;

    .title-content {
      font-size: 20px;
      font-weight: 700;
      color: #5f9f9f;
      padding: 10px 0;
      text-align: center;
    }

    .comments-content {
      font-size: 20px;
      font-weight: 700;
      color: #5f9f9f;
      padding: 30px 0;
      text-align: center;
    }

    .item-title {
      font-size: 18px;
    }

    .item-number {
      font-weight: 700;
      font-size: 20px;
      color: #5d5d5d;
    }

    .content {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 30px 0;
    }
  }
</style>
