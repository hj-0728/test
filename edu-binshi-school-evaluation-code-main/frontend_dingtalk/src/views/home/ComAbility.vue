<template>
  <div class="home-ability-container">
    <van-cell-group>
      <van-grid
          :class="idx === 0 ? 'action-icons' : 'action-icons other-row'"
          gutter="10"
          clickable
          :border="false"
          icon-size="32px"
          :column-num="group.length"
          v-for="(group, idx) in menuGroup"
          :key="idx"
      >
        <van-grid-item v-for="(menu, idx) in group"
                       :key="menu.id"
                       :text="menu.name"
                       @click="toMenu(menu.path, menu.code)">

          <div class="menu-div">
            <van-image :src="'homeIcon/' + menu.icon"
                       class="menu-icon"></van-image>
            <div class="menu-name-class">
              {{ menu.name }}
            </div>
          </div>
        </van-grid-item>
      </van-grid>
    </van-cell-group>
  </div>
</template>

<script>
import {Grid, GridItem, Toast} from 'vant';
import constant from "../../constant";
import {apiGetMenuList} from "../../api/menu";
import {ref, inject} from "vue";
import {stayTunedIcon} from "../../resource";

const env = import.meta.env

export default {
  components: {
    [Grid.name]: Grid,
    [GridItem.name]: GridItem,
  },
  setup() {
    const loading = inject('loading')
    const menuGroup = ref([])
    const getMenuList = () => {
      if (sessionStorage.getItem('menuGroup')) {
        menuGroup.value = JSON.parse(sessionStorage.getItem('menuGroup'));
        loading.value = false
      } else {
        apiGetMenuList().then((res) => {
          if (res.data.code === 200) {
            for (let i = 0; i < res.data.data.length-1; i+=2) {
              menuGroup.value.push(res.data.data.slice(i, i+2))
            }
            sessionStorage.setItem('menuGroup', JSON.stringify(menuGroup.value));
          } else {
            this.$notify({
              type: 'danger',
              message: res.data.messages.join('\n')
            })
          }
        }).catch((err) => {
          console.error('获取菜单失败：', err)
          this.$notify({
            type: 'danger',
            message: constant.networkAnomaly
          })
        }).finally(() => {
          loading.value = false
        })
      }
    };
    getMenuList();

    return {
      env,
      getMenuList,
      stayTunedIcon,
      menuGroup
    }
  },
  methods: {
    toMenu(path, code) {
      if (path === '#') {
        Toast({
          message: '敬请期待',
          iconSize: 60,
          icon: this.stayTunedIcon,
        })
        return
      }
      try {
        this.$router.push(path)
      } catch (e) {
        this.$notify({
          type: 'danger',
          message: e
        })
      }
    },
  }
}
</script>

<style lang="less" scoped>
:deep(.action-icons) {
  .van-grid-item__text {
    font-size: 12px !important;
  }

  .van-grid-item__content {
    border-radius: 8px !important;
    padding: 10px 0 !important;
  }
}

.menu-div {
  text-align: center
}

.menu-icon {
  width: 50px;
  height: 50px;
}

.home-ability-container {
  padding: 0.2em;

  .van-cell-group {
    background-color: unset;
  }
}

.menu-name-class {
  font-size: 12px !important;
  margin-top: 4px;
  color: #646566;
  line-height: 1.5;
  word-break: break-all;
}
.other-row {
  margin-top: 10px;
}
</style>