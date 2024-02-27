
const team = {
    state: () => ({
        scopeId: null,
        showTeam: false,
        teamCategoryId: '',
        gradeId: null,
        myDeptCount: 0,
        endFirstLoading: false,
        sortBy: 'TOTAL',
        canEditTeamCategory: false
    }),

    mutations: {
        updateShowTeam(state, show) {
            state.showTeam = show;
            if (!show) {
                state.teamCategoryId = '';
            }
        },
        updateScopeId(state, id) {
            state.scopeId = id;
        },
        updateTeamCategoryId(state, id) {
            state.teamCategoryId = id;
        },
        updateCanEditTeamCategory(state, canEdit) {
            state.canEditTeamCategory = canEdit;
        },
        updateGradeId(state, id) {
            state.gradeId = id;
        },
        updateMyDeptCount(state, count) {
            state.myDeptCount = count;
        },
        reset(state) {
            state.scopeId = null;
            state.showTeam = false;
            state.gradeId = null;
            state.myDeptCount = 0;
            state.teamCategoryId = '';
            state.sortBy = 'TOTAL';
        },
        updateEndFirstLoading(state, end) {
            state.endFirstLoading = end;
        },
        updateSortBy(state, sortBy) {
            state.sortBy = sortBy;
        }

    },
    actions: {
        updateShowTeam(context, show) {
            context.commit("updateShowTeam", show);
        },
        updateScopeId(context, id) {
            context.commit("updateScopeId", id);
        },
        updateTeamCategoryId(context, id) {
            context.commit("updateTeamCategoryId", id);
        },
        updateCanEditTeamCategory(context, id) {
            context.commit("updateCanEditTeamCategory", id);
        },
        updateGradeId(context, id) {
            context.commit("updateGradeId", id);
        },
        updateMyDeptCount(context, count) {
            context.commit("updateMyDeptCount", count);
        },
        reset(state) {
            state.commit("reset");
        },
        updateEndFirstLoading(context, end) {
            context.commit("updateEndFirstLoading", end);
        },
        updateSortBy(context, sortBy) {
            context.commit("updateSortBy", sortBy);
        }
    },
};

export default team;
