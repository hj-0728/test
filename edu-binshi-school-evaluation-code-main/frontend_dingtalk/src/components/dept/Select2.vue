<template>
  <van-popup v-model:show="showDeptSelectPopup"
             position="bottom" :style="{ height: '100%' }" @closed="onCloseDeptFilterPopup">

    <div style="background-color: #efefef; height: 100%;">
      <OverlayLoading v-if="loading"></OverlayLoading>
      <div style="width: 100%; z-index: 100">
        <van-nav-bar title="选择范围">
          <template #left>
            <van-icon name="arrow-left" size="22" style="margin-right: 16px" @click="onClickLeft"/>
            <div style="color: #1989fa;font-size:16px" @click="showDeptSelectPopup = false">
              关闭
            </div>
          </template>
        </van-nav-bar>
        <div style="width: 100%; ">

          <div style="width: 100%">
            <form action="/">
              <van-search
                  shape="round"
                  show-action
                  :clearable=false
                  v-model="searchValue"
                  placeholder="请输入范围名称"
                  @search="onSearch"
                  @cancel="onCancelSearch"
              />
            </form>
          </div>
<!--          <van-notice-bar color="#1989fa" background="#ecf9ff" left-icon="info-o" v-if="parentDept">-->
<!--            年级：{{parentDept['name']}}-->
<!--          </van-notice-bar>-->
        </div>
      </div>
      <div class="content-div">
        <van-cell-group inset v-if="currentDeptList.length > 0">
          <van-cell
              v-for="(dept, index) in currentDeptList"
              clickable
              :key="dept['id']"
              :is-link="dept['children'].length > 0"
              @click.stop="cellClick(index, dept)"
          >
            <template #title>
              <div style="display: flex;margin-top: 2px;align-items: center">
                <div style="margin-top: -4px">
                  <van-checkbox
                      v-if="selectedDeptIdList.indexOf(dept['id']) > -1 || this.selectedDeptList.findIndex(item=>item.id===dept.id) > -1"
                      :name="dept['id']"
                      :checked="true"
                      @click.stop="checkboxClick(dept)"
                      shape="square"
                  />
                  <van-checkbox
                      v-else-if="selectClassGradeIdList.indexOf(dept['id']) > -1"
                      :name="dept['id']"
                      :checked="false"
                      @click.stop="checkboxClick(dept)"
                      shape="square"
                  >
                    <template #icon="props">
                      <van-icon :name="selectedIcon"/>
                    </template>
                  </van-checkbox>
                  <van-checkbox
                      v-else
                      :name="dept['id']"
                      :checked="false"
                      @click.stop="checkboxClick(dept)"
                      shape="square"
                  />
                </div>
                <div style="width: 5px"></div>
                <div style="margin-top: 3px">
                  <van-icon :name="deptRootIcon" size="18" v-if="dept['category'] === 'ROOT'"/>
                  <van-icon :name="deptCampusIcon" size="18" v-if="dept['category'] === 'CAMPUS'"/>
                  <van-icon :name="deptAcademicSectionIcon" size="18" v-if="dept['category'] === 'ACADEMIC_SECTION'"/>
                  <van-icon :name="deptGradeIcon" size="18" v-if="dept['category'] === 'GRADE'"/>
                  <van-icon name="cluster-o" color="#0aa7ef" size="18" v-if="dept['category'] === 'SCHOOL_CLASS'"/>
                </div>
                <div style="width: 5px"></div>
                <div>
                  {{ dept.name }}
                </div>
              </div>
            </template>
          </van-cell>
        </van-cell-group>
        <empty-content v-else :is-show="true" description="暂无相关数据"></empty-content>
      </div>

      <div class="bottom-div">
        <div class="bottom-content">
          <div class="selected-dept-tag-div" ref="tagDiv">
            <template v-for="(dept, index) in selectedDeptList">
              <van-tag
                  closeable
                  size="medium"
                  type="primary"
                  @close="closeTag(index, dept)"
                  class="tag"
              >
                {{ dept.name }}
              </van-tag>
            </template>
          </div>
          <div style="width: 10px;height: 10px"></div>
          <div>
            <van-button style="border-radius: 8px; width: 100px" type="primary" @click="clickConfirm">
              确认({{ selectedDeptList.length }})
            </van-button>
          </div>
        </div>
      </div>
    </div>
  </van-popup>

</template>

<script>
import {Icon, Button, Tag, Checkbox, CheckboxGroup,
  Search, Popup, NoticeBar} from 'vant';
import {ref} from "vue";
import {deptRootIcon, deptCampusIcon, deptAcademicSectionIcon, deptGradeIcon, deptClassIcon, selectedIcon} from '../../resource.js'
import {apiGetScopeDeptList} from "../../api/dept.js";
import OverlayLoading from "../OverlayLoading.vue";
import EmptyContent from "../EmptyContent.vue";
import _ from "lodash";
import constant from "../../constant";

export default {
  name: 'DeptSelectComponent',
  emits: ['confirmSelectDept'],
  components: {
    [Button.name]: Button,
    [Tag.name]: Tag,
    [Checkbox.name]: Checkbox,
    [CheckboxGroup.name]: CheckboxGroup,
    [Search.name]: Search,
    [Popup.name]: Popup,
    [NoticeBar.name]: NoticeBar,
    OverlayLoading,
    EmptyContent
  },
  setup() {
    const deptTreeList = ref([])
    const currentDeptList = ref([])
    // 下面展示的部门
    const selectedDeptList = ref([])
    // 所有选中的部门
    const selectedDeptIdList = ref([])
    const searchValue = ref('')
    const loading = ref(true)
    const currentCategory = ref('GRADE')
    const currentClassNum = ref(0)
    const selectAll = ref(false)
    const showDeptSelectPopup = ref(false)

    const parentDept = ref(null)

    // 有班级被选中的年级
    const selectClassGradeIdList = ref([])

    return {
      deptTreeList,
      currentDeptList,
      selectedDeptList,
      selectedDeptIdList,
      searchValue,
      deptRootIcon,
      deptCampusIcon,
      deptAcademicSectionIcon,
      deptGradeIcon,
      deptClassIcon,
      loading,
      currentCategory,
      currentClassNum,
      selectAll,
      showDeptSelectPopup,
      selectedIcon,
      selectClassGradeIdList,
      parentDept,
    }
  },
  mounted() {
    this.getDeptTree()
  },
  methods: {
    popup(){
      this.showDeptSelectPopup = true
    },
    onCancelSearch() {
      this.searchValue = ''
      this.getDeptTree()
    },
    getDeptTree() {
      this.loading = true
      console.log('getDeptTree ...');
      console.log(this.$store.state.Ranking.filterTopic);
      if (this.$store.state.Ranking.filterTopic === 'student') {
        this.currentCategory = 'SCHOOL_CLASS'
      } else {
        this.currentCategory = 'GRADE'
      }
      apiGetScopeDeptList(this.currentCategory, this.$store.state.Ranking.periodId).then((res) => {
        if (res.data.code === 200) {
          if (res.data.data && res.data.data.length > 0) {
            this.deptTreeList = res.data.data[0].children
            this.currentDeptList = this.deptTreeList
          }
        } else {
          this.$notify(res.data.messages.join(';'))
        }
      }).catch((err) => {
        console.error('获取部门失败：', err)
        this.$notify(constant.networkAnomaly)
      }).finally(() => {
        this.loading = false
      })
    },
    onClickLeft() {
      if (this.currentCategory === 'GRADE') {
        this.$dialog.confirm({
          title: '已到达顶层，是否关闭？',
        }).then(() => {
          setTimeout(() => {
            this.showDeptSelectPopup = false
          }, 200)
        })
      } else {
        this.parentDept = null
        this.currentDeptList = this.searchTree(this.searchValue.trim(), this.deptTreeList)
        // this.currentDeptList = this.deptTreeList
        this.currentCategory = 'GRADE'
        // this.selectJudge()
      }
    },
    closeTag(index, dept) {
      if (dept.children.length > 0) {
        // 修复选择班级时，删除年级无效的问题
        // 因为只有两层 所以可以这么做，层级很多应做递归
        const idx = this.selectedDeptList.map(item => item['id']).indexOf(dept['id'])
        if (idx > -1) {
          this.selectedDeptList.splice(idx, 1)
        }
        for (const d of dept.children) {
          const index = this.selectedDeptIdList.indexOf(d['id'])
          if (index > -1) {
            this.selectedDeptIdList.splice(index, 1)
          }
        }
      } else {
        const idx = this.selectedDeptIdList.indexOf(dept['id'])
        this.selectedDeptIdList.splice(idx, 1)
        this.selectedDeptList.splice(idx, 1)
      }
      this.calcCurrentClassNum()
    },
    cellClick(index, dept) {
      if (dept.children.length > 0) {
        if (this.$store.state.Ranking.filterTopic === 'student') {
          this.currentCategory = 'SCHOOL_CLASS'
          this.currentDeptList = this.searchTree(this.searchValue.trim(), dept['children'])
          this.parentDept = dept
        }
      }
    },
    clickConfirm() {
      // 历史原因，怎么能用怎么来吧。或者有哪位勇士去重写一遍
      const deptIdList = []
      if (this.$store.state.Ranking.filterTopic === 'schoolClass') {
        deptIdList.push(...this.selectedDeptList.map(item=>item.id))
      } else {
        deptIdList.push(...this.selectedDeptIdList)
      }
      this.$emit('confirmSelectDept',
         deptIdList, this.selectedDeptList
      )
      this.showDeptSelectPopup = false
    },
    checkboxClick(dept) {
      let target = this.selectedDeptList.findIndex(item=>item.id===dept.id)
      let targetId = this.selectedDeptIdList.indexOf(dept.id)
      if (target > -1 || targetId > -1) {
        // this.selectedDeptIdList.splice(target, 1)
        if (target > -1) {
          this.selectedDeptList.splice(this.selectedDeptList.findIndex(item=>item.id===dept.id), 1)
        }
        if(targetId > -1) {
          this.selectedDeptIdList.splice(targetId, 1)
        }
        if (dept.category === "GRADE") {
          for (let deptClass of dept['children']) {
            let targetClass = this.selectedDeptIdList.indexOf(deptClass.id)
            if (targetClass > -1) {
              this.selectedDeptIdList.splice(targetClass, 1)
            }
          }
        }
      } else {
        // this.selectedDeptIdList.push(dept.id)
        // console.log(this.selectedDeptList.findIndex(item=>item.id===dept.id))
        let selectDept = _.cloneDeep(dept)
        if (dept.category === "SCHOOL_CLASS" && this.parentDept) {
          selectDept['name'] = `${this.parentDept['name']}/${selectDept['name']}`
        }
        this.selectedDeptList.push(selectDept)
        if (dept.category === "GRADE") {
          for (let deptClass of dept['children']) {
            let targetClass = this.selectedDeptIdList.indexOf(deptClass.id)
            if (targetClass < 0) {
              this.selectedDeptIdList.push(deptClass.id)
            }
          }
        } else {
          this.selectedDeptIdList.push(dept.id)
        }
      }
      this.calcCurrentClassNum()
      if (this.$store.state.Ranking.filterTopic === 'student') {
        this.judgeSelect()
      }
    },
    judgeSelect() {
      this.selectClassGradeIdList.splice(0)
      for(let dept of this.deptTreeList){
        console.log('dept~~~~~~~~~~', dept)
        let isSelectGrade = true
        let selectDeptPush = _.cloneDeep(this.selectedDeptList)
        let selectDeptSplice = _.cloneDeep(this.selectedDeptList)
        let isSelectGradeClass = false
        for(let schoolClass of dept['children']){
          let indexClass = this.selectedDeptIdList.indexOf(schoolClass['id'])
          console.log('schoolClass____', schoolClass)
          if(indexClass < 0) {
            isSelectGrade = false
          }
          if (indexClass > -1 && !isSelectGradeClass){
            isSelectGradeClass = true
          }
          console.log('schoolClassIndex----', this.selectedDeptList.findIndex(item=>item.id===schoolClass.id))
          if(this.selectedDeptList.findIndex(item=>item.id===schoolClass.id) > -1) {
            selectDeptSplice.splice(selectDeptSplice.findIndex(item=>item.id===schoolClass.id), 1)
            console.log(selectDeptSplice)
          } else {
            console.log('indexClass---', indexClass)
            if(selectDeptPush.findIndex(item=>item.id===schoolClass.id) < 0 && indexClass > -1){
              let schoolClassDept = _.cloneDeep(schoolClass)
              schoolClassDept['name'] = `${dept['name']}/${schoolClassDept['name']}`
              selectDeptPush.push(schoolClassDept)
            }
          }
        }
        console.log('selectDeptPush---', selectDeptPush)
        let indexGrade = this.selectedDeptList.findIndex(item=>item.id===dept.id)
        if(isSelectGradeClass && !isSelectGrade) {
          this.selectClassGradeIdList.push(dept.id)
        }
        if(indexGrade > -1 && !isSelectGrade){
          this.selectedDeptList = selectDeptPush
          this.selectedDeptList.splice(this.selectedDeptList.findIndex(item=>item.id===dept.id), 1)
        }
        if(indexGrade < 0 && isSelectGrade){
          this.selectedDeptList = selectDeptSplice
          this.selectedDeptList.push(dept)
        }
        if(indexGrade < 0 && !isSelectGrade) {
          this.selectedDeptList = selectDeptPush
        }
        if(indexGrade > -1 && isSelectGrade) {
          this.selectedDeptList = selectDeptSplice
        }
      }
    },
    calcCurrentClassNum() {
      this.currentClassNum = this.selectedDeptList.length
    },
    onClear() {
      this.currentDeptList = this.deptTreeList
      this.selectedDeptList = []
      this.selectedDeptIdList = []
      this.selectClassGradeIdList = []
      this.currentClassNum = 0
      this.selectAll = false
    },
    onSearch() {
      if(this.currentCategory === 'GRADE' || this.parentDept === null) {
        this.currentDeptList = this.searchTree(this.searchValue.trim(), this.deptTreeList)
      } else {
        this.currentDeptList = this.searchTree(this.searchValue.trim(), this.parentDept['children'])
      }
    },
    searchTree(value, arr) {
      if(value === ''){
        return arr
      }
      let newArr = [];
      for (let item of arr) {
        if (item['name'].indexOf(value) > -1) {
          newArr.push(item);
        }
        if (item['category'] === 'GRADE' && item['children'].length > 0) {
          for(let classDept of item['children']) {
            if (classDept['name'].indexOf(value) > -1) {
              newArr.push(classDept);
            }
          }
        }
      }
      return newArr;
    },
    onCloseDeptFilterPopup() {

    }
  }
}
</script>

<style scoped lang="less">
.bottom-div {
  bottom: 0;
  position: fixed;
  height: 50px;
  width: 100%;
  background-color: white;
}

.bottom-content {
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
  margin-left: 0;
}

.selected-dept-tag-div {
  width: calc(100% - 130px);
  height: 40px;
  overflow-x: scroll;
  overflow-y: hidden;
  border-radius: 8px;
  display: flex;
  white-space: nowrap;
}

.tag-div {
  background-color: #e0dfe0;
  border-radius: 8px;
}

.tag {
  height: 35px;
  background-color: #e0dfe0;
  color: black;
  border-radius: 8px;
  margin-right: 10px;
}

.content-div {
  padding: 10px;
  height: calc(100vh - 170px);
  overflow-y: auto;
  z-index: 99
}

.select-all-div {
  display: flex;
  justify-content: center;
  background-color: white
}
:deep(.select-sign) {
  display: flex;
  align-items: center;
  border-radius: 2px;
  width: 14px;
  height: 14px;
  border: 1px solid #ccc;
  margin-right: 5px;
  justify-content: center;
}
:deep(.select-sign-active) {
  display: flex;
  align-items: center;
  width: 14px;
  height: 14px;
  border-radius: 2px;
  background: #1889f9;
  border: 1px solid #1889f9;
  margin-right: 5px;
  justify-content: center;
}
:deep(.title-wrapper) {
  display: flex;
  align-items: center;
  .name {
    color:#1889f9; font-size: 14px;
    font-weight: bold;
  }
  .icon {
    color:#1889f9;
    margin-right: 5px;
  }
}
:deep(.person-list-item__right_icon) {
  flex-direction: row;
  font-size: 14px!important;
  display: flex;
  align-items: center;
  .van-popover__action-icon {
    font-size: 14px!important;
  }
}
:deep(.select-sign-disabled) {
  background: #ebedf0;
  border-color:#c8c9cc;
}
:deep(.icon) {
  color: #ffffff;
}
:deep(.icon-disabled) {
  color: #c8c9cc;
}
:deep(.van-icon__image) {
  width: 12px;
  height: 12px;
  padding: 3px 0 0 3.5px;
}
</style>
