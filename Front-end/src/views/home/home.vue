<template>
    <div class="home-container">
        <div class="left-content">
            <h2 class="title">TOP:</h2>
            <div class="now-play play-section">
                <div v-for="item in rankList" :key="item.id" @click="toDetail(item.id)" class="handClick">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + item.poster_path" class="movie-img" alt="NULL">
                    <div class="movie-img">
                        <span style="color: deeppink">{{ item.release_date }}</span>
                        <!--  -->
                        <div class="score" v-if="item.vote_average">
                            <div class="score-content">
                                <rankstar :score="Number(item.vote_average)" />
                            </div>
                        </div>
                        <div class="no-score" v-else> Null </div>
                        <!--  -->
                        <div class="title-text">
                            <p>{{ item.title }}</p>
                        </div>
                        <br />
                    </div>
                </div>
            </div>
            <div class="now-play play-section">
                <div v-for="item in rankList2" :key="item.id" @click="toDetail(item.id)" class="handClick">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + item.poster_path" class="movie-img" alt="NULL">
                    <div class="movie-img">
                        <span style="color: deeppink">{{ item.release_date }}</span><br />
                        <!--  -->
                        <div class="score" v-if="item.vote_average">
                            <div class="score-content">
                                <rankstar :score="Number(item.vote_average)" />
                            </div>
                        </div>
                        <div class="no-score" v-else> Null </div>
                        <!--  -->
                        <div class="title-text">
                            <p>{{ item.title }}</p>
                        </div>

                    </div>
                </div>
            </div>
            <h2 class="title">Now:</h2>
            <div class="recent-play play-section">
                <span v-for="item in nowplayList" :key="item.id" @click="toDetail(item.id)" class="handClick">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + item.poster_path" class="movie-img" alt="NULL">
                    <div class="movie-img">
                        <span style="color: deeppink">{{ item.release_date }}</span><br />
                        <!--  -->
                        <div class="score" v-if="item.vote_average">
                            <div class="score-content">
                                <rankstar :score="Number(item.vote_average)" />
                            </div>
                        </div>
                        <div class="no-score" v-else> Null </div>
                        <!--  -->
                        <div class="title-text">
                            <p>{{ item.title }}</p>
                        </div>

                        <br />
                    </div>
                </span>
            </div>
            <div class="recent-play play-section">
                <span v-for="item in nowplayList2" :key="item.id" @click="toDetail(item.id)" class="handClick">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + item.poster_path" class="movie-img" alt="NULL">
                    <div class="movie-img">
                        <span style="color: deeppink">{{ item.release_date }}</span><br />
                        <!--  -->
                        <div class="score" v-if="item.vote_average">
                            <div class="score-content">
                                <rankstar :score="Number(item.vote_average)" />
                            </div>
                        </div>
                        <div class="no-score" v-else> Null </div>
                        <!--  -->
                        <div class="title-text">
                            <p>{{ item.title }}</p>
                        </div>

                        <br />
                    </div>
                </span>
            </div>
        </div>
        <div class="right-content">
            <div class="top-rank">
                <h2 class="title">UPCOMING</h2>
                <div style="display: flex" v-for="item in upcomingList" :key="item.id" @click="toDetail(item.id)"
                    class="handClickRow">
                    <div>
                        <span style="color: blue">{{ item.title }}</span><br>
                        <span style="color: red">release at {{ item.release_date }}</span><br>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import rankstar from '@/components/rankstar/rankstar.vue'
// 引入axios
import axios from 'axios'
import { ref } from 'vue'

import { useStore } from 'vuex'
// 引入路由
import { useRouter } from 'vue-router'


/**
 * 首页页面组件
 */
export default {
    // 定义静态方法
    asyncData({ store }) {
        return store.dispatch('getHomeMovieData')
    },
    name: 'home',// 组件的名称，尽量和文件名一致
    components: {
        rankstar,
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        // 从store获取数据
        // let nowplayList = computed(() => store.state.nowplayList)
        // let upcomingList = computed(() => store.state.upcomingList)
        // let rankList = computed(() => store.state.rankList)
        let nowplayList = ref([])
        let nowplayList2 = ref([])
        let upcomingList = ref([])
        let upcomingList2 = ref([])
        let rankList = ref([])
        let rankList2 = ref([])

        function getNowplayList() {
            axios.get('https://api.themoviedb.org/3/movie/now_playing?api_key=2582b42403a1b46e0d8e848924f5dce3').then(res => {
                // console.log(res.data.results)
                nowplayList.value = res.data.results
                //     截取前4个
                nowplayList.value = nowplayList.value.slice(0, 4)
                //    截取第5个到第8个
                nowplayList2.value = res.data.results.slice(4, 8)

            }).catch(err => {
                console.log(err)
            })
        }

        function getupcomingList() {
            axios.get('https://api.themoviedb.org/3/movie/upcoming?api_key=2582b42403a1b46e0d8e848924f5dce3').then(res => {
                upcomingList.value = res.data.results
                //     截取前4个
                upcomingList.value = upcomingList.value.slice(0, 16)
                upcomingList2.value = res.data.results.slice(4, 8)
            }).catch(err => {
                console.log(err)
            })
        }

        function getRankList() {
            axios.get('https://api.themoviedb.org/3/movie/top_rated?api_key=2582b42403a1b46e0d8e848924f5dce3').then(res => {
                rankList.value = res.data.results
                //     截取前4个
                rankList.value = rankList.value.slice(0, 4)
                rankList2.value = res.data.results.slice(4, 8)
            }).catch(err => {
                console.log(err)
            })
        }

        function toDetail(id) {
            console.log(id)
            router.push('/detail?id=' + id)
        }

        getNowplayList()
        getupcomingList()
        getRankList()
        return {
            nowplayList,
            nowplayList2,
            upcomingList,
            upcomingList2,
            rankList,
            rankList2,
            getNowplayList,
            getupcomingList,
            getRankList,
            toDetail,
            router
        }
    }
}
</script>
<style scoped lang="less">
.home-container {
    display: flex;
    background-color: rgba(255, 255, 255, 0.8);
    font-family: Arial, sans-serif;
    /* 设置内容区域半透明白色背景色 */
}

.left-content {
    display: flex;
    flex-direction: column;
    width: 705px;
}

.right-content {
    display: flex;
    width: 300px;
    margin-left: 20px;
}

.title {
    margin-left: 16%;
    margin-top: 50px;
    font-size: 25px;
    font-weight: 500;
    color: #111;
    padding-bottom: 10px;
    border-bottom: 1px solid #eaeaea;
    margin-bottom: 18px;
}

.play-section {
    display: flex;
    margin-left: 16%;
    margin-top: 15px;
    padding: 15px;
}

.recent-item {
    display: inline-block;
    width: 675px;
    white-space: normal;
}

.top-rank {
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

//设置图片大小

img {
    width: 120px;
    height: auto;
    background-size: cover;
}

.movie-img {
    margin-left: 5px;
    margin-right: 5px;
}

.vote-average {
    //    居中
    text-align: center;
    //color: deeppink;
}

.handClick {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    position: relative;
}

.handClick::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
    z-index: -1;
}

.handClick:hover::before,
.handClick:hover .title-text {
    opacity: 1;
    z-index: 1;
}

.title-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #fff;
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
    background: rgba(0, 0, 0, 0.7);
    padding: 5px 10px;
    border-radius: 3px;
}

.handClick:hover .title-text {
    opacity: 1;
}

.handClickRow {
    display: flex;
    flex-direction: row;
    cursor: pointer;
    margin-top: 10px;
}
</style>
