import type { App } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedState from 'pinia-plugin-persistedstate';
const store = createPinia();
store.use(piniaPluginPersistedState);
export function setupStore(app: App<Element>) {
  app.use(store);
}

export { store };
