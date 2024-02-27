import { createApp } from "vue";
import store from "./store";
import App from "./App.vue";
import router from "./router";
import HorizSpacer from "./components/HorizSpacer.vue";
import axios from "axios";
import VueAxios from "vue-axios";
import dayjs from "dayjs";
import lodash from 'lodash';
import "vant/lib/index.css";
import { regGlobalFilters } from './misc/global-filters';
import VueClipboard from 'vue-clipboard2';

import {
  NavBar,
  Icon,
  Button,
  Cell,
  CellGroup,
  Image,
  Loading,
  Notify,
  Dialog,
  Toast,
  Divider
} from "vant";


const env = import.meta.env;

VueClipboard.config.autoSetContainer = true // add this line

axios.defaults.baseURL = env.VITE_GLOB_API_URL
const app = createApp(App)
app.config.globalProperties.$D = dayjs;
app.config.globalProperties.__ = lodash; // 组件内可使用 this.__ 调用lodash
regGlobalFilters(app)
app.use(store)
  // 加载第三方组件
  .use(router)
  .use(VueAxios, axios)
  // vant 全局组件
  .use(NavBar)
  .use(Image)
  .use(Icon)
  .use(Button)
  .use(Cell)
  .use(CellGroup)
  .use(Loading)
  .use(Notify)
  .use(Dialog)
  .use(Toast)
  .use(Divider)
  .use(VueClipboard)
  // 加载全局自定义组件
  .component(HorizSpacer.name, HorizSpacer);
// 全局directive
app.directive("bg", {
  mounted(el, binding) {
    el.style.background = binding.value;
  },
});

// Padding
app.directive("pd", {
  mounted(el, binding) {
    el.style.padding = binding.value;
    el.style.width = "auto";
  },
});

// border radius
app.directive("rds", {
  mounted(el, binding) {
    el.style.borderRadius = binding.value;
  },
});

// margin
app.directive("mg", {
  mounted(el, binding) {
    el.style.margin = binding.value;
    el.style.width = "auto";
  },
});

app.mount('#app');
