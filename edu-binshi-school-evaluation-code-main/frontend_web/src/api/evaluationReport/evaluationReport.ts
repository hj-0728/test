import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/evaluation-report';
const Api = {
  GET_EVALUATION_REPORT_TREE: `${PREFIX}/tree`,
  GET_EVALUATION_REPORT_ASSIGNMENT_PAGE_LIST: `${PREFIX}/assignment-page-list`,
  GET_EVALUATION_ASSIGNMENT_REPORT: `${PREFIX}/get-evaluation-assignment-report`,
  GET_DIMENSION_DEPT_TREE_REPORT: `${PREFIX}/get-dimension-dept-tree-report`,
  GET_ORGANIZATION_REPORT: `${PREFIX}/get-organization-report`,
  GET_REPORT_CATEGORY_LIST: `${PREFIX}/get-report-category-list`,
  GET_REPORT_TEMPLATE_FILE: `${PREFIX}/get-report-template-file`,
};

export const apiGetEvaluationReportTree = (params) => {
  return defHttp.post<any>({
    url: Api.GET_EVALUATION_REPORT_TREE,
    params: params,
  });
};

export const apiGetEvaluationReportAssignmentPageList = (params) => {
  return defHttp.post<any>({
    url: Api.GET_EVALUATION_REPORT_ASSIGNMENT_PAGE_LIST,
    params: params,
  });
};

export const apiGetEvaluationAssignmentReportReport = (params) => {
  return defHttp.post<any>({
    url: Api.GET_EVALUATION_ASSIGNMENT_REPORT,
    params: params,
  });
};

export const apiGetDimensionDeptTreeReport = (params) => {
  return defHttp.post<any>({
    url: Api.GET_DIMENSION_DEPT_TREE_REPORT,
    params: params,
  });
};
