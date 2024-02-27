<template>
  <Dropdown placement="bottomRight" trigger="click">
    <div class="icon-div">
      <Icon icon="ant-design:filter-twotone" :color="iconColor" />
    </div>
    <template #overlay>
      <div class="multiple-choice-filters-content">
        <div style="height: 2px"></div>
        <div
          v-for="filter in $props.filters"
          :key="'multiple-choice-filters-' + filter.value"
          :class="{
            'filter-div': checkedList.indexOf(filter.value) < 0,
            'filter-div-active': checkedList.indexOf(filter.value) > -1,
          }"
          style="margin-bottom: 4px"
          @click.stop="onClick(filter)"
        >
          <Checkbox
            v-if="$props.choiceType === 'Checkbox'"
            :checked="checkedList.indexOf(filter.value) > -1"
          />
          <Radio
            v-if="$props.choiceType === 'Radio'"
            :checked="checkedList.indexOf(filter.value) > -1"
          />
          <span style="margin-left: 5px">{{ filter.text }}</span>
        </div>
        <div class="btn-div">
          <div class="btn-reset">
            <Button type="link" size="small" @click="onReset"> 重置 </Button>
          </div>
          <div style="width: 5px"></div>
          <div class="btn-confirm">
            <Button type="primary" size="small" @click="onConfirm"> 确定 </Button>
          </div>
        </div>
      </div>
    </template>
  </Dropdown>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { Checkbox, Button, Dropdown, Radio } from 'ant-design-vue';
  import Icon from '/@/components/Icon';

  export default defineComponent({
    emit: ['onReset', 'onConfirm'],
    components: {
      Checkbox,
      Button,
      Icon,
      Dropdown,
      Radio,
    },
    props: {
      filters: {
        type: Array,
      },
      choiceType: {
        type: String,
        default: 'Checkbox', // or Radio
      },
      defaultSelect: {
        type: Array,
        default: () => {
          return [];
        },
      },
      needSetupOnReset: {
        type: Boolean,
        default: false,
      },
    },
    setup(props, context) {
      const checkedList = ref<any[]>([]);
      const iconColor = ref('#717171');
      checkedList.value = props.defaultSelect.slice();
      if (props.needSetupOnReset) {
        if (checkedList.value.length === 0) {
          if (props.filters !== undefined && props.filters !== null) {
            context.emit('onReset', { click: false });
          }
          iconColor.value = '#717171';
        } else {
          iconColor.value = '#0960bd';
        }
      }
      return {
        checkedList,
        iconColor,
      };
    },
    methods: {
      onClick(filter) {
        const idx = this.checkedList.indexOf(filter.value);
        if (idx > -1) {
          this.checkedList.splice(idx, 1);
        } else {
          if (this.$props.choiceType === 'Checkbox') {
            this.checkedList.push(filter.value);
          } else {
            this.checkedList = [filter.value];
          }
        }
      },
      onReset() {
        this.iconColor = '#717171';
        this.checkedList = [];
        this.$emit('onReset', { click: true });
      },
      onConfirm() {
        if (this.checkedList.length === 0) {
          this.iconColor = '#717171';
          this.$emit('onConfirm', null);
        } else {
          this.iconColor = '#0960bd';
          this.$emit('onConfirm', this.checkedList);
        }
      },
    },
  });
</script>

<style scoped lang="less">
  .icon-div {
    cursor: pointer;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
  }

  .icon-div:hover {
    background-color: #ddd;
  }

  .multiple-choice-filters-content {
    padding: 2px 0;
    background-color: white;
    box-shadow: 0 0 5px #d5d5d5, 0 0 8px #dddddd;

    .filter-div {
      cursor: pointer;
      padding: 0 8px;
      height: 30px;
      display: flex;
      align-items: center;
    }

    .filter-div:hover {
      background-color: #f5f5f5;
    }

    .filter-div-active {
      cursor: pointer;
      padding: 0 8px;
      height: 30px;
      display: flex;
      align-items: center;
      background-color: #e3f4fc;
    }

    .filter-div-active:hover {
      background-color: #e7f5fc;
    }

    .btn-div {
      display: flex;
      justify-content: center;
      align-items: center;
      border-top: #e8e8e8 solid 1px;
      padding: 4px 8px;
      height: 36px;
      position: relative;
      min-width: 120px;
    }

    .btn-reset {
      color: #0960bd;
      position: absolute;
      left: 5px;
      top: 4px;
    }

    .btn-reset:hover {
      color: #2e84d2;
    }

    .btn-confirm {
      position: absolute;
      right: 8px;
      top: 5px;
    }
  }
</style>
