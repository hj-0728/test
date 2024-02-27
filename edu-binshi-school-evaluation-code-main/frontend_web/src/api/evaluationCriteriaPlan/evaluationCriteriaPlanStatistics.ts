import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
const PREFIX = '/evaluation-criteria-plan-statistics';
const Api = {
  INDICATOR_TREE: `${PREFIX}/indicator-tree`,
  GET_PLAN_INDICATOR_BENCHMARK: `${PREFIX}/get-plan-indicator-benchmark`,
  GET_PLAN_DEPT_GRADE_SCOPE: `${PREFIX}/get-plan-dept-grade-scope`,
  GET_PLAN_BENCHMARK_STATISTICS: `${PREFIX}/get-plan-benchmark-statistics`,
  GET_PLAN_BENCHMARK_RANKING: `${PREFIX}/get-plan-benchmark-ranking`,
  PROGRESS_DETAIL: `${PREFIX}/progress-detail`,
  FILTER_DEPT_TREE: `${PREFIX}/filter-dept-tree`,
  PLAN_STATUS_COUNT: `${PREFIX}/status-count`,
};

/**
 * 获取计划评价指标树
 */
export const apiGetPlanIndicatorTree = (evaluationCriteriaPlanId: String) => {
  return defHttp.get<any>({
    url: `${Api.INDICATOR_TREE}/${evaluationCriteriaPlanId}`,
  });
};

/**
 * 获取计划评价指标的 benchmark
 */
export const apiGetPlanIndicatorBenchmark = (
  evaluationCriteriaPlanId: String,
  indicator: String,
) => {
  return defHttp.get<any>({
    url: `${Api.GET_PLAN_INDICATOR_BENCHMARK}/${evaluationCriteriaPlanId}/${indicator}`,
  });
};

/**
 * 获取计划评价指标的部门对应的年级范围
 */
export const apiGetPlanDeptGradeScope = (evaluationCriteriaPlanId: String) => {
  return defHttp.get<any>({
    url: `${Api.GET_PLAN_DEPT_GRADE_SCOPE}/${evaluationCriteriaPlanId}`,
  });
};

/**
 * 获取计划评价指标基准的统计数据
 */
export const apiGetPlanBenchmarkStatistics = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.GET_PLAN_BENCHMARK_STATISTICS}`,
    params: params,
  });
};

/**
 * 获取计划评价指标基准的排行数据
 */
export const apiGetPlanBenchmarkRanking = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.GET_PLAN_BENCHMARK_RANKING}`,
    params: params,
  });
};

/**
 * 获取计划评价进展信息
 */
export const apiGetPlanProgressDetail = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.PROGRESS_DETAIL}`,
    params: params,
  });
};

/**
 * 获取计划排行部门筛选
 */
export const apiGetPlanRankingFilterDeptTree = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.FILTER_DEPT_TREE}`,
    params: params,
  });
};

/**
 * 获取计划状态统计
 */
export const apiGetPlanStatusCount = () => {
  return defHttp.get<any>({
    url: `${Api.PLAN_STATUS_COUNT}`,
  });
};
