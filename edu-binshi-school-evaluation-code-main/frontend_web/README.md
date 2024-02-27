```bash
cd vue-vben-admin

pnpm install

```

- run

```bash
pnpm serve
```

- build

```bash
pnpm build
```

# 命名规则

##### 文件夹/.ts 文件/assets 文件：小驼峰

##### .vue 文件：大驼峰

####

# 路由

项目路由配置存放于 [src/router/routes](https://github.com/vbenjs/vue-vben-admin/tree/main/src/router/routes) 下面。 [src/router/routes/modules](https://github.com/vbenjs/vue-vben-admin/tree/main/src/router/routes/modules)用于存放路由模块，在该目录下的文件会自动注册，默认添加到菜单，若不想在菜单显示，添加 hideMenu: true 属性

文件命名方式：小驼峰

# Icon

##### Antv Icon（按需引入）

```
<GithubFilled :style="{ fontSize: '30px' }"/>

import {GithubFilled} from '@ant-design/icons-vue';
components:{
	GithubFilled
}
```

##### Iconify

```
<Icon icon="ion:settings-outline" :size="30" />
import { Icon } from '/@/components/Icon';
components:{
	Icon
}
```

##### Svg

在’/src/assets/icons‘中放入同名 svg 文件

```
<SvgIcon name="test" size="32" />
import { SvgIcon } from '/@/components/Icon';
components:{
	Icon
}
```

建议：

​ 使用 Iconify 线性图标 : https://icones.netlify.app/;

​ size 默认使用 16，特殊情况可自定义；

​ 若在 iconify 中找不到合适的图标，使用 Svg：https://www.iconfont.cn/

# 消息实例

##### 需确认的对话框

```
useMessage().createConfirm({
	iconType: type: 'warning' | 'error' | 'success' | 'info',
    title: 'Tip',
    content: 'content message...',
});
```

##### 无需确认的提示框

```
useMessage().createInfoNotification({
	message: 'Tip',
	description: 'content message...',
})
createInfoNotification;
createErrorNotification;
createWarningNotification;
createSuccessNotification;
```

# 弹窗

统一用 vben 的打开方式

```
const [register, { openModal }] = useModal();
this.openModal(true,data)
```

# Button

建议使用 vben 的 button

type 与 ant 一样，区别是多了 color 属性，目前修改后拥有的 color 属性：['error', 'warning', 'success', 'edit', 'purple', 'blue', 'green', 'orange']

若想使用间距，默认从左往右数第二个 button 起添加 ‘ class：ant-btn-left-margin ’ 默认间距 8px

# ts 强制声明类型，api 爱写不写

# Tree(ant design vue 2.x -> ant design vue 3.x)

replaceFields 已被废弃，应使用 fieldNames

# Table(ant design vue 2.x -> ant design vue 3.x)

1.原来定义在 columns 里的插槽已被废弃，应使用 bodyCell，用 column.dataIndex 判断列

```
<template #bodyCell="{ text, record, index, column }">
 <template v-if="column.dataIndex === 'mobile_list'">
   <div v-for="mobile in record['mobile_list']" :key="'mobile' + mobile">
      {{ mobile }}
   </div>
   </template>
   <template v-if="column.dataIndex === 'operation'">
     <Button
        type="primary"
        preIcon="ant-design:eye-outlined"
        :iconSize="16"
        color="edit"
        @click.stop=""
     >
       查看
    </Button>
 </template>
</template>
```

2.标题 tableTitle

```
<template #tableTitle>
</template>
```

3.工具栏 toolbar

```
<template #toolbar>
</template>
```

4.table 筛选 点击重置按钮时不会触发更新，点击 drop down 外面才触发更新，

如果出现这种情况，请使用：frontend_web/src/components/Table/src/components/filters/Filters.vue

参考：frontend_web/src/components/DeptPeopleSelect/src/PeopleList.vue

5.table 高度设置

###### 父 div (此处指让 div 撑满页面)，这么做为了防止 table 出现多余的滚动条背景（怎么方便怎么来，此处不固定） :

```
height: calc(100vh - 115px);
background-color: white;
overflow: hidden;
```

###### template :

```
<BasicTable :scroll="{ y: tableHeight }">
</BasicTable>
```

###### import :

```
import { getTableHeight } from '/@/utils/helper/tableHelper';
```

###### setup :

```
setup() {
    const tableHeight = ref<Number>(getTableHeight(document));
    return { tableHeight }
}
```
