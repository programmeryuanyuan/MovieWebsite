<template>
    <div class="movie-cards">
        <div v-for="movie in movies" :key="movie.id" class="movie-card" @click="toDetail(movie.id)">
            <img :src="getImageUrl(movie)" :alt="movie.title" />
            <p class="simMovieTitle">{{ movie.title }}</p>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import rankstar from '@/components/rankstar/rankstar.vue';

export default {
    name: 'sim',
    components: {
        rankstar,
    },
    setup() {
        const route = useRoute();
        const router = useRouter();
        const movies = ref([]);
        const apiKey = '2582b42403a1b46e0d8e848924f5dce3';
        const movieId = computed(() => route.query.id);

        const getImageUrl = (movie) => `https://image.tmdb.org/t/p/w300${movie.poster_path}`;

        const fetchMovies = async () => {
            try {
                const response = await axios.get(`https://api.themoviedb.org/3/movie/${movieId.value}/recommendations?api_key=${apiKey}`);
                movies.value = response.data.results;
            } catch (error) {
                console.error(error);
            }
        };

        const toDetail = (id) => {
            router.push(`/detail?id=${id}`).then(() => {
                location.reload();
            });
        };


        onMounted(() => {
            fetchMovies();
        });

        return {
            movies,
            getImageUrl,
            toDetail,
        };
    },
};
</script>
  
<style>
.movie-cards {
    display: flex;
    flex-wrap: wrap;
}

.movie-card {
    margin: 10px;
    width: 100px;
    cursor: pointer;
}

.movie-card img {
    width: 100%;
    height: auto;
}

.simMovieTitle {
    text-align: center;
    font-size: 12px;
    color: #002;
}
</style>
  