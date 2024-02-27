import { createStore } from "vuex";
import app from "./modules/app";
import team from "./modules/team";
import ranking from "./modules/ranking";
const store = createStore({
  modules: {
    App: app,
    Team: team,
    Ranking: ranking,
  },
  getters: {
    transName(state) {
      return state.App.transName;
    },
    userInfo(state) {
      return state.App.userInfo;
    },
  },
});

export default store;
