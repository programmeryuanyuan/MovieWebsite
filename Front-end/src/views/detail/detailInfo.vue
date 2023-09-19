<template>
    <div className="detail-container">
        <div className="left-content">
            <!--            电影详情-->
            <h1 className="title">Movie Details</h1>
            <hr />
            <img :src="'https://image.tmdb.org/t/p/w500/' + movieInfo.poster_path" />

            <h2 className="title">title:{{ movieInfo.title }}</h2>
            <h2 className="title">budget:{{ movieInfo.budget }}</h2>
            <h2 className="title">overview:{{ movieInfo.overview }}</h2>
            <h2 className="title">popularity:{{ movieInfo.popularity }}</h2>
        </div>
        <div className="right-content">
            <div className="similar-movies">
                <h2 className="title">similar movies</h2>
                <div className="form-check">
                    <input className="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
                    <label className="form-check-label" htmlFor="flexRadioDefault1">
                        Base on genre
                    </label>
                </div>
                <div className="form-check">
                    <input className="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                    <label className="form-check-label" htmlFor="flexRadioDefault2">
                        Base on director
                    </label>
                </div>
                <div id="simMovies">
                    <ul>
                        <li>
                            <div className="testS">movie1</div>
                        </li>
                        <li>
                            <div className="testS">movie2</div>
                        </li>
                        <li>
                            <div className="testS">movie3</div>
                        </li>
                        <li>
                            <div className="testS">movie4</div>
                        </li>
                        <li>
                            <div className="testS">movie5</div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import {ref,onMounted,toRaw, reactive} from 'vue'
import service from '@/utils/service'
import movieinfo from './movieinfo.vue'
import movieactors from './movieactors.vue'
import moviecomments from './moviecomments.vue'
// 引入路由
import { useRoute } from 'vue-router'
import Vuex from 'vuex'
import { reactive, ref } from "vue";
import axios from "axios";

/**
 * 待办事项页面组件
 */
export default {
    name: 'detail',// 组件的名称，尽量和文件名一致
    components: {
        movieinfo,
        movieactors,
        moviecomments
    },
    setup() {
        const route = useRoute()
        const movieId = route.params.id
        console.log(movieId)
        // 发送请求 得到电影详情
        const movieInfo = reactive({
            title: '',
            budget: '',
            overview: '',
            popularity: '',
            poster_path: '',
        })

        function getMovieInfo() {
            axios.get('https://api.themoviedb.org/3/movie/' + movieId + '?api_key=2582b42403a1b46e0d8e848924f5dce3').then(res => {
                console.log(res)
                movieInfo.title = res.data.title
                movieInfo.budget = res.data.budget
                movieInfo.overview = res.data.overview
                movieInfo.popularity = res.data.popularity
                movieInfo.poster_path = res.data.poster_path
            }).catch(err => {
                console.log(err)
            })
        }

        getMovieInfo()
        return {
            movieId,
            movieInfo,

        }
    }
}
</script>
<style scoped lang="less">
.detail-container {
    display: flex;
    background-color: rgba(255, 255, 255, 0.8);
    /* 设置内容区域半透明白色背景色 */
}

.left-content {
    display: flex;
    flex-direction: column;
    width: 705px;
    margin-top: 40px;
    padding: 15px;
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

.testS {
    font-size: 20px;
    width: 80%;
    background-color: rgb(230, 230, 230);
    align-items: center;
    color: #111;
    padding-bottom: 10px;
    border: 1px solid #eaeaea;
    margin-bottom: 18px;
}

#simMovies {
    font-size: 20px;
}
</style>
