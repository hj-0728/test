import { BasicResponseModel } from '/@/api/model/baseModel';

export interface k12TeacherSubjectVm {
  id: string;
  name: string;
  peopleID: string;
  dimensionDeptTreeId: string;
  subjectId: string;
  subjectName: string;
}

export interface k12TeacherSubjectVmList extends BasicResponseModel {
  data: k12TeacherSubjectVm[];
}
