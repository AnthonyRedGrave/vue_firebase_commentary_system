import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    accessToken: JSON.parse(localStorage.getItem('token')),
    refreshToken: null,
    APIData: [],
    username: JSON.parse(localStorage.getItem('username'))

  },
  mutations: {
    updateStorage (state, {access, refresh, username}){
      state.accessToken = access
      state.refreshToken = refresh
      state.username =  username 
    },
    destroyToken(state){
      console.log("попал")
      state.accessToken = null
      state.refreshToken = null
      state.username =  null
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  },
  getters:{
    loggedIn(state){
      return state.accessToken != null
    }
  },
  actions: {
    userLogin(context, usercredential){
      return new Promise((resolve, reject)=>{
        console.log("userLogin")
        axios({
            method: 'post',
            url: 'http://localhost:8000/api/token/',
            data:{
              username: usercredential.username,
              password: usercredential.password 
            },
            credentials: 'include',
          }).then((responce)=>{
            context.commit('updateStorage', {access: responce.data.access, refresh: responce.data.refresh, username: usercredential.username})
            localStorage.setItem('token', JSON.stringify(responce.data.access))
            localStorage.setItem('username', JSON.stringify(usercredential.username))
            
            resolve(responce)
          })
          .catch(err=>{
            console.log(err)
            reject(err)
          })
      })
       
    },
    userLogout(context){
      if (context.getters.loggedIn){
        context.commit('destroyToken')
      }
    }
  },
  modules: {
  }
})
