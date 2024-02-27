<template>
  <div ref="evaluationAssignment">
    <Loading :loading="dataLoading" :absolute="true" />
    <PageWrapper :content-style="{ height: 'calc(100vh - 80px)' }">
      <div class="content">
        <Card
          style="height: calc(100vh - 80px)"
          class="card"
          :headStyle="{
            height: '30px',
            lineHeight: '10px',
            fontWeight: 'bold',
          }"
        >
          <template v-if="evaluationCriteriaPlan" #title>
            <div style="float: left">
              <Tag :color="colorData[evaluationCriteriaPlan.status]">
                {{ evaluationCriteriaPlan.statusName }}
              </Tag>
            </div>
            <div style="max-width: 70%; float: left; left: 30px">
              <Tooltip placement="bottomLeft">
                <template #title>{{ evaluationCriteriaPlan.name }}</template>
                <div class="evaluation-criteria-plan">
                  <div class="evaluation-criteria-plan-name">
                    {{ evaluationCriteriaPlan.name }}：
                  </div>
                  <span class="evaluation-criteria-plan-span">
                    {{
                      dayjs
                        .utc(evaluationCriteriaPlan.executedStartAt)
                        .local()
                        .format('YYYY-MM-DD HH:mm')
                    }}
                    -
                    {{
                      dayjs
                        .utc(evaluationCriteriaPlan.executedFinishAt)
                        .local()
                        .format('YYYY-MM-DD HH:mm')
                    }}
                  </span>
                </div>
              </Tooltip>
            </div>
          </template>
          <template #extra>
            <div style="margin-top: -10px">
              <InputSearch
                placeholder="搜索"
                enter-button
                style="width: 100%"
                v-model:value="searchText"
                @search="onSearch"
              />
            </div>
          </template>
          <div class="evaluation-assignment-content">
            <List
              item-layout="horizontal"
              :data-source="evaluationAssignmentTodoList"
              style="padding: 10px"
            >
              <template v-if="firstLoading">
                <Skeleton avatar :paragraph="{ rows: 4 }" />
              </template>
              <template #renderItem="{ item }">
                <Skeleton avatar :title="false" :loading="loading" active>
                  <ListItem>
                    <template #actions>
                      <Button
                        v-if="canEvaluation === true"
                        type="primary"
                        color="edit"
                        :iconSize="16"
                        title="评价"
                        preIcon="solar:branching-paths-up-broken"
                        @click="evaluation(item)"
                      >
                        评价
                      </Button>
                      <Button
                        v-if="canEvaluation === false"
                        type="primary"
                        color="info"
                        :iconSize="16"
                        title="查看"
                        preIcon="ant-design:eye-outlined"
                        @click="evaluation(item)"
                      >
                        查看
                      </Button>
                    </template>
                    <ListItemMeta>
                      <template #avatar>
                        <Avatar :src="item.avatarUrl ? item.avatarUrl : defaultAvatar" :size="50" />
                      </template>
                      <template #title>
                        <div style="margin-top: 10px">
                          <span style="font-weight: bold; font-size: 15px">{{
                            item.peopleName
                          }}</span>
                          <Tag style="margin-left: 10px; line-height: 24px" color="blue">
                            {{ item.deptName }}
                          </Tag>
                        </div>
                      </template>
                    </ListItemMeta>
                    <div>
                      <span>
                        <Tag style="margin-left: 5px; line-height: 24px" color="green">
                          已填写：{{ item.fillCount }}
                        </Tag>
                      </span>
                      <span style="margin-left: 40px">
                        <Tag style="margin-left: 10px; line-height: 24px" color="pink">
                          未填写：{{ item.notFillCount }}
                        </Tag>
                      </span>
                    </div>
                  </ListItem>
                </Skeleton>
              </template>
            </List>
            <div style="width: 100%; text-align: center; margin-top: 20px" v-if="total > 0">
              <Button
                @click="onLoadMore"
                :loading="loading"
                v-if="evaluationAssignmentTodoList.length < total && !loading"
              >
                加载更多
              </Button>
              <div v-else-if="evaluationAssignmentTodoList.length == total" style="color: #bfbfcd">
                <div>没有更多了</div>
              </div>
              <div style="height: 20px"></div>
            </div>
          </div>
        </Card>
      </div>
    </PageWrapper>
    <EvaluationRecord @register="registerEvaluationRecord" @refresh="refreshEvaluationAssignment" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { Input, Card, List, Skeleton, Tag, Avatar, Tooltip } from 'ant-design-vue';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { PageWrapper } from '/@/components/Page';
  import { apiGetEvaluationAssignmentTodoList } from '/@/api/evaluationAssignment/evaluationAssignment';
  import { useRoute } from 'vue-router';
  import defaultAvatar from '/@/assets/images/defaultAvatar.png';
  import dayjs from 'dayjs';
  import utc from 'dayjs/plugin/utc';
  import { useModal } from '/@/components/Modal';
  import EvaluationRecord from '/src/components/EvaluationRecord/Index.vue';
  import { evaluationCriteriaPlanStatusEnum } from '/@/enums/bizEnum';
  import { apiGetEvaluationCriteriaPlanInfo } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { Button } from '/@/components/Button';
  import { colorData } from '/@/utils/helper/common';
  import { Loading } from '/@/components/Loading';

  export default defineComponent({
    components: {
      Loading,
      Tooltip,
      PageWrapper,
      InputSearch: Input.Search,
      Card,
      List,
      ListItem: List.Item,
      ListItemMeta: List.Item.Meta,
      Skeleton,
      Tag,
      Avatar,
      Button,
      EvaluationRecord,
    },
    setup() {
      const route = useRoute();
      dayjs.extend(utc);

      const evaluationAssignmentTodoList = ref([]);
      const loading = ref(true);
      const firstLoading = ref(true);
      const dataLoading = ref(true);
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document));
      const params = reactive({
        pageSize: 50,
        pageIndex: 0,
        searchText: '',
        draw: 1,
        capacityCodeList: [],
        evaluationCriteriaPlanId: route.params.evaluationCriteriaPlanId,
      });
      const canEvaluation = ref<boolean | null>(false);
      const evaluationCriteriaPlan = reactive({
        name: '',
        executedStartAt: '',
        executedFinishAt: '',
        status: '',
        statusName: '',
      });

      const getEvaluationCriteriaPlanInfo = () => {
        apiGetEvaluationCriteriaPlanInfo(route.params.evaluationCriteriaPlanId)
          .then((res) => {
            if (res.code === 200) {
              evaluationCriteriaPlan.name = res.data.name;
              evaluationCriteriaPlan.executedStartAt = res.data.executedStartAt;
              evaluationCriteriaPlan.executedFinishAt = res.data.executedFinishAt;
              if (
                res.data.status === evaluationCriteriaPlanStatusEnum.PUBLISHED &&
                dayjs(evaluationCriteriaPlan.executedFinishAt) < dayjs()
              ) {
                evaluationCriteriaPlan.status = evaluationCriteriaPlanStatusEnum.ARCHIVED;
                evaluationCriteriaPlan.statusName = '已归档';
              } else if (
                res.data.status === evaluationCriteriaPlanStatusEnum.PUBLISHED &&
                dayjs(evaluationCriteriaPlan.executedFinishAt) > dayjs() &&
                dayjs() >= dayjs(evaluationCriteriaPlan.executedStartAt)
              ) {
                evaluationCriteriaPlan.status = evaluationCriteriaPlanStatusEnum.IN_PROGRESS;
                evaluationCriteriaPlan.statusName = '进行中';
              } else {
                evaluationCriteriaPlan.status = res.data.status;
                evaluationCriteriaPlan.statusName = res.data.statusName;
              }
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((err) => {
            console.log(`error: ${err}`);
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络异常',
            });
          })
          .finally(() => {});
      };
      getEvaluationCriteriaPlanInfo();

      const getEvaluationAssignmentTodoList = () => {
        apiGetEvaluationAssignmentTodoList(params)
          .then((res) => {
            if (res.code === 200 && params.draw === res.data.draw) {
              if (
                res.data.data.length > 0 &&
                res.data.data[0].planStatus == evaluationCriteriaPlanStatusEnum.IN_PROGRESS
              ) {
                canEvaluation.value = true;
              }
              total.value = res.data.filterCount;
              evaluationAssignmentTodoList.value = evaluationAssignmentTodoList.value.concat(
                res.data.data,
              );
              params.draw++;
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
            firstLoading.value = false;
            dataLoading.value = false;
          });
      };
      getEvaluationAssignmentTodoList();

      const [registerEvaluationRecord, { openModal: openEvaluationRecordModal }] = useModal();

      const debounceTimer = ref();

      return {
        evaluationAssignmentTodoList,
        loading,
        firstLoading,
        total,
        tableHeight,
        params,
        defaultAvatar,
        canEvaluation,
        evaluationCriteriaPlan,
        colorData,
        registerEvaluationRecord,
        openEvaluationRecordModal,
        ...toRefs(params),
        getEvaluationAssignmentTodoList,
        dayjs,
        debounceTimer,
        dataLoading,
      };
    },
    methods: {
      onSearch(value) {
        if (this.dataLoading) {
          return;
        }
        clearTimeout(this.debounceTimer);

        this.debounceTimer = setTimeout(() => {
          this.init();
          this.searchText = value;
          this.getEvaluationAssignmentTodoList();
        }, 500);
      },
      init() {
        this.loading = true;
        this.firstLoading = true;
        this.dataLoading = true;
        this.pageSize = 50;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
        this.total = 0;
        this.evaluationAssignmentTodoList = [];
      },
      refreshEvaluationAssignment() {
        if (this.canEvaluation) {
          this.init();
          this.getEvaluationAssignmentTodoList();
        }
      },
      onLoadMore() {
        this.pageIndex += 1;
        this.draw += 1;
        this.dataLoading = true;
        this.getEvaluationAssignmentTodoList();
      },
      evaluation(data) {
        this.openEvaluationRecordModal(true, {
          evaluationCriteriaId: data.evaluationCriteriaId,
          evaluationAssignmentId: data.id,
          effectedName: data.effectedName,
          evaluationCriteriaPlanId: this.evaluationCriteriaPlanId,
          canEvaluation: this.canEvaluation,
        });
      },
    },
  });
</script>

<style scoped lang="less">
  .content {
    width: 100%;
    height: 100%;
    background-color: #fff;
  }

  :deep(.ant-card-body) {
    overflow: hidden;
    height: 100%;
  }

  .evaluation-assignment-content {
    background-color: white;
    overflow: hidden;
    height: calc(100% - 40px);
    width: calc(100% + 10px);
    overflow-y: auto;

    .description-content {
      padding: 16px 0;
    }

    .avatar {
      width: 35px;
      display: flex;
      justify-content: center;
    }

    .title {
      font-weight: bold;
      font-size: 16px;
      margin-left: 15px;
      cursor: pointer;
      border-left: #ededed solid 1px;
      padding: 0 0 0 15px;
    }

    .active-title {
      font-weight: bold;
      font-size: 16px;
      color: #2a7dc9;
    }
  }

  .evaluation-criteria-plan {
    margin-top: -3px;
    width: 100%;
    display: flex;
    justify-content: left;
  }

  .evaluation-criteria-plan-name {
    padding: 8px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .evaluation-criteria-plan-span {
    padding: 9px 0;
    font-size: 14px;
    font-weight: normal;
  }
</style>
