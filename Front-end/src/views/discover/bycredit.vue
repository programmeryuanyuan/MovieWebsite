<template>
    <div class="search-container">
        <h1 class="page-title">Movies of credit</h1>
        <div class="search-result">
            <div v-if="searchList0.list.length == 0">No data</div>
            <div class="item-content" v-for="item in searchList0.list">
                <div class="right-content">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + item.poster_path" class="item-img" />
                    <div class="rank-content">
                        <rankstar :score="item.vote_average" class="rank-star"></rankstar>
                        <div class="score-text">{{ item.vote_average }}</div>
                    </div>
                </div>
                <div class="left-content">
                    <router-link :to="'/detail?id=' + item.id" class="title">{{ item.title }}</router-link>
                    <div class="overview">{{ item.overview }}</div>
                    <div class="place"><span style="color: grey">language: {{ item.original_language }} </span> / <span
                            style="color: deeppink">release at {{ item.release_date }}</span> / <span
                            style="color: red">popularity: {{
                                item.popularity }}</span></div>
                </div>
            </div>
        </div>

    </div>
</template>
  
<script>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import rankstar from '@/components/rankstar/rankstar.vue'
/**
 * 待办事项页面组件
 */
export default {
    name: 'bycredit',// 组件的名称，尽量和文件名一致
    components: {
        rankstar
    },
    setup() {

        let movieData = ref({})
        let content = ref('')
        let searchList = reactive({
            list: []
        })
        let searchList0 = reactive({
            list: []
        })

        const fetchData = async () => {
            const route = useRoute()
            const id = route.query.id
            const apiKey = '2582b42403a1b46e0d8e848924f5dce3'
            const searchurl = `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_people=${id}&with_watch_monetization_types=flatrate`;
            const response = await fetch(searchurl);
            console.log(response)
            const data2 = await response.json();
            console.log(data2)
            searchList0.list = data2.results.sort((a, b) => b.vote_average - a.vote_average || a.title.localeCompare(b.title));
            console.log(searchList0)
        }

        onMounted(async () => {
            fetchData();
        })
        return {
            searchList0,
        }
    },
    computed: {

    },
    methods: {

    }
}
</script>
<style scoped lang="less">
.search-container {
    background-color: rgba(255, 255, 255, 0.8);
    // width: 790px;
    margin: 0 auto;
}

.page-title {
    font-size: 32px;
    font-weight: bold;
    padding: 20px 0;
    background-color: rgba(255, 255, 250, 0.2);
    border-bottom: 1px solid #ccc;
}

.item-content {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 10px;
    background-color: rgba(255, 255, 250, 0.2);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    transition: box-shadow 0.3s ease-in-out;
    margin: 10px;

    &:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .item-img {
        width: 100px;
        height: 150px;
        object-fit: cover;
        border-radius: 4px 0 0 4px;
    }

    .left-content {
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 150px;
        flex: 1;
    }

    .right-content {
        display: flex;
        flex-direction: column;
    }

    .overview {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .title {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
        text-align: center;
        text-decoration: none;
        transition: color 0.3s ease-in-out;

        &:hover {
            color: deeppink;
        }
    }


    .rank-content {
        display: flex;
        align-items: center;
    }

    .score-text {
        color: #e09015;
        font-weight: bold;
        margin-left: 5px;
    }

    .place {
        color: #666;
        font-size: 14px;
        margin-top: 10px;
        text-align: center;
    }
}
</style>
  