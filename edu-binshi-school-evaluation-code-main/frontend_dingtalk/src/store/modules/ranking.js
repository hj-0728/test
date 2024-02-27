const ranking = {
    state: () => ({
        periodId: '',
        periodName: '',
        filterTopic: '',
        selectedPeriodPath: []
    }),

    mutations: {
        updateRankingSelectedPeriodPath(state, periodList) {
            state.selectedPeriodPath = periodList
        },
        updateRankingPeriodId(state, id) {
            state.periodId = id;
        },
        updateRankingPeriodName(state, name) {
            state.periodName = name;
        },
        updateRankingFilterTopic(state, topic) {
            state.filterTopic = topic;
        },
        resetRanking(state) {
            state.periodId = '';
            state.filterTopic = '';
        }
    },
    actions: {
        updateRankingPeriodId(state, id) {
            state.commit("updateRankingPeriodId", id);
        },
        updateRankingPeriodName(state, name) {
            state.commit("updateRankingPeriodName", name);
        },
        updateRankingFilterTopic(state, topic) {
            state.commit("updateRankingFilterTopic", topic);
        },
        resetRanking(state) {
            state.commit("resetRanking");
        },
        updateSelectedPeriodPath(state, periodList) {
            state.commit("updateRankingSelectedPeriodPath", periodList);
        },
    },
};

export default ranking;
