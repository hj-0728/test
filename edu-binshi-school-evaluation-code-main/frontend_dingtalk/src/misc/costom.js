import axios from "axios";
// import dayjs from "dayjs";
import {apiGetWecomUserInfo} from "../api/dingtalkUser.js";
import dayjs from "dayjs";
import utc from 'dayjs/plugin/utc'

async function getWecomDuty() {
    let duty = ''
    if (sessionStorage.getItem('wecomUserInfo')) {
        const wecomUserInfo = JSON.parse(sessionStorage.getItem('wecomUserInfo'))
        duty = wecomUserInfo.duty
    } else {
        await apiGetWecomUserInfo().then((res) => {
            if (res.data.code === 200) {
                sessionStorage.setItem('wecomUserInfo', JSON.stringify(res.data.data))
                duty = res.data.data.duty
            } else {
                console.log(res.data.messages.join(';'))
            }
        }).catch((error) => {
            console.log(`获取用户失败 - ${error}`)
        })
    }
    return duty
}

function formatDate(date, formatStr) {
    dayjs.extend(utc)
    return dayjs.utc(date).local().format(formatStr)
}

export {
    getWecomDuty,
    formatDate
}
