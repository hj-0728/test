import request from "../utils/request";

//获取当前部门列表
export async function apiGetCurrentDeptList(params) {
    return request({
        url: '/wecom-k12-dept/current-dept-list',
        method: 'post',
        data: params
    })
}

//获取部门列表
export async function apiGetScopeDeptList(category, periodId) {
    return request({
        url: `wecom-k12-dept/tree-by-category/${category}/${periodId}`,
        method: 'get',
    })
}
