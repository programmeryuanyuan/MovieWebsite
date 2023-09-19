<template>
  <div class="register-container">
    <div class="register-content">
      <div class="register-logo"></div>
      <div class="register-title">Register</div>
      <div class="input-wrap">
        <div><input class="register-input" type="text" placeholder="username" v-model="registerInfo.username" /></div>
        <div><input class="register-input" type="password" placeholder="password" v-model="registerInfo.password" /></div>
        <div><input class="register-input" type="password" placeholder="confirm password"
            v-model="registerInfo.confirm_password" /></div>
        <div class="register-btn" @click="register">Sign up</div>
      </div>
      <div class="error-tips" v-if="registerInfo.errorInfo">Incorrect password</div>

      <div class="tips"></div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, computed, onMounted, getCurrentInstance } from 'vue'
import axios from "axios";
import service from '@/utils/service'
import Vuex from 'vuex'
/**
 * 待办事项页面组件
 */
export default {
  name: 'register',// 组件的名称，尽量和文件名一致
  data() {
    return {
      prevRoute: null
    }
  },
  components: {
  },
  setup() {

    let registerInfo = reactive({
      username: '',
      password: '',
      confirm_password: '',
      errorInfo: false
    })

    const store = Vuex.useStore()
    const { proxy } = getCurrentInstance()
    const valid = () => {
      if (registerInfo.username == '') {
        return false
      }
      if (registerInfo.password == '') {
        return false
      }
      if (registerInfo.confirm_password == '') {
        return false
      }
      if (registerInfo.confirm_password != registerInfo.password) {
        return false
      }
      return true
    }

    const register = () => {
      // 验证用户名密码
      if (valid()) {
        registerInfo.errorInfo = false
        const userInfo = {
          username: registerInfo.username,
          password: registerInfo.password

        }
        axios
          .post("http://localhost:5050/register", {
          username: userInfo.username,
          password: userInfo.password,
          })
          .then((response) => {
          console.log(response);
          store.commit('setUser', userInfo)
          if (proxy.prevRoute) {
            proxy.$router.push(proxy.prevRoute)
          }
          })
          .catch((error) => {
          console.log(error);
          registerInfo.errorInfo = true
          });
        

        

      } else {
        registerInfo.errorInfo = true
      }
    }


    return {
      registerInfo,
      register
    }
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      // 获取vm this得到上一个页面路由from
      vm.prevRoute = from;
    })
  }
}
</script>
<style scoped lang="less">
.register-container {
  overflow: hidden;
}

.register-content {
  min-height: 300px;
  width: 340px;
  padding: 50px 30px 100px;
  margin: 0 auto;
  margin-top: 100px;
  overflow: hidden;
  position: relative;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #d8d8d8;
}

.register-title {
  border-bottom: 2px solid #494949;
  color: #333;
  font-weight: 600;
  font-size: 18px;
  width: 150px;
  text-align: center;
  margin: 0 auto;
  margin-top: 20px;
  margin-bottom: 20px;
}

.register-logo {
  width: 225px;
  height: 44px;
  ;
  margin: 0 auto;
  background-size: cover;
  background-image: url('./imgs/logo.png');
}

.input-wrap {
  text-align: center;
}

.register-input {
  width: 280px;
  font-size: 13px;
  padding: 10px;
  border-radius: 3px;
  box-sizing: border-box;
  border: 1px solid #e4e6e5;
  -webkit-appearance: none;
  -webkit-tap-highlight-color: rgba(255, 0, 0, 0);
  background: transparent;
  outline: none;
  margin-top: 7px;
}

.register-btn {
  width: 280px;
  height: 36px;
  border-radius: 3px;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  line-height: 36px;
  text-align: center;
  outline: 0;
  cursor: pointer;
  margin: 0 auto;
  margin-top: 10px;
  background-color: #41ac52;
}

.tips {
  margin-top: 10px;
  color: #ddd;
  text-align: center;
}

.error-tips {
  color: red;
  text-align: left;
  width: 280px;
  margin: 0 auto;
}</style>
