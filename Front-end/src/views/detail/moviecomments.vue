<template>
    <div class="movie-comments" v-if="detailData.list.length">
        <h2 class="intro-title">
            Comments of {{ title }}
        </h2>
        <div class="scroll-wrap">
            <div class="comment-item" v-for="item in detailData.list||[]">
                <div v-if="!isUserInBlacklist(item.user_id)">
                    <div class="top-content" >
                        <span class="nickname">{{ item.username }}</span>
                        <div v-if="item.rating && item.rating.value" class="rankstar"><span class="rank-text">watched</span>
                            <rankstar :score="item.rating.value"/>
                        </div>
                    </div>
                    <div class="content" style="height: auto;">{{ item.text }}</div>
                    <!--          添加一个拉黑评论的按钮-->
                    <button class="btn btn-danger" @click="addtoblacklist(item.user_id,item.username)">Add to Blacklist</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {ref, onMounted, computed, reactive} from 'vue'
import service from '@/utils/service'
import rankstar from '@/components/rankstar/rankstar.vue'
import configapi from '@/utils/configapi'
import Vuex from 'vuex'
import {useRoute} from 'vue-router'
import {useStore} from 'vuex'
import axios from 'axios'
import { watchEffect,watch } from 'vue';

/**
 * 待办事项页面组件
 */
export default {
    name: 'moviecomments',// 组件的名称，尽量和文件名一致
    components: {
        rankstar
    },
    setup() {
      const store = useStore();
      
      const userinfo = computed(() => store.state.userInfo);
      async function addtoblacklist(banned_user_id,banned_username) {
          const userInfo = store.state.userInfo;
          
          if (!userInfo.id) return;
          if(userInfo.id==banned_user_id){
              alert("cannot add yourself to bannedlist")
              return
          }
          try {
              const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/bannedlist", 
              {banned_user_id: banned_user_id,banned_username:banned_username});
              if (response.data) {
                  console.log("add to bannedlist:");
                  alert(response.data.message)
                  console.log(response.data);
              }
          } catch (error) {
              console.error(error);
          }
      };
        const getblacklist=async()=>{

            //const userInfo = store.state.userInfo;
            //if (!userInfo.id) return;
            if(!userinfo){
                return
            }
            try {
                const response = await axios.get("http://localhost:5050/user/" + store.state.userInfo.id + "/bannedlist");
                if (response.data) {
                    console.log("blacklist:");
                    console.log(blacklist);
                    blacklist.value=response.data;
                }
            } catch (error) {
                console.error(error);
            }
        };

        const blacklist=ref([]);
        watch(userinfo, () => {
          getblacklist();
        });
        watchEffect(() => {
          getblacklist();
        });
        async function showComment(movieid) {
            try {
                const response = await axios.get("http://localhost:5050/movies/" + movieid + "/show_comment");
                if (response.data) {
                    console.log("comment:");
                    console.log(response.data);
                    detailData.list = response.data; // Set the result to detailData.list
                }
            } catch (error) {
                console.error(error);
            }
        }
        const title = computed(() => store.state.detailTitle);
        const incommentList = computed(() => store.state.commentList);

        let detailData = reactive({
            list: []
        })
        const route = useRoute()
        let id = computed(() => route.query.id);
        onMounted(async () => {
        await showComment(id.value); // Call the showComment function here
        }

        );

        

        return {
            detailData,
            title,
            addtoblacklist,
            blacklist,
        }
    },
    computed: {
        userinfo() {
            return this.$store.state.userInfo;
        },


    },
    methods: {
        isUserInBlacklist(userId) {
            return this.blacklist.some((blackuser) => blackuser.banned_user_id === userId);
        },
    },
}
</script>
<style scoped lang="less">

.intro-title {
  margin: 24px 0 12px 0;
  font-size: 16px;
  color: #007722;
}

.top-content {
  display: flex;
  align-items: center;

  .avatar {
    width: 24px;
    height: 24px;
  }

  .nickname {
    font-size: 13px;
    margin-left: 10px;
    color: #37a;
    margin-right: 10px;;
  }

  .time {
    font-size: 13px;
    margin-left: 10px;
    color: #999;
  }
}

.comment-item {
  padding: 20px 0px;
  position: relative;
  border-top: 0.5px solid #ddd;
  margin-bottom: 5px;
}

.rankstar {
  display: flex;
  align-items: center;
}

.rank-text {
  margin-right: 3px;
}

.content {
  margin-top: 10px;
  color: #666;
  font-size: 13px;
  line-height: 1.5;
  height: auto;
}

</style>
