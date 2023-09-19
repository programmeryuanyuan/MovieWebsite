<template>
  <div class="movie-actors" v-if="detailData.list.length">
    <h2 class="intro-title">
      Actors
    </h2>
    <div class="scroll-wrap">
      <div class="scroll-content">
        <div class="actor-item" v-for="item in detailData2.list" :key="item.cast_id">
          <router-link :to="'/credit?id=' + item.cast_id" class="title">
            <img class="actor-img" :src="'https://image.tmdb.org/t/p/w500/' + item.profile_path" />
          </router-link>
          <div class="actor-name one-line">{{ item.name }}</div>
          <div class="actor-character one-line">{{ item.character }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, reactive } from 'vue'
import service from '@/utils/service'
import configapi from '@/utils/configapi'
import Vuex from 'vuex'
import { useRoute } from 'vue-router'
/**
 * 待办事项页面组件
 */
export default {
  name: 'movieactors',
  components: {},
  setup() {
    const store = Vuex.useStore();
    const route = useRoute();
    const detailData = reactive({
      list: [],
    });
    const detailData2 = reactive({
      list: [],
    });
    const id = computed(() => route.query.id);

    onMounted(async () => {
      try {
        const response1 = await fetch(
          `https://api.themoviedb.org/3/movie/${id.value}/credits?api_key=2582b42403a1b46e0d8e848924f5dce3`
        );
        if (!response1.ok) {
          throw new Error('Failed to fetch movie details');
        }
        const detailDataData = await response1.json();
        const cast = detailDataData.cast;
        const crew = detailDataData.crew.filter(obj => obj.known_for_department === 'Directing');
        detailData2.list = cast.filter(item => item.profile_path !== null);
        console.log(detailData2);

        const data = await service.get(configapi.actors(id.value));
        detailData.list = data.directors.concat(data.actors);
        console.log(detailData);
      } catch (error) {
        console.error(error);
      }
    });

    return {
      detailData,
      detailData2
    };
  },
};

</script>
<style scoped lang="less">
.intro-title {
  margin: 24px 0 12px 0;
  font-size: 16px;
  color: #007722;
}

.actor-item {
  display: inline-block;
  margin-right: 20px;
}

.scroll-wrap {
  overflow-x: auto;
  overflow-y: hidden;
}

.scroll-content {
  display: inline-block;
  white-space: nowrap;
}

.actor-name {
  width: 90px;
  color: #111;
  font-size: 13px;
  text-align: center;
}

.actor-character {
  color: #9b9b9b;
  font-size: 13px;
  text-align: center;
  width: 94px;
}

.actor-img {
  width: 95px;
  height: 133px;
  object-fit: cover;
  background-color: #ccc;
}

::-webkit-scrollbar-track {
  background: #f6f6f6;
  border-radius: 2px;
}

::-webkit-scrollbar-thumb {
  background: #cdcdcd;
  border-radius: 2px;
}

::-webkit-scrollbar-corner {
  background: #f6f6f6;
}

::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}
</style>
