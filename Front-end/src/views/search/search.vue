<template>
  <div class="search-container">
    <div>
      <h5>Search History: </h5> <a style="font-size: small;" @click="clearLocalStorage">clear</a>
      <ul class="history">
        <li v-for="item in searchHistoryList" :key="item">
          <router-link :to="'/search?searchText=' + item"><a>{{ item }}</a></router-link>
        </li>
      </ul>
    </div>
    <h1 class="page-title">Search by {{ $route.query.searchText }}</h1>
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
              style="color: deeppink">release at {{ item.release_date }}</span> / <span style="color: red">popularity: {{
                item.popularity }}</span></div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import moment from 'moment'
import rankstar from '@/components/rankstar/rankstar.vue'
/**
 * 待办事项页面组件
 */
export default {
  name: 'search',// 组件的名称，尽量和文件名一致
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
    const route = useRoute()
    const searchHistoryList = ref(JSON.parse(localStorage.getItem('searchHistory')) || [])

    const addSearchHistory = (text) => {
      const index = searchHistoryList.value.indexOf(text)
      if (index !== -1) {
        searchHistoryList.value.splice(index, 1)
      }
      searchHistoryList.value.unshift(text)
      if (searchHistoryList.value.length > 8) {
        searchHistoryList.value.pop()
      }
      localStorage.setItem('searchHistory', JSON.stringify(searchHistoryList.value))
    }

    let searchText = computed(() => route.query.searchText);

    watch(
      () => route.query.searchText,
      async (inner) => {
        const page = 1;
        const searchurl = `https://api.themoviedb.org/3/search/multi?api_key=2582b42403a1b46e0d8e848924f5dce3&language=en-US&query=${inner}&page=${page}&include_adult=false`;
        const response = await fetch(searchurl);
        const data2 = await response.json();
        const searchlist2 = data2.results.filter(item => item.media_type === 'movie');
        const personlist = data2.results.filter(item => item.media_type === 'person');
        const searchlist3 = personlist.flatMap(item => item.known_for);
        searchList0.list = searchlist2.concat(searchlist3).sort((a, b) => b.popularity - a.popularity)
        addSearchHistory(inner)
      },
      {
        deep: false,
        immediate: true
      }
    )
    onMounted(async () => {
    })
    return {
      searchList0,
      searchHistoryList
    }
  },
  computed: {

  },
  methods: {
    clearLocalStorage() {
      localStorage.removeItem('searchHistory');
    }
  }
}
</script>
<style scoped lang="less">
.search-container {
  background-color: rgba(255, 255, 255, 0.8);
  // width: 790px;
  margin: 0 auto;
}

.history {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  padding: 0;
  margin: 0;
}

.history li {
  display: inline-block;
  margin-right: 10px;
  margin-bottom: 10px;
  padding: 6px 12px;
  border-radius: 4px;
  background-color: #f0f0f0;
}

.history li a {
  color: #333;
  text-decoration: none;
  font-weight: bold;
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
