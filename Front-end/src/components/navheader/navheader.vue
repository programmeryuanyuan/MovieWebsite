<template>
  <div class="nav-wapper">
    <div class="nav-header">
        <div class="nav-logo" @click="$router.push('/')"></div>
        <div class="nav-search">
            <input id="inp" placeholder="Search" v-model.trim="searchText"/>
            <div class="search-btn" @click="goSearch"></div>
        </div>
        <!-- to add -->
        <div v-if="user.username" class="nickname">
          <div @click="$router.push('/info')">Welcome,{{user.username}}&nbsp;&nbsp;</div>
          <a id="logout" @click=logout()>Logout</a>
        </div>
        <!-- to add -->
        <div v-else class="nickname">
          <div @click="$router.push('/login')">
            Login
          </div>
          <div>&nbsp; or &nbsp;</div>
          <div @click="$router.push('/Register')">Register
          </div>
        </div>
        
    </div>
  </div>
</template>

<script>
  import {ref,onMounted,computed, reactive,watchEffect} from 'vue'
  import Vuex from 'vuex'
  import {useRoute} from 'vue-router'

  export default  {
    name: 'navheader',

    setup(props,context){
      onMounted(() => {
            const user = JSON.parse(localStorage.getItem('user'))
            if (user) {
                store.commit('setUser', user)
            }
        })
      const store = Vuex.useStore()
      const router = useRoute()
      const user = computed(() => store.state.userInfo);
      const searchText = ref('');
      //to add
      const logout= ()=>{
        store.commit('setUser',{})
        localStorage.removeItem('user');
        localStorage.removeItem('searchHistory');
      }
      watchEffect(()=>{
        searchText.value = router.query.searchText
      })




      return {
        user,
        searchText,
        logout
      }
    },
    methods:{
      goSearch(){
        this.$router.push({
          path:'/search',
          query:{
            searchText:this.searchText
          }
        })
      }
      
    }

  }
</script>

<style scoped lang="less">
  .nav-wapper {
      background-color:#f0f3f5;
      width: 100%;
  }
  .nav-header {
    width: 1040px;
    margin: 0 auto;
    height:75px;
    overflow: hidden;
    background-color:#f0f3f5;
    display: flex;
    position: relative;
  }


  .nav-logo {
      width: 230px;
      height: 54px;
      background-image: url('./imgs/lg_movie@2x.png');
      background-repeat: no-repeat;
      background-position: 0 center;
      background-size: 54% 50%;
      margin-top: 11px;
      align-self: flex-start;
      cursor: pointer;
  }

  .nav-search {
      margin-left: -30px;
      height: 32px;
      align-self: center;
      background-image: url('./imgs/nav_mv_bg.png');
      border-radius: 3px;
      background-color: #fff;
      display: flex;
      #inp {
          width: 460px;
          height: 28px;
          outline: none;
          background-color: #fff;
          border: none;
          -webkit-appearance: none;
          margin-top: 2px;
          text-indent: 11px;
      }
  }
  .search-btn {
      width: 35px;
      height: 32px;
      background-image: url('./imgs/nav_mv_bg.png');
      background-position: -40px 35px;
      border-radius: 3px;
      cursor: pointer;
  }
  .nickname {
      display: flex;
      flex-direction: row;
      position: absolute;
      top:28px;
      right:10px;
      cursor: pointer;
  }

  #logout{
    color: #858585;
    margin-left: 10px;
  }
  
</style>
