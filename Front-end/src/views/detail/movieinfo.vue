<template>
  <div class="movie-info" v-if="detailData.id">
    <h1 class="title">{{ detailData.title }} <span class="year">({{
      detailData.release_date
    }})</span>
      <button class="btn-info btn" @click="collect">Wishlist</button>
      <button class="btn-danger btn" @click="collect2">Favorite</button>
    </h1>
    <div class="desc-content">
      <img class="mv-img" :src="'https://image.tmdb.org/t/p/w500/' + detailData.poster_path" />
      <div class="mv-desc">
        <p>Genres:
          <router-link :to="'/genres?id=' + detailData.genres.map(item => item.id).join('%2C')">
            <span class="it">{{ detailData.genres.map(item => item.name).join('/') }}</span>
          </router-link>
        </p>
        <p>Director: <a href="#" v-if="detailData4 && detailData4.length">
            {{ detailData4[0].name }}({{ detailData4.length }})</a></p>
        <p>Actors: <a href="#" v-for="(item, index) in actors.short" :key="index">{{ item.name }}
            <template v-if="index != actors.short.length - 1">/
            </template>
          </a><span @click="expand" class="more-actors" v-if="actors.isShowMore">More..</span></p>
        <p>Company: <span class="it">{{ detailData.production_companies.map(item => item.name).join('/') }}</span></p>
        <p>Country: <span class="it">{{ detailData.production_countries.map(item => item.name).join('/') }}</span></p>
        <p>Languages: <span class="it">{{ detailData.spoken_languages.map(item => item.name).join('/') }}</span></p>
        <p>Budget: <span class="it">{{ detailData.budget > 0 ? (detailData.budget / 10000).toFixed(2) + ' million USD' :
          'unknown' }}</span></p>
        <p>Revenue: <span class="it">{{ detailData.revenue > 0 ? (detailData.revenue / 10000).toFixed(2) + ' million USD'
          : 'unknown' }}</span></p>

        <p>Runtime: <span class="it">{{ detailData.runtime }}min</span></p>
        <a :href="'https://www.imdb.com/title/' + detailData.imdb_id" target="_blank">Link to IMDB.com</a>
        <!-- <p>Special name: <span class="it">{{ detailData.aka.join('/') }}</span></p> -->
      </div>
      <div class="mv-rank">
        <div class="rank-title">Fun Stars</div>
        <div class="rank-score">
          <div class="score"><strong class="num">{{ detailData.vote_average }}</strong></div>
          <div class="score-star">
            <rankstar :score="detailData.vote_average" class="rankstar" />
            <div class="score-comment"><a href="#">{{ detailData.vote_count }}</a>Rated</div>
          </div>
        </div>
      </div>
    </div>
    <div class="opera-box">
      <div>:</div>
      <div>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil"
          viewBox="0 0 16 16">
          <path
            d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z" />
        </svg>&nbsp
        <a href="javascript:void(0)" class="comment-link" @click="goPublish">Add a comment</a>
      </div>
    </div>
    <div class="intro">
      <h2 class="intro-title">
        Overview
      </h2>
      <div style="text-indent:20px;">
        {{ detailData.overview }}
      </div>

      <div class="collect">
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive, computed } from 'vue'
import service from '@/utils/service'
import rankstar from '@/components/rankstar/rankstar.vue'
import configapi from '@/utils/configapi'
import Vuex from 'vuex'
import { useStore } from 'vuex';
import { useRoute } from 'vue-router'
import axios from "axios";

/**
 * 待办事项页面组件
 */
export default {
  name: 'movieinfo',// 组件的名称，尽量和文件名一致
  components: {
    rankstar
  },
  setup() {
    const store = useStore()
    const addtowishlist = async (movieid,movietitle) => {
            const userInfo = store.state.userInfo;
            if (!userInfo.id) return;
            try {
                const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/wishlist", 
                {movie_id:movieid,movie_title:movietitle,});
                if (response.data) {
                    console.log("add to wishlist:");
                    alert(response.data.message);
                }
            } catch (error) {
                console.error(error);
                alert(error);
            }
    };
    const setFavoriteMovie = async (movieId) => {
        const userInfo = store.state.userInfo;
        if (!userInfo.id) return;
        console.log(movieId)
        try {
            const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/set_favorite_movie",
            { movie_id: movieId });
            
            if (response.data) {
                alert("set favorite movie successfully");
                
            }
        } catch (error) {
            console.error(error);
        }
    };
    let detailData = ref({})
    let detailData3 = ref({})
    let detailData4 = ref({})
    let actors = reactive({
      orgin: [],
      short: [],
      isShowMore: true
    })
    const route = useRoute()
    let id = computed(() => route.query.id);
    onMounted(async () => {
      try {
        const response1 = await fetch(`https://api.themoviedb.org/3/movie/${id.value}?api_key=2582b42403a1b46e0d8e848924f5dce3`);
        if (!response1.ok) {
          throw new Error('Failed to fetch movie details');
        }
        const detailDataData = await response1.json();
        detailData.value = detailDataData;

        const response2 = await fetch(`https://api.themoviedb.org/3/movie/${id.value}/credits?api_key=2582b42403a1b46e0d8e848924f5dce3`);
        if (!response2.ok) {
          throw new Error('Failed to fetch movie credits');
        }
        const detailData3Data = await response2.json();
        detailData3.value = detailData3Data.cast;
        detailData4.value = detailData3Data.crew.filter(obj => obj.known_for_department === 'Directing');

        store.commit('setTitle', detailData.value.title);
        actors.orgin = detailData3.value || [];
        actors.short = actors.orgin.slice(0, 3);
        actors.isShowMore = actors.orgin.length > 3;
      } catch (error) {
        console.error(error);
      }
    });


    const expand = () => {
      actors.short = actors.orgin
      actors.isShowMore = false
    }


    return {
      detailData,
      detailData,
      detailData4,
      actors,
      expand,
      addtowishlist,
      setFavoriteMovie,
    }
  },
  computed: {
        userinfo() {
            return this.$store.state.userInfo;
        },


    },
  methods: {
    goPublish() {
      if (this.$store.state.userInfo.username) {
        this.$router.push('/publish?id=' + this.detailData.id)
      } else {
        this.$router.push('/login')
      }
    },
    collect() {
      const movieId = this.detailData.id;
      const movieTitle = this.detailData.title;
      this.addtowishlist(movieId, movieTitle);
    
  },
  collect2(){
    const movieId = this.detailData.id;
    let user0 = JSON.parse(localStorage.getItem("user"));
    user0.favorite_movie = movieId;
    localStorage.setItem("user", JSON.stringify(user0));
    this.setFavoriteMovie(movieId);
  }
}
}
</script>
<style scoped lang="less">
.title {
  font-size: 26px;
  font-weight: bold;
  color: #494949;

  .year {
    color: #888;
  }
}

.desc-content {
  display: flex;
  margin-top: 13px;
}

.mv-img {
  width: 135px;
  height: 200px;
}

.mv-desc {
  font-size: 13px;
  margin-left: 15px;
  max-width: 600px;
  margin-right: 15px;

  p {
    margin: 2px 0;
    color: #666;

    .it {
      color: #111;
    }
  }
}

.more-actors {
  color: #aaa;
  cursor: pointer;

  &:hover {
    color: #fff;
    background: #aaa;
  }
}

.mv-rank {
  width: 155px;
  margin: 15px 0 0 0;
  padding: 0 0 0 15px;
  border-left: 1px solid #eaeaea;
  color: #9b9b9b;

}

.rank-score {
  margin-top: 5px;
  display: flex;

  .num {
    color: #494949;
    padding: 0;
    font-size: 28px;
  }
}

.score-star {
  margin-left: 10px;
  padding-top: 5px;

  .rankstar {
    transform: scale(1.3);
    transform-origin: 0 0;
  }
}

.score-comment {
  margin-top: 7px;
}

.wline {
  height: 10px;
  margin: 1px 4px;
  background-color: #ffd596;
  falign-self: center;
}

.better-content {
  position: relative;
  padding: 15px 0;
  border-top: 1px solid #eaeaea;
  color: #9b9b9b;
  margin-top: 20px;
}

.better-item {
  margin-top: 1px;
}

.intro-title {
  margin: 24px 0 12px 0;
  font-size: 16px;
  color: #007722;
}

.comment-link {
  font-size: 13px;
}
</style>
