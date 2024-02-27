export function getSessionDingtalkUserInfo() {
    const dingtalkUser = sessionStorage.getItem('dingtalkUserInfo')
    if (!dingtalkUser) {
        throw ('未获取到当前用户身份')
    }
    return JSON.parse(dingtalkUser)
}