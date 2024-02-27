<template>
  <a-list :class="prefixCls" bordered :pagination="getPagination">
    <template v-for="item in getData" :key="item.id">
      <a-list-item class="list-item">
        <a-list-item-meta>
          <template #title>
            <div class="title">
              <a-typography-paragraph
                @click="handleTitleClick(item)"
                style="width: 100%; margin-bottom: 0 !important; color: #2a7dc9"
                :style="{ cursor: isTitleClickable ? 'pointer' : '' }"
                :delete="!!item.titleDelete"
                :ellipsis="
                  $props.titleRows && $props.titleRows > 0
                    ? { rows: $props.titleRows, tooltip: !!item.title }
                    : false
                "
                :content="item.title ? item.title : item.content"
              />
              <div class="extra" v-if="item.extra">
                <a-tag class="tag" :color="item.color">
                  {{ item.extra }}
                </a-tag>
              </div>
            </div>
          </template>

          <template #avatar>
            <a-avatar
              class="avatar"
              :src="'https://gw.alipayobjects.com/zos/rmsportal/ThXAXghbEsBCCSDihZxY.png'"
            />
          </template>

          <template #description>
            <div>
              <div class="description" v-if="item.content">
                <a-typography-paragraph
                  style="width: 100%; margin-bottom: 0 !important"
                  :ellipsis="
                    $props.descRows && $props.descRows > 0
                      ? { rows: $props.descRows, tooltip: !!item.content }
                      : false
                  "
                  :content="prepare(item.content)"
                />
              </div>
              <div class="datetime">
                {{ dayjs(item.createdAt).format('YYYY-MM-DD HH:mm') }}
              </div>
            </div>
          </template>
        </a-list-item-meta>
      </a-list-item>
    </template>
  </a-list>
</template>
<script lang="ts">
  import { computed, defineComponent, PropType, ref, watch, unref, inject } from 'vue';
  import { ListItem } from './data';
  import { useDesign } from '/@/hooks/web/useDesign';
  import { List, Avatar, Tag, Typography } from 'ant-design-vue';
  import { isNumber } from '/@/utils/is';
  import dayjs from 'dayjs';

  export default defineComponent({
    components: {
      [Avatar.name]: Avatar,
      [List.name]: List,
      [List.Item.name]: List.Item,
      AListItemMeta: List.Item.Meta,
      ATypographyParagraph: Typography.Paragraph,
      [Tag.name]: Tag,
    },
    props: {
      list: {
        type: Array as PropType<ListItem[]>,
        default: () => [],
      },
      pageSize: {
        type: [Boolean, Number] as PropType<Boolean | Number>,
        default: 4,
      },
      totalCount: {
        type: Number,
        default: 0,
      },
      currentPage: {
        type: Number,
        default: 1,
      },
      titleRows: {
        type: Number,
        default: 1,
      },
      descRows: {
        type: Number,
        default: 2,
      },
      onTitleClick: {
        type: Function as PropType<(Recordable) => void>,
      },
    },
    emits: ['update:currentPage', 'getMessage', 'updateExistUnreadMessage'],
    setup(props, { emit }) {
      console.log(props.list);
      const noticeVisible = inject('noticeVisible');
      const { prefixCls } = useDesign('header-notify-list');
      const current = ref(props.currentPage || 1);
      const getData = computed(() => {
        const { pageSize, list } = props;
        if (pageSize === false) return [];
        let size = isNumber(pageSize) ? pageSize : 5;
        return list.slice(size * (unref(current) - 1), size * unref(current));
      });
      watch(
        () => props.currentPage,
        (v) => {
          current.value = v;
        },
      );
      watch(noticeVisible, () => {
        if (!noticeVisible.value) {
          current.value = 1;
        }
      });
      const isTitleClickable = computed(() => !!props.onTitleClick);
      const getPagination = computed(() => {
        const { list, pageSize } = props;
        if (pageSize > 0 && list && props.totalCount > pageSize) {
          return {
            total: props.totalCount,
            pageSize,
            simple: true,
            //size: 'small',
            current: unref(current),
            onChange(page) {
              current.value = page;
              emit('update:currentPage', page);
              // emit('getMessage', page);
            },
          };
        } else {
          return false;
        }
      });

      function handleTitleClick(item: ListItem) {
        if (props.list.length === 1) {
          emit('updateExistUnreadMessage', false);
        }
        current.value = 1;
        props.onTitleClick && props.onTitleClick(item);
      }

      return { prefixCls, getPagination, getData, handleTitleClick, isTitleClickable, dayjs };
    },
    methods: {
      getMessageList(page, pageSize) {
        console.log(page);
        console.log(pageSize);
      },
      prepare(content) {
        content = content.replace(/<[^>]+>/g, '');
        return content;
      },
    },
  });
</script>
<style lang="less" scoped>
  @prefix-cls: ~'@{namespace}-header-notify-list';

  .@{prefix-cls} {
    &::-webkit-scrollbar {
      display: none;
    }

    ::v-deep(.ant-pagination-disabled) {
      display: inline-block !important;
    }

    &-item {
      padding: 6px;
      overflow: hidden;
      cursor: pointer;
      transition: all 0.3s;

      .title {
        margin-bottom: 8px;
        font-weight: normal;

        .extra {
          float: right;
          margin-top: -1.5px;
          margin-right: 0;
          font-weight: normal;

          .tag {
            margin-right: 0;
          }
        }

        .avatar {
          margin-top: 4px;
        }

        .description {
          font-size: 12px;
          line-height: 18px;
        }

        .datetime {
          margin-top: 4px;
          font-size: 12px;
          line-height: 18px;
        }
      }
    }
  }
</style>
