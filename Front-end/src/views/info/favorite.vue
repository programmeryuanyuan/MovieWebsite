<template>
    <div v-if="data.title == null">NO FAVORITE MOVIE</div>
    <div class="item-content" v-else>
        <div class="right-content">
            <img :src="'https://image.tmdb.org/t/p/w500/' + data.poster_path" class="item-img" />
            <div class="rank-content">
                <rankstar :score="data.vote_average" class="rank-star"></rankstar>
                <div class="score-text">{{ data.vote_average }}</div>
            </div>
        </div>
        <div class="left-content">
            <router-link :to="'/detail?id=' + data.id" class="title">{{ data.title }}</router-link>
            <div class="overview">{{ data.genres }}</div>
            <div class="place">{{ data.tagline }}</div>
        </div>
    </div>
</template>

<script>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import moment from 'moment'
import { useStore } from 'vuex'
import { watchEffect } from 'vue';
import rankstar from '@/components/rankstar/rankstar.vue'
export default {
    name: 'favorite',
    components: {
        rankstar
    },
    setup() {
        const store = useStore();
        const userinfo = computed(() => store.state.userInfo);
        onMounted(async () => {
            const user = JSON.parse(localStorage.getItem('user'))
            if (user) {
                store.commit('setUser', user)
            }
            await getfavoritemovie();
        })
        

        const data = reactive({
            poster_path: '',
            vote_average: '',
            id: '',
            title: null,
            overview: '',
            genres: '',
            original_language: '',
            release_date: '',
            popularity: '',
            tagline: ''
        });
        const getfavoritemovie=async()=>{
            const userInfo = store.state.userInfo;
            if (!userInfo.favorite_movie) return;
            try {
                //const response = await axios.get("http://localhost:5050/user/" + userInfo.id + "/wishlist",config);
                //const geturl = `https://api.themoviedb.org/3/movie/${userInfo.favorite_movie}?api_key=2582b42403a1b46e0d8e848924f5dce3&language=en-US`;
                const geturl = `https://api.themoviedb.org/3/movie/${userInfo.favorite_movie}?api_key=2582b42403a1b46e0d8e848924f5dce3&language=en-US`;
                const response = await fetch(geturl);
                const responseData = await response.json(); 
                if (responseData.poster_path) {
                    console.log(responseData)
                    data.poster_path = responseData.poster_path;
                    data.vote_average = responseData.vote_average;
                    data.id = responseData.id;
                    data.title = responseData.title;
                    data.overview = responseData.overview;
                    data.original_language = responseData.original_language;
                    data.release_date = moment(responseData.release_date).format('LL');
                    data.popularity = responseData.popularity;
                    data.tagline = responseData.tagline;
                    // data.genres = response.genres.map(genre => genre.name).join('/');
                    //data.genres = responseData.genres.map(genre => genre.name).join(' / ');
                    console.log(data.id)
                    console.log(data.title)
                    //data=responseData
                }
            } catch (error) {
                console.error(error);
            }
        };
        
        watch(() => store.state.userInfo, () => {
            getfavoritemovie();
        });

        return {
            data
            
            
        }
    },


    computed: {
    },
    methods: {
    }
}
</script>

<style scoped lang="less">
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
    position: relative;

    &:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    &::before {
        content: "";
        position: absolute;
        top: 5%;
        right: 3%;
        width: 20px;
        height: 20px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' t='1681980447233' class='icon' viewBox='0 0 1024 1024' version='1.1' width='200' height='200'%3E%3Cpath d='M512 950.784c-17.92 0-35.84-6.144-50.176-18.432L130.56 645.12c-0.512-0.512-1.024-1.024-1.536-1.024C65.536 580.096 0 500.736 0 394.24c0-169.472 137.728-307.2 307.2-307.2 76.8 0 148.48 27.648 204.8 78.336 56.32-50.688 128-78.336 204.8-78.336 169.472 0 307.2 137.728 307.2 307.2 0 111.104-66.56 187.392-129.024 249.856-0.512 0.512-1.024 1.024-1.536 1.024l-331.264 287.232c-14.336 12.288-32.256 18.432-50.176 18.432z m364.544-324.608z' fill='%23FF2B2B'%3E%3C/path%3E%3Cpath d='M801.28 509.952c-7.68 0-14.848-3.584-19.968-9.728-8.704-11.264-6.656-27.136 4.096-35.84 24.576-19.456 38.912-48.64 38.912-80.384 0-56.32-46.08-102.4-102.4-102.4H718.848c-14.336 0.512-26.112-10.752-26.624-24.576-0.512-14.336 10.752-26.112 24.576-26.624H721.408c84.48 0 153.6 69.12 153.6 153.6 0 47.104-21.504 91.136-58.368 120.832-4.608 3.584-9.728 5.12-15.36 5.12z' fill='%23FFFFFF'%3E%3C/path%3E%3C/svg%3E");
        background-size: cover;
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
        justify-content: center;
        /* 垂直居中 */
        align-items: center;
        /* 水平居中 */
        height: 150px;
        flex: 1;
    }

    .right-content {
        display: flex;
        flex-direction: column;
    }

    .overview {
        color: #666;
        font-size: 14px;
        margin-top: 0px;
        text-align: center;
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
        font-size: 18px;
        margin-top: 10px;
        text-align: center;
        background: linear-gradient(to right, rgb(0, 255, 51), rgb(0, 255, 191), rgb(0, 174, 255), rgb(0, 28, 128), rgb(76, 0, 255), purple);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
}
</style>