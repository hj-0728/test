const dynamicRoundedCell = (currentIndex, itemsLength, roundPx = 8) => {
    if (currentIndex === 0) {
        return `${roundPx}px ${roundPx}px 0 0`
    } else {
        return '0px'
    }
}

const taskStatusColorFilter = (code) => {
    switch (code) {
        case 'unclaimed':
            return "#cbc9c9";
        case 'claim':
            return "#ec0a25";
        case 'apply_finished':
            return "#cece03";
        case 'activity_in_progress':
            return "#07BF60";
        case 'activity_finished':
            return "#cbc9c9";
        default:
            return "";
    }
};

const taskStatusFilter = (code) => {
  switch (code) {
    case 'unclaimed':
      return "未领取";
    case 'claim':
      return "已领取";
    case 'apply_finished':
      return "报名结束";
    case 'activity_in_progress':
      return "活动中";
    case 'activity_finished':
      return "活动结束";
    default:
      return "";
  }
};

const regGlobalFilters = (app) => {
    if (app.config.globalProperties && !app.config.globalProperties.$filters) {
        app.config.globalProperties.$filters = {
            dynamicRoundedCell,
            taskStatusColorFilter,
            taskStatusFilter
        };
    }
};

export {
    regGlobalFilters,
}