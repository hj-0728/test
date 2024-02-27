import { defHttp } from '/@/utils/http/axios';

enum Api {
  GET_BENCHMARK_STRATEGY_LIST = '/benchmark-strategy/list',
  GET_STRATEGY_INPUT_PARAMS = '/benchmark-strategy/get-input-params',
}

export const apiGetBenchmarkStrategyList = (benchmarkId) => {
  return defHttp.get<any>({
    url: benchmarkId
      ? `${Api.GET_BENCHMARK_STRATEGY_LIST}?benchmarkId=${benchmarkId}`
      : Api.GET_BENCHMARK_STRATEGY_LIST,
  });
};
export const apiGetBenchmarkStrategyInputParamsByStrategyId = (params) => {
  return defHttp.post<any>({
    url: Api.GET_STRATEGY_INPUT_PARAMS,
    params: params,
  });
};
