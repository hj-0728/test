import { defHttp } from '/@/utils/http/axios';
import { k12TeacherSubjectVmList } from '/@/api/model/k12TeacherSubjectModel';

const PREFIX = '/k12-teacher-subject';

const Api = {
  GET_K12_TEACHER_LIST_PAGE: `${PREFIX}/teacher-list`,
  GET_SUBJECT_LIST: `${PREFIX}/subject-list`,
  GET_K12_TEACHER_SUBJECT: `${PREFIX}/detail/`,
  SAVE_K12_TEACHER_SUBJECT: `${PREFIX}/save`,
  CAPACITY_AND_SUBJECT_FILTERS: `${PREFIX}/capacity-and-subject-filters`,
};

export const apiK12TeacherListPage = (params) => {
  return defHttp.post<any>({
    url: Api.GET_K12_TEACHER_LIST_PAGE,
    params: params,
  });
};

export const apiGetK12TeacherSubjectDetail = (peopleId, dimensionDeptTreeId) => {
  return defHttp.get<k12TeacherSubjectVmList>({
    url: Api.GET_K12_TEACHER_SUBJECT + peopleId + '/' + dimensionDeptTreeId,
  });
};

export const apiGetSubjectList = () => {
  return defHttp.get<any>({
    url: Api.GET_SUBJECT_LIST,
  });
};

export const apiSaveK12TeacherSubject = (params) => {
  return defHttp.post<any>({
    url: Api.SAVE_K12_TEACHER_SUBJECT,
    params: params,
  });
};

export const apiGetCapacityAndSubjectFilters = () => {
  return defHttp.get<any>({
    url: Api.CAPACITY_AND_SUBJECT_FILTERS,
  });
};
