import {createRouter, createWebHistory} from 'vue-router'
import _ from 'lodash'
import store from '../store'
import constant from '../constant'
import instance from "../utils/request";

const env = import.meta.env
const modules = import.meta.globEager('./modules/**/*.js');

const routeModuleList = []
const noNeedAuthRouteList = []

Object.keys(modules).forEach((key) => {
    const mod = modules[key].default || {};
    const modList = Array.isArray(mod) ? [...mod] : [mod];
    modList.map((m) => {
        if (Object.keys(m).includes("needAuth") && !m.needAuth) {
            noNeedAuthRouteList.push(m.path)
        }
    })
    routeModuleList.push(...modList);
});

const routes = [...routeModuleList]

const router = createRouter({
    history: createWebHistory(env.VITE_BASE_URL),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (to.meta.scrollTop) {
            return {left: 0, top: 0}
        }
    },
})

const _updateTransition = (to, from) => {
    const toDepth = _.compact(to.path.split('/')).length
    const fromDepth = _.compact(from.path.split('/')).length
    if (router.isBack) {
        router.isBack = false
        store.dispatch('updateTrans', 'slide-right')
    } else if (router.isForward) {
        router.isForward = false
        store.dispatch('updateTrans', 'slide-left')
    } else if (to.meta.isTabPage === true && from.meta.isTabPage === true) {
        store.dispatch('updateTrans', 'fade')
    } else {
        store.dispatch(
            'updateTrans',
            toDepth < fromDepth ? 'slide-right' : 'slide-left'
        )
    }
}

const _verifyIdentity = (to, next) => {
    if (noNeedAuthRouteList.includes(to.path) || !JSON.parse(env.VITE_NEED_AUTH)) {
        console.log("啥玩意儿")
        console.log(env.VITE_NEED_AUTH, noNeedAuthRouteList, to.path)
        next()
    } else {
        const refreshToken = sessionStorage.getItem('refreshToken')
        const accessToken = sessionStorage.getItem('accessToken')
        if (!accessToken || !refreshToken) {
            let url = env.VITE_VERIFY_CATEGORY === "DINGTALK" ? 'auth/dingtalk-login': 'auth/wecom-login'
            if ('authToken' in to.query && to.query.authToken) {
                url += `?authToken=${to.query.authToken}`
            }
            else if ('code' in to.query && to.query.code) {
                url += `?code=${to.query.code}`
            }
            console.log("+++++++++++++++++++++++")
            instance.post(url).then((res) => {
                console.log("----------------------")
                console.log(res.data.data)
                if (res.data.code === 302) {
                    let redirect_url = res.data.data.redirect_url
                    if (env.VITE_VERIFY_CATEGORY === "DINGTALK") {
                        dd.ready(function() {
                            dd.runtime.permission.requestAuthCode({corpId:'ding59671a103ffc8e344ac5d6980864d335'}).then((result) => {
                                if (result) {
                                    const ddCode = result.code
                                    window.location.href = res.data.data.redirect_url + '?code=' + ddCode
                                }
                            });
                        });
                    } else {
                        window.location.href = redirect_url
                    }
                } else if (res.data.code === 200) {
                    if (res.data.data.auth_token) {
                        window.location.href = `${env.VITE_REDIRECT_URL}?authToken=${res.data.data.auth_token}`
                    } else if (res.data.data.access_token) {
                        sessionStorage.setItem('accessToken', res.data.data.access_token)
                        sessionStorage.setItem('refreshToken', res.data.data.refresh_token)
                        router.push('/')
                    }
                } else if (res.data.code === 500) {
                    var messages = res.data.error.message
                    router.isForward = true
                    router.push('/tips/error?data=' + encodeURIComponent(messages))
                }
            }).catch((error) => {
                sessionStorage.clear()
                router.isForward = true
                router.push(`/tips/error?data=${constant.authenticationFailed}`)
                console.log('身份验证失败：', error)
            })
        } else {
            next()
        }
    }
}


router.beforeEach((to, from, next) => {
    _verifyIdentity(to, next)
    _updateTransition(to, from)
})

export default router
