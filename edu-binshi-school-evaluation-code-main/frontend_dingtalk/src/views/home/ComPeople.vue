<template>
  <div class="container" v-if="dingtalkUser">
    <van-cell-group inset>
      <van-cell>
        <template #title>
          <div style="padding: 3px 0;font-size: 16px">
            欢迎您：{{ dingtalkUser.name }}
          </div>
        </template>
        <template #right-icon>
          <div style="padding: 3px 0;color: #1989fa;font-size: 16px;" v-if="dingtalkUser.currentCapacity">
            <van-tag @click="checkDutyCanSwitch" plain
            class="van-tag-custom" type="primary" size="large"
            >{{ dingtalkUser.currentCapacity.name }}
              <van-icon v-if="dingtalkUser.capacityList && dingtalkUser.capacityList.length > 1"
                        :name="openDown"
                        size="10px"
                        style="margin-left: 6px"/>
            </van-tag>
          </div>
        </template>
      </van-cell>
    </van-cell-group>
    <van-popup v-model:show="showCapacitySwitchSheet" round position="bottom">
      <van-picker
          v-if="showCapacitySwitchSheet"
          show-toolbar
          title="职责切换"
          :columns="capacityList"
          :allow-html="true"
          @confirm="onSwitchCapacity"
          @cancel="showCapacitySwitchSheet = false"
          :default-index="defaultIndex"
      />
    </van-popup>
  </div>
</template>

<script>
import { reactive, toRefs, ref, inject } from "vue";
import { Popover, Popup, Tag, Empty, Picker } from "vant";
import constant from "../../constant";
import { getSessionDingtalkUserInfo } from "../../sessionStorage";
import { openDown } from '../../resource'
import { apiGetDingtalkUserInfo } from "../../api/dingtalkUser";
import { apiSwitchCapacity } from "../../api/capacity";


export default {
  emits: ['refreshMenu'],
  components: {
    [Tag.name]: Tag,
    [Popover.name]: Popover,
    [Popup.name]: Popup,
    [Empty.name]: Empty,
    [Picker.name]: Picker,
  },
  setup() {
    const state = reactive({
      dingtalkUser: null,
    })
    const showCapacitySwitchSheet = ref(false);
    const defaultIndex = ref(0);
    const capacityCode = ref('');
    const capacityList = ref([]);
    const loading = inject('loading')
    return {
      ...toRefs(state),
      openDown,
      showCapacitySwitchSheet,
      defaultIndex,
      capacityCode,
      capacityList,
      loading
    }
  },
  created() {
    this.preparePeopleInfo()
  },
  methods: {
    checkDutyCanSwitch() {
      if(this.dingtalkUser.capacityList.length > 1){
         this.showCapacitySwitchSheet = true;
      }
    },
    async preparePeopleInfo() {
      try {
        this.dingtalkUser = getSessionDingtalkUserInfo();
        this.makeCapacityList(this.dingtalkUser.currentCapacity.code)
        this.loading = false
      } catch (e) {
        await this.getDingtalkUserInfo()
      }
      // dingFlow.flow()
    },
    async getDingtalkUserInfo() {
      await apiGetDingtalkUserInfo().then((res) => {
        if (res.data.code === 200) {
          this.dingtalkUser = res.data.data;
          sessionStorage.setItem('dingtalkUserInfo', JSON.stringify(res.data.data))
          this.capacityCode = res.data.data.currentCapacity.code
          this.makeCapacityList(res.data.data.currentCapacity.code)
        } else {
          this.$notify({
            type: 'danger',
            message: res.data.messages.join('\n')
          })
        }
        this.loading = false
      }).catch((err) => {
        console.error('获取人员失败：', err)
        this.$notify({
          type: 'danger',
          message: constant.networkAnomaly
        })
        this.loading = false
      })
    },
    makeCapacityList(excludeCode){
      this.capacityList.length = 0
      this.dingtalkUser.capacityList.map((capacity, index) => {
        if (excludeCode !== capacity.code) {
          capacity.text = capacity.name
          this.capacityList.push(capacity)
        } else {
          capacity.text = `<div style="color: #1989fa">${capacity.name}<span style="padding-left: 10px">√</span></div>`
          this.capacityList.push(capacity)
          this.defaultIndex= index
        }
      })
    },
    onSwitchCapacity(e) {
      this.showCapacitySwitchSheet = false
      if (e.code !== this.dingtalkUser.currentCapacity.code) {
        this.loading = true
        apiSwitchCapacity(e.code).then((res) => {
          if (res.data.code === 200) {
            this.switchCapacity(e)
          } else {
            this.$notify({
              type: 'danger',
              message: res.data.messages.join(';')
            })
            this.loading = false
          }
        }).catch((err) => {
          console.error('切换职责失败：', err)
          this.$notify({
            type: 'danger',
            message: constant.networkAnomaly
          })
          this.loading = false
        })
      }
    },
    switchCapacity(newCapacity) {
      this.dingtalkUser.currentCapacity = newCapacity
      this.capacityCode = newCapacity.code
      this.makeCapacityList(newCapacity.code);
      sessionStorage.setItem('dingtalkUserInfo', JSON.stringify(this.dingtalkUser))
      sessionStorage.removeItem('menuList')
      this.$emit('refreshMenu')
    }
  }
}
</script>

<style scoped lang="less">
</style>