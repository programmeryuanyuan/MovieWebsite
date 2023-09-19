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
            </div>>
            <!--       TODO 选择标签  后面可以在数据库查询 查询用户选择的的-->
            <div id="label_container">
                <div id="label" class="block">
                    <button type="button" class="btn btn-light margin">Comedy</button>
                    <button type="button" class="btn btn-light margin">Romance</button>
                </div>
                <div id="select_container">
                    <button type="button" id="selectLabel" class="btn btn-dark" @click="toDisplay">select label</button>
                </div>
            </div>
            
            <!--       TODO 选择标签  后面可以在数据库查询 查询全部的-->               
            

            

            <input type="file" ref="backgroundInput" @change="handleBackgroundFileChange" style="display:none;">
            
            <div class="my-fav play-section">
                <h2 class="title">My favorite movie:</h2>
                <div class="section-bottom" v-if="nowplayList && nowplayList.length">
                    <slider>
                        <mitem v-for="item in nowplayList" :itemData="item" :key="item.id" />
                    </slider>
                </div>
            </div>
            <div class="wish-list play-section">
                <h2 class="title">Wish list:</h2>
                <div class="section-bottom" v-if="recentplayList && recentplayList.length">
                    <slider>
                        <div v-for="(item, index) in recentplayList" :key="index" class="recent-item">
                            <mitem v-for="(_item, _index) in item" :itemData="_item" :key="_item.id" />
                        </div>
                    </slider>
                </div>
            </div>
            <div class="user-blacklist">
                <h2 class="title">Black List</h2>
                <div class="section-bottom" v-if="rankList && rankList.length">
                    <slider>
                    </slider>
                </div>
            </div>
            <div class="user-comments">
                <h2 class="title">Comments</h2>
                <div class="section-bottom" v-if="rankList && rankList.length">
                    <slider>
                    </slider>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import mitem from '@/components/mitem/mitem.vue'
import slider from '@/components/slider/slider.vue'
import { reactive, ref, computed } from 'vue'
import axios from "axios"
import service from '@/utils/service'
import Vuex from 'vuex'
import configapi from '@/utils/configapi'
import { watchEffect } from 'vue';
import { useStore } from 'vuex'
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
        slider
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
            console.log(this.$store.state.userInfo.banner);
            const bgUrl = this.$store.state.userInfo.banner;
            return bgUrl ? `data:image/png;base64,${bgUrl}` : '../../assets/bg.jpg';
            // 如果有背景图片URL，就使用它；否则使用默认的背景图片URL
        },

    },
    setup() {
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
        const addtobannedlist=async(userid)=>{
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/bannedlist", 
                {user_id:userid,},config);
                if (response.data) {
                    console.log("add to bannedlist:");
                    console.log(response.data);
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
                    console.log(response.data);
                }
            } catch (error) {
                console.error(error);
            }
        };
        const getwishlist = async () => {
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.get("http://localhost:5050/user/" + userInfo.id + "/wishlist",config);
                if (response.data) {
                    console.log("wishlist:");
                    console.log(response.data);
                }
            } catch (error) {
                console.error(error);
            }
        };
        const addtowishlist = async (movieid,movietitle) => {
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/wishlist", 
                {movie_id:movieid,movie_title:movietitle,},config);
                if (response.data) {
                    console.log("add to wishlist:");
                    console.log(response.data);
                }
            } catch (error) {
                console.error(error);
            }
        };
        const sendcomment = async (movieid,comment,rating) => {
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/add_comment", 
                {movie_id:movieid,comment_text:comment,rating:rating,pfp:userInfo.pfp},config);
                if (response.data) {
                    console.log("comment sent:");
                    console.log(response.data);
                }
            } catch (error) {
                console.error(error);
            }   
        };
        const showcomment=async(movieid)=>{
            try{const response=await axios.get("http://localhost:5050/movies/"+movieid+"/show_comment",config);
                if(response.data){
                    console.log("comment:");
                    console.log(response.data);
                }
            }catch(error){
                console.error(error);
            }
        }
        const setfavoritemovie=async(movieid)=>{
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/set_favorite_movie", 
                {movie_id:movieid,},config);
                if (response.data) {
                    console.log("add to favorite movie:");
                    console.log(response.data);
                }
            } catch (error) {
                console.error(error);
            }
        }
        const getmoviesbygenre=async(genre)=>{
            try{const response=await axios.post("http://localhost:5050/movies/genre",{genre_name:genre,},config);
                if(response.data){
                    console.log("movies by genre:");
                    console.log(response.data);
                }
            }catch(error){
                console.error(error);
            }
        }
        watchEffect(() => {
            //getwishlist ();
            //addtowishlist(100,"Lock, Stock and Two Smoking Barrels");
            //getblacklist();
            //addtobannedlist(3);
            //sendcomment(100,"test",5);
            //showcomment(100);
            //setfavoritemovie(100);
            //getmoviesbygenre('Action');
        });

        return {
            nowplayList,
            recentplayList,
            rankList,
            
            
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
                    if (response.data && response.data.background_url) {
                        document.body.style.backgroundImage = `url(${response.data.background_url})`;
                    }

                } catch (error) {
                    console.error(error);
                }
            }
        },
    },
}
</script>
<style scoped lang="less">
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css');

.block {
  display: block;
}
.info-bg {
  display: flex;
  flex-direction: column;
  //background-image: url(' + backgroundURL + ') !important;
  height: auto;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
  background-attachment: scroll;
  font-family: 'IBM Plex Sans', sans-serif;
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
  opacity: 0.01;
  cursor: pointer;
}

.info-container {
    display: flex;
    background-color: rgba(255, 255, 255, 0.8);
    /* 设置内容区域半透明白色背景色 */
}

.left-content {
    display: flex;
    flex-direction: column;
    width: 1040px;
}

.right-content {
    width: 300px;
    margin-left: 20px;
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
    padding: 30px 22px;
}

.avatar {
    width: 60px;
    height: 60px;
    align-self: center;

    img {
        width: 100%;
        height: 100%;
    }
}

.username {
    align-self: center;
    font-size: 16px;
}

#cbg {
    display: flex;
    margin-right: 22px;
    /* 右外边距 */
    height: 30px;
    min-width: 20px;
    /* 最短20px */
    padding: 0 8px;
    /* 按钮内容与按钮边缘的距离 */
    font-size: 14px;
    line-height: 1.5;
    border-radius: .25rem;
    cursor: pointer;
}

.my-fav {
    min-height: 344px;
}

.wish-list {
    min-height: 565px;
}

.play-section {
    padding: 15px;
}

.recent-item {
    display: inline-block;
    width: 675px;
    white-space: normal;
}

.blacklist {
    margin-top: 68px;
}

.rank-item {
    padding: 7px 0;
    border-bottom: 1px solid #eaeaea;
    font-size: 13px;
    margin-bottom: 5px;
}

.rank-link {
    margin-left: 7px;
}

.coopt,
.fans {
    margin-top: 50px;
}

.fans-list {
    display: flex;
}

.fans-item {
    text-align: center;
    margin-right: 20px;
}

.fans-img {
    width: 40px;
    height: 40px;
    background-size: cover;
    margin-bottom: 10px;
}

#label_container {
  display: flex; /* 将 label 和 select label 上 */
  flex-wrap: wrap;
  flex-direction: column;
  justify-content: center; /* 水平居中 */
}

#label {
  display: flex; /* 将标签按钮放置在一行上 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  flex-wrap: wrap; /* 如果按钮的数量超出了容器的宽度，则将它们放置在新行上 */
}

#label button {
  margin: 5px; /* 添加间距 */
}

#selectLabel {
  justify-content: center;
  /*display: block; 将 select label 按钮放置在一列上 */
  margin-top: 10px; /* 在标签按钮和 select label 按钮之间添加一些间距 */
  margin-left:50px;
}
</style>  