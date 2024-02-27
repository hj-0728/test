<template>
  <div class="datetime-range-picker">
    <div>
      <van-datetime-picker
        v-model="start"
        type="datetime"
        :title="pickerTitle"
        :visible-item-count="5"
        :min-date="minDate"
        @change="onStartTimeChange"
        @confirm="onConfirmAll"
        @cancel="onCancelAll"
      />
    </div>
    <h-spacer size="lg"></h-spacer>
    <div>
      <van-datetime-picker
        v-model="end"
        type="datetime"
        :show-toolbar="false"
        @change="onEndTimeChange"
        :visible-item-count="5"
        :min-date="minDate"
      />
    </div>
  </div>
</template>
<script>
// datetime picker 参考: https://vant-contrib.gitee.io/vant/v3/#/zh-CN/datetime-picker
// Vant官方只提供日期粒度的 时间范围选择， 我们使用两个Datepicker组合成一个精确到分的时间周期的选择器
import { DatetimePicker } from "vant";
import { ref } from 'vue'
export default {
  emits: ["confirmSelectTimeRange", "cancelSelectTimeRange", "startTimeChange", "endTimeChange"],
  components: {
    [DatetimePicker.name]: DatetimePicker,
  },
  props: {
    isMoreThenNow: Boolean,
    pickerTitle: String,
    defaultAt: Object,
    applyAt: Object,
    activityAt: Object,
    checkInAt: Object,
    checkOutAt: Object
  },
  setup(props) {
    const start = ref(new Date());
    const end = ref(new Date());
    const minDate = ref(new Date());
    if(props.defaultAt){
      start.value = props.defaultAt.start
      end.value = props.defaultAt.end
    } else {
      start.value.setMinutes(start.value.getMinutes()+5)
      end.value.setHours(start.value.getHours()+1)
    }
    if (props.applyAt&&props.pickerTitle==='报名起止时间') {
      start.value = props.applyAt.start
      end.value = props.applyAt.end
    } else if (props.activityAt&&props.pickerTitle==='活动进行时间') {
      start.value = props.activityAt.start
      end.value = props.activityAt.end
    } else if (props.checkInAt&&props.pickerTitle==='签到起止时间') {
      start.value = props.checkInAt.start
      end.value = props.checkInAt.end
    } else if (props.checkOutAt&&props.pickerTitle==='签退起止时间') {
      start.value = props.checkOutAt.start
      end.value = props.checkOutAt.end
    }
    // start.value = props.applyStartAt
    // end.value = props.applyEndAt
    return {
      start,
      end,
      minDate
    };
  },
  methods: {
    onCancelAll() {
      this.$emit("cancelSelectTimeRange");
    },
    onConfirmAll() {
      const valid = this.checkTimeRangeValid()
      if (!valid) {
        return false
      }
      this.$emit("confirmSelectTimeRange", { start: this.start, end: this.end });
    },
    onStartTimeChange(e) {
      // this.checkStartTimeValid()
      this.$emit("startTimeChange", e);
    },
    onEndTimeChange(e) {
      // this.checkEndTimeValid()
      this.$emit("endTimeChange", e);
    },

    checkTimeRangeValid () {
      const now = this.$D()
      if (!this.start) {
        this.$notify({type: 'danger', message: '请选择开始时间'})
        return false
      }
      if (this.isMoreThenNow) {
        if (this.start < now) {
          this.$notify({type: 'danger', message: '开始时间不能小于当前时间'})
          return false
        }
        if (this.end < now) {
          this.$notify({type: 'danger', message: '结束时间不能小于当前时间'})
          return false
        }
      }

      if (!this.end) {
        this.$notify({type: 'danger', message: '请选择结束时间'})
        return false
      }

      if (this.end <= this.start) {
        this.$notify({type: 'danger', message: '结束时间不能小于等于开始时间'})
        return false
      }
      return true
    }

  },
};
</script>

<style scoped lang="less">
.datetime-range-picker {
  display: flex;
  flex-direction: column;
}
</style>
