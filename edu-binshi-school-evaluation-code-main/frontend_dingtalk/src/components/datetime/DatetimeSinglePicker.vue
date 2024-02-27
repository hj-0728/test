<template>
  <div class="datetime-range-picker">
    <div>
      <van-datetime-picker
          v-model="time"
          type="datetime"
          :title="pickerTitle"
          :visible-item-count="5"
          @change="onTimeChange"
          @confirm="onConfirmAll"
          @cancel="onCancelAll"
          :min-date="minDate"
      />
    </div>
  </div>
</template>
<script>
// datetime picker 参考: https://vant-contrib.gitee.io/vant/v3/#/zh-CN/datetime-picker
// Vant官方只提供日期粒度的 时间范围选择， 我们使用两个Datepicker组合成一个精确到分的时间周期的选择器
import {DatetimePicker} from "vant";
import {ref} from 'vue'

export default {
  emits: ["confirmSelectTime", "cancelSelectTime", "timeChange"],
  components: {
    [DatetimePicker.name]: DatetimePicker,
  },
  props: {
    pickerTitle: String,
    defaultAt: Date,
  },
  setup(props) {
    const time = ref(new Date());
    if (props.defaultAt) {
      time.value = props.defaultAt
    }
    console.log(props.pickerTitle)
    const minDate = ref(new Date())
    return {
      time,
      minDate
    };
  },
  methods: {
    onCancelAll() {
      this.$emit("cancelSelectTime");
    },
    onConfirmAll() {
      const valid = this.checkTimeRangeValid()
      if (!valid) {
        return false
      }
      this.$emit("confirmSelectTime", {time: this.time});
    },
    onTimeChange(e) {
      // this.checkStartTimeValid()
      this.$emit("timeChange", e);
    },

    checkTimeRangeValid() {
      if (!this.time) {
        this.$notify({type: 'danger', message: '请选择时间'})
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
