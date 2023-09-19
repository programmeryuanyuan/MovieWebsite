<template>
  <div class="detail-container">
    <div class="left-content">
      <movieinfo />
      <movieactors />
      <moviecomments />
    </div>
    <div class="right-content">
      <div class="similar-movies">
        <h2 class="title" style="margin-top: 50px;">Similar</h2>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" value="intelligent"
            v-model="selected">
          <label class="form-check-label" for="flexRadioDefault1">
            Intelligent Recommendation
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" value="director"
            v-model="selected" checked>
          <label class="form-check-label" for="flexRadioDefault2">
            Similar movies
          </label>
        </div>
        <div id="simMovies">
          <ul>
            <sim v-if="selected === 'intelligent'" />
            <sim2 v-else-if="selected === 'director'" />
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import movieinfo from './movieinfo.vue'
import movieactors from './movieactors.vue'
import moviecomments from './moviecomments.vue'
import sim from './sim.vue'
import sim2 from './sim2.vue'

export default {
  name: 'detail',
  components: {
    movieinfo,
    movieactors,
    moviecomments,
    sim,
    sim2,
  },
  data() {
    return {
      selected: 'director',
    }
  },
}
</script>

<style scoped lang="less">
.detail-container {
  display: flex;
  background-color: rgba(255, 255, 255, 0.8);
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
