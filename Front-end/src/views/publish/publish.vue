<template>
  <div class="publish-container">
    <h1 class="page-title">Add a comment</h1>
    <div class="movie-info" v-if="movieData.title">
      <img class="info-img" :src="movieData.poster_path" />
      <div class="right-info">
        <div class="title">{{ movieData.title }}</div>
        <div class="desc">{{ movieData.vote_average }}Stars</div>
      </div>
    </div>
    <div class="score-add">
      <div>Rank it：</div>
      <div class="rankstar">
        <div :class="['star-item', item.state]" v-for="(item, index) in starlist.list || []" :key="index"
          @mouseenter="changeScore(index)"></div>
      </div>
    </div>
    <div class="text-input">
      <textarea id="commentInput" placeholder="Write your comment here~" v-model.trim="content"></textarea>
    </div>
    <div id="submitBtn" @click="submit">submit</div>
  </div>
</template>

<script>
import { reactive, ref, computed, onMounted } from 'vue'
import axios from 'axios'
import service from '@/utils/service'
import Vuex from 'vuex'
import moment from 'moment'
import { useRoute } from 'vue-router'
import configapi from '@/utils/configapi'
/**
 * 待办事项页面组件
 */
export default {
  name: 'publish',// 组件的名称，尽量和文件名一致
  components: {
  },
  setup() {
    const store = Vuex.useStore()
    const sendcomment = async (movieid, comment, rating) => {
      
      const userInfo = store.state.userInfo;
      if (!userInfo.id) return;
      try {
        const response = await axios.post("http://localhost:5050/user/" + userInfo.id + "/add_comment",
          { movie_id: movieid, comment_text: comment, rating: rating,username:userInfo.username});
        if (response.data) {
          console.log("comment sent:");
          console.log(response.data);
        }
      } catch (error) {
        console.error(error);
      }
    };
    let movieData = ref({})
    let content = ref('')
    let starlist = reactive({
      list: new Array(5).fill({ state: 'normal' })
    })

    const route = useRoute()
    let id = computed(() => route.query.id);
    onMounted(async () => {
      console.log(id.value)
      const geturl = `https://api.themoviedb.org/3/movie/${id.value}?api_key=2582b42403a1b46e0d8e848924f5dce3&language=en-US`;
      const response = await fetch(geturl);
      const responseData = await response.json();
      if (responseData) {
          movieData.value = responseData
          /**console.log(responseData)
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
          data.genres = responseData.genres.map(genre => genre.name).join(' / ');
          console.log(data.id)
          console.log(data.title)**/
          console.log(movieData.value)
      }
      //let data = await service.get(configapi.detail(id.value), {})
      //movieData.value = data
      //console.log(movieData.value)
    });

    const changeScore = (index) => {
      let list = []

      starlist.list.forEach((item, _index) => {
        if (_index <= index) {
          item.state = 'full'
        } else {
          item.state = 'normal'
        }
        list.push({ ...item })

      })
      starlist.list = list
    }


    return {
      movieData,
      starlist,
      content,
      changeScore,
      sendcomment
    }
  },
  computed: {
    userInfo() {
      return this.$store.state.userInfo
    }
  },
  methods: {
    submit() {
      let count = 0
      this.starlist.list.forEach((item) => {
        if (item.state == 'full') {
          count++
        }
      })
      this.sendcomment(this.movieData.id, this.content, count);
      this.$store.commit('setCommentList', {
        rating: {
          value: count
        },
        user: {
          avatar: this.userInfo.avatar,
          name: this.userInfo.name
        },
        create_time: moment().format('YYYY-MM-DD HH:mm:ss'),
        abstract: this.content
      })
      

      this.$router.push('/detail?id=' + this.movieData.id)
    }
  }
}
</script>
<style scoped lang="less">
.publish-container {
  background-color: rgba(255, 255, 255, 0.9);
  width: 705px;
  margin: 0 auto;
  padding: 22px;
}

.page-title {
  font-size: 14px;
  margin-top: 5px;
  color: #007722;
}

.movie-info {
  display: flex;
  width: 705px;
  height: 62px;
  margin: 0 auto;
  margin-top: 10px;
  background-color: #f8f8f8;
  overflow: hidden;
}

.info-img {
  width: 48px;
  height: 62px;
  margin-right: 15px;
}

.right-info {
  padding: 10px 40px 0 0;
  margin-bottom: 5px;

  .title {
    color: #37a;
    font-size: 14px;
    line-height: 1.4;
  }

  .desc {
    margin-top: 2px;
    color: #999;
  }
}

.rankstar {
  display: flex;
  align-items: center;
}

.star-item {
  width: 16px;
  height: 16px;
  background-size: cover;
  cursor: pointer;

  &.normal {
    background-image: url('./imgs/star.png');
  }

  &.full {
    background-image: url('./imgs/star-fill.png');
  }
}

.score-add {
  margin-top: 30px;
  display: flex;
}

.text-input {
  margin-top: 20px;
}

#commentInput {
  outline: none;
  border: none;
  border-top: 1px solid #ddd;
  white-space: pre-wrap;
  overflow-wrap: break-word;
  padding: 16px 10px;
  width: 88%;
  min-height: 400px;
  overflow: auto;
  font-size: 14px;
}

#submitBtn {
  padding: 0 20px;
  height: 40px;
  line-height: 40px;
  color: #fff;
  background-color: #3db04d;
  width: 28px;
  cursor: pointer;
}
</style>
