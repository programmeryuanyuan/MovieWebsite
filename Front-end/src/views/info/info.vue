<template>
    <div class="info-bg" :style="{ backgroundImage: `url(${backgroundURL})` }" 
     style="height:auto; min-height: 100%; ">

     <div class="info-container">
        <div class="left-content">
            <div class="basic-info">
                <div class="avatar">
                    <div class="avatar-wrapper" @click="handleAvatarClick">
                        <input type="file" ref="fileInput" @change="handleFileChange" class="file-input" >

                        <img :src="pfpURL" alt="Profile Picture">
                    </div>
                    <div class="username" value="argo">{{ userinfo.username }}</div>
                </div>
                <button type="button" class="btn btn-dark" id="cbg" @click="handleCustomBackgroundClick">custom background</button>
            </div>
            <div id="label_container">
                <div id="label" class="block">
                    <div v-for="(achivement, index) in achivements" :key="index">
                        <button type="button" class="btn btn-light margin" v-if="achivement">{{ achivement }}</button>
                    </div>
                </div>

            </div>
            
                     
            

            

            <input type="file" ref="backgroundInput" @change="handleBackgroundFileChange" style="display:none;">
            
            <div class="my-fav play-section">
                <h2 class="title">My favorite movie:</h2>
                <favorite/>
            </div>
            
            <div class="user-blacklist" v-if="blacklist.length">
                <h2 class="title">Black List</h2>
                <div class="section-bottom">
                    <div class="blacklist-container">
                        <div v-for="(blackuser, index) in blacklist" :key="index" class="blacklist-item">
                            <div class="blacklist-user">
                                <i class="fas fa-user"></i>
                                <span>{{ blackuser.banned_username }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="wish-list play-section">
                <h2 class="title">Wish list:</h2>
                        <div class="wishlist-container">
                            <router-link
                                v-for="(wishmovie, index) in wishlist"
                                :key="index"
                                :to="'/detail?id=' + wishmovie.movie_id">
                                <div class="wishlist-item">
                                    <div>{{ wishmovie.movie_title }}</div>
                                </div>
                            </router-link>
                        </div>
                
            </div>
            
        </div>
    </div>
</div>
</template>

<script>
import { onMounted } from 'vue';
import mitem from '@/components/mitem/mitem.vue'
import slider from '@/components/slider/slider.vue'
import { reactive, ref, computed } from 'vue'
import axios from "axios"
import service from '@/utils/service'
import Vuex from 'vuex'
import configapi from '@/utils/configapi'
import { watchEffect } from 'vue';
import { useStore } from 'vuex'
import favorite from "./favorite.vue"
/**
 * 首页页面组件
 */
export default {
    // 定义静态方法
    asyncData({ store }) {
        return store.dispatch('getHomeMovieData')
    },
    name: 'info',// 组件的名称尽量和文件名一致
    data(){
        return{
            change_profile: false,
            //achivements:[]
        };
    },
    components: {
        mitem,
        slider,
        favorite
    },
    computed: {
        userinfo() {
            return this.$store.state.userInfo;
        },
        pfpURL() {
            console.log(this.$store.state.userInfo.pfp);
            const pfp = this.$store.state.userInfo.pfp;
            return pfp ? `data:image/png;base64,${pfp}` : './avatar.jpg';
            // This will create a URL from the pfp Blob and return it.
            // If there is no pfp, it will return the URL of the default profile picture.   
        },
        backgroundURL() {
            //console.log(this.$store.state.userInfo.banner);
            const bgUrl = this.$store.state.userInfo.banner;
            return bgUrl ? `data:image/png;base64,${bgUrl}` : '../../assets/bg.jpg';
            // 如果有背景图片URL，就使用它；否则使用默认的背景图片URL
        },

    },
    setup() {
        onMounted(() => {
            const user = JSON.parse(localStorage.getItem('user'))
            if (user) {
                store.commit('setUser', user)
            }
        })
        const store = useStore()
        //const user = computed(() => store.state.userInfo);      
        //console.log(store.state.userInfo);     
        // 从store获取数据
        let nowplayList = computed(() => store.state.nowplayList)
        let recentplayList = computed(() => store.state.recentplayList)
        let rankList = computed(() => store.state.rankList)
        
        const config = {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        };
        const getwishlist = async () => {
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.get("http://localhost:5050/user/" + userInfo.id + "/wishlist",config);
                if (response.data) {
                    console.log(response.data)
                    wishlist.value=response.data;
                }
            } catch (error) {
                console.error(error);
            }
        };
        const getAchivements = async () => {
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.get("http://localhost:5050/user/" + userInfo.id + "/achievements",config);
                if (response.data) {
                    //console.log("achivements:");
                    //console.log(response.data);
                    achivements.value=response.data;
                }
            } catch (error) {
                console.error(error);
            }
        };
        const getblacklist=async()=>{
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.get("http://localhost:5050/user/" + userInfo.id + "/bannedlist",config);
                if (response.data) {
                    console.log("blacklist:");
                    console.log(blacklist);
                    blacklist.value=response.data;
                }
            } catch (error) {
                console.error(error);
            }
        };
        const achivements = ref([])
        const wishlist=ref([])
        const blacklist=ref([]);
        watchEffect(() => {
            getAchivements();
            getwishlist();
            getblacklist();
        });

        return {
            nowplayList,
            recentplayList,
            rankList,
            achivements,
            wishlist,
            blacklist,
            
        }
    },
    
    methods: {
        
        handleAvatarClick() {
            //console.log("click");
            this.change_profile=true;
            this.$refs.fileInput.click();
        },
        
        async handleFileChange(event) {
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append("file", file);
            formData.append("username", this.userinfo.username);
            console.log("file uploaded");
            if (file) {
      
                try {

                    axios
                        .post("http://localhost:5050/user/"+this.userinfo.id+"/upload_pfp", formData)
                                .then((response) => {
                                console.log(response);
                                })
                                .catch((error) => {
                                console.log(error);
                                });
                    
                } catch (error) {
                    console.error(error);
                }
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => {
                    //const store=this.$store
                    //store.dispatch('updateBanner', reader.result);
                    this.$store.state.userInfo.banner = `${reader.result}`;
                    let user0 = JSON.parse(localStorage.getItem("user"));
                    user0.pfp = reader.result.split(",")[1];
                    localStorage.setItem("user", JSON.stringify(user0));
                    console.log(reader.result);
                    
                    //console.log(this.$store.state.userInfo.banner);
                    //this.$forceUpdate();
                };
            }
            
        
        },

        handleCustomBackgroundClick() {
            // 触发隐藏的文件输入元素的点击事件
            this.$refs.backgroundInput.click();
        },
        
        async handleBackgroundFileChange(event) {
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append("file", file);
            formData.append("username", this.userinfo.username);

            if (file) {
                try {
                    const response = await axios.post(
                        "http://localhost:5050/user/" + this.userinfo.id + "/upload_banner",
                        formData
                    );

                    console.log(response);
                    
                    // 如果上传成功，使用新的背景图片 URL 更新页面背景
                    
                        
                    

                } catch (error) {
                    console.error(error);
                }

                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => {
                    //const store=this.$store
                    //store.dispatch('updateBanner', reader.result);
                    this.$store.state.userInfo.banner = `${reader.result}`;
                    let user0 = JSON.parse(localStorage.getItem("user"));
                    user0.banner = reader.result.split(",")[1];
                    localStorage.setItem("user", JSON.stringify(user0));
                    console.log(reader.result);
                    
                    //console.log(this.$store.state.userInfo.banner);
                    //this.$forceUpdate();
                };
            }
        },
    },
}
</script>
<style scoped lang="less">
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css');

.info-bg {
display: flex;
flex-direction: column;
height: auto;
background-repeat: no-repeat;
background-size: cover;
background-attachment: fixed;
background-position: center;
background-attachment: scroll;
font-family: 'IBM Plex Sans', sans-serif;
box-shadow: inset 0 0 0 1000px rgba(0, 0, 0, 0.3);
}

.avatar-wrapper {
position: relative;
display: inline-block;
}

.file-input {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
opacity: 0;
cursor: pointer;
}

.info-container {
display: flex;
background-color: rgba(255, 255, 255, 0.9);
border-radius: 10px;
overflow: hidden;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.left-content {
display: flex;
flex-direction: column;
width: 1040px;
padding: 20px;
}

.title {
font-size: 25px;
font-weight: 500;
color: #111;
padding-bottom: 10px;
border-bottom: 1px solid #eaeaea;
margin-bottom: 18px;
}

.basic-info {
height: 150px;
display: flex;
flex-direction: row;
justify-content: space-between;
align-items: center;
}

.avatar {
width: 60px;
height: 60px;
align-self: center;

img {
width: 100%;
height: 100%;
border-radius: 50%;
}
}

.username {
align-self: center;
font-size: 16px;
font-weight: bold;
}

#cbg {
background-color: #333;
color: #fff;
height: 30px;
min-width: 20px;
padding: 0 8px;
font-size: 14px;
line-height: 1.5;
border-radius: 4px;
cursor: pointer;
border: none;
}

.my-fav,
.wish-list {
background-color: #f5f5f5;
padding: 20px;
border-radius: 8px;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.08);
margin-bottom: 20px;
}

.wishlist-container {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
gap: 20px;
padding: 0;
}

.wishlist-item {
  text-align: center;
  border: 2px solid #ccc;
  border-radius: 50%;
  padding: 20px;
  box-sizing: border-box;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.08);
  color: #333;
  transition: all 0.3s;
}

.wishlist-item:hover {
  background-color: #ccc;
  color: #333;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.16), 0 1px 3px rgba(0, 0, 0, 0.12);
}


#label_container {
display: flex;
flex-wrap: wrap;
flex-direction: column;
align-items: center;
margin-bottom: 20px;
}

#label {
display: flex;
justify-content: center;
align-items: center;
flex-wrap: wrap;
}

#label button {
background-color: #4a4a4a;
color: #fff;
margin: 5px;
border-radius: 4px;
border: none;
padding: 5px 10px;
font-size: 14px;
cursor: pointer;
transition: all 0.3s;
}

#label button:hover {
background-color: #333;
}

.blacklist-item {
margin-bottom: 10px;
padding: 10px;
background-color: #fff;
border-radius: 5px;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.08);
}

.blacklist-item:last-child {
margin-bottom: 0;
}

.blacklist-user {
display: flex;
align-items: center;
}

.blacklist-user i {
color: #4a4a4a;
font-size: 20px;
margin-right: 10px;
}

.blacklist-user span {
font-size: 18px;
}

.user-blacklist {
padding: 15px;
background-color: #f5f5f5;
border-radius: 8px;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.08);
margin-bottom: 20px;
}
</style>  