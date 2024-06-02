import { createStore } from 'vuex'

export default createStore({
  state: {
    logged_in: false,
    user_id: '',
    token: '',
  },
  getters: {
  },
  mutations: {
    login(state, data){
      state.logged_in = true
      state.user_id = data.user_id
      state.token = data.token
    },

    logout(state){
      state.logged_in = false
    }
  },
  actions: {
  },
  modules: {
  }
})
