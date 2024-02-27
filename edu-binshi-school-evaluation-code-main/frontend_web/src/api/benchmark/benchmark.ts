import { defHttp } from '/@/utils/http/axios';

enum Api {
  GET_BENCHMARK_LIST_BY_INDICATOR_ID = '/benchmark/get-list-by-indicator-id',
  SAVE_AGGREGATED_BENCHMARK = '/benchmark/save-aggregated-benchmark',
  SAVE_GRADE_BENCHMARK = '/benchmark/save-grade-benchmark',
  SAVE_BENCHMARK = '/benchmark/save-benchmark',
  GET_CHILD_NODE_AGGREGATED_BENCHMARK_LIST_BY_INDICATOR_ID = '/benchmark/get-child-node-benchmark-list',
  GET_BENCHMARK_DETAIL = '/benchmark/detail',
  DELETE_BENCHMARK = '/benchmark/delete',
}

export const apiGetBenchmarkListByIndicatorId = (indicatorId, inputScoreSymbolId) => {
  return defHttp.get<any>({
    url: `${Api.GET_BENCHMARK_LIST_BY_INDICATOR_ID}/${indicatorId}/${inputScoreSymbolId}`,
  });
};

export const apiGetChildNodeBenchmarkList = (parentIndicatorId, inputScoreSymbolId) => {
  return defHttp.get<any>({
    url: `${Api.GET_CHILD_NODE_AGGREGATED_BENCHMARK_LIST_BY_INDICATOR_ID}/${parentIndicatorId}/${inputScoreSymbolId}`,
  });
};

export const apiSaveAggregatedBenchmark = (params) => {
  return defHttp.post<any>({
    url: Api.SAVE_AGGREGATED_BENCHMARK,
    params: params,
  });
};

export const apiSaveBenchmark = (params) => {
  return defHttp.post<any>({
    url: Api.SAVE_BENCHMARK,
    params: params,
  });
};

export const apiGetBenchmarkDetail = (benchmarkId) => {
  return defHttp.get<any>({
    url: `${Api.GET_BENCHMARK_DETAIL}/${benchmarkId}`,
  });
};

export const apiDeleteBenchmark = (params) => {
  return defHttp.post<any>({
    url: Api.DELETE_BENCHMARK,
    params: params,
  });
};
