
const app = {
  state: () => ({
    transName: "fade",
  }),
  mutations: {
    updateTrans(state, name) {
      state.transName = name;
    },
    updateActivityTypes(state, types) {
      state.activityTypes = types;
    },
  },
  actions: {
    updateTrans(context, name) {
      context.commit("updateTrans", name);
    },

  },
};

export default app;
