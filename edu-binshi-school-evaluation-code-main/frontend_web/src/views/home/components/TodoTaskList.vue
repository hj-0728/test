<template>
  <div style="margin: 0 10px 10px 10px">
    <List :loading="loading" item-layout="horizontal" :data-source="todoTaskList">
      <template #loadMore>
        <div
          v-if="!loading && todoTaskListFilterCount > todoTaskList.length"
          :style="{
            textAlign: 'center',
            marginTop: '16px',
            height: '32px',
            lineHeight: '32px',
            marginBottom: '12px',
          }"
        >
          <a-button @click="onLoadMore">加载更多</a-button>
        </div>
      </template>
      <template #renderItem="{ item, index }">
        <ListItem>
          <ListItemMeta>
            <template #description>
              {{ item.planName }}
              <div v-if="isCompleted">
                <span class="complete-info">{{ item.completedPeopleName }}</span>
                <span style="padding: 0 4px">完成于</span>
                <span class="complete-info">
                  {{ dayjs(item.completedAt).format('YYYY-MM-DD HH:mm') }}
                </span>
              </div>
            </template>
            <!-- eslint-disable-next-line -->
            <template #title>
              <span v-if="!isCompleted" v-html="item.title"></span>
              <span v-else v-html="item.title"></span>
            </template>
            <template #avatar>
              <Icon v-if="isCompleted" icon="todo-c|svg" :size="30" />
              <div
                v-else
                style="cursor: pointer"
                @mouseover="changeIcon(index)"
                @mouseleave="resetIcon(index)"
              >
                <Icon :icon="item.icon" :size="30" @click="completeTodoTask(item, index)" />
              </div>
            </template>
          </ListItemMeta>
          <div>
            {{ dayjs(item.generatedAt).format('YYYY-MM-DD') }}
          </div>
        </ListItem>
      </template>
    </List>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { List, ListItem, ListItemMeta } from 'ant-design-vue';
  import todoSvg from '/@/assets/icons/todo.svg';
  import { apiCompleteTodoTask, apiGetTodoTaskPage } from '/@/api/todoTask/todoTask';
  import { Icon } from '/@/components/Icon';
  import dayjs from 'dayjs';
  export default defineComponent({
    components: {
      List,
      ListItem,
      ListItemMeta,
      Icon,
    },
    props: {
      isCompleted: {
        type: Boolean,
        default: null,
      },
    },
    emits: ['setTodoCount', 'todoTaskCompleted'],
    setup(props) {
      const loading = ref(false);
      const todoTaskList = ref([]);
      const todoTaskListFilterCount = ref(0);
      const todoIcon = ref('todo|svg');
      const selectIndex = ref(-1);
      const params = reactive({
        searchText: '', //搜索框中的内容
        pageSize: 20, //页面显示条数
        pageIndex: 0, //当前显示的第几页
        draw: 1, //默认显示第一页
        isCompleted: props.isCompleted,
      });
      return {
        loading,
        todoTaskList,
        todoSvg,
        params,
        ...toRefs(params),
        todoTaskListFilterCount,
        todoIcon,
        selectIndex,
      };
    },
    mounted() {
      this.getTodoTaskProgressData();
    },
    methods: {
      dayjs,
      getTodoTaskProgressData() {
        this.loading = true;
        apiGetTodoTaskPage(this.params)
          .then((res) => {
            if (res.code === 200 && res.data.draw === this.draw) {
              res.data.data.forEach((res) => {
                res.icon = 'todo|svg';
              });
              this.todoTaskList.push(...res.data.data);
              this.todoTaskListFilterCount = res.data.filterCount;
              this.$emit('setTodoCount', {
                isCompleted: this.isCompleted,
                count: res.data.totalCount,
              });
              this.draw += 1;
            }
            if (res.code !== 200) {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误',
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
      onLoadMore() {
        this.pageIndex += 1;
        this.getTodoTaskProgressData();
      },
      init() {
        this.pageIndex = 0;
        this.searchText = '';
        this.todoTaskListFilterCount = 0;
        this.todoTaskList = [];
        this.getTodoTaskProgressData();
      },
      completeTodoTask(todoTask, index) {
        this.selectIndex = index;
        this.todoTaskList[index].icon = 'todo-c|svg';
        useMessage().createConfirm({
          iconType: 'info',
          title: '确定该待办事项已完成吗？',
          content: todoTask.title,
          onOk: () => {
            this.loading = true;
            apiCompleteTodoTask({
              id: todoTask.id,
              version: todoTask.version,
              completedAt: new Date(),
            })
              .then((res) => {
                if (res.code === 200) {
                  this.$emit('todoTaskCompleted');
                  useMessage().createSuccessNotification({
                    message: '成功',
                    description: '修改成功',
                  });
                } else {
                  useMessage().createErrorNotification({
                    message: '错误',
                    description: res.error.message,
                  });
                }
              })
              .catch((err) => {
                console.error(1111111, err);
                useMessage().createErrorNotification({
                  message: '错误',
                  description: '网络错误2222',
                });
              })
              .finally(() => {
                this.loading = false;
                this.selectIndex = -1;
              });
          },
          onCancel: () => {
            this.selectIndex = -1;
            this.todoTaskList[index].icon = 'todo|svg';
          },
        });
      },
      changeIcon(index) {
        setTimeout(() => {
          this.todoTaskList[index].icon = 'todo-c|svg';
          this.todoTaskList.forEach((val, i) => {
            if (i !== index) {
              val.icon = 'todo|svg';
            }
          });
        }, 100);
      },
      resetIcon(index) {
        setTimeout(() => {
          if (this.selectIndex > -1) {
            return;
          }
          this.todoTaskList[index].icon = 'todo|svg';
        }, 100);
      },
    },
  });
</script>

<style lang="less" scoped>
  .echarts-container {
    height: fit-content;
  }

  .complete-info {
    color: #389e0d;
    font-weight: 500;
  }

  .important-info {
    color: #2a7dc9;
    font-weight: bold;
  }
</style>
