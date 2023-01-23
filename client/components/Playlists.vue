<template>
    <div :key="playlist.id" v-for="playlist in playlists">
        <Playlist @select-playlist="$emit('select-playlist', playlist.id)" :playlist="playlist" />
    </div>

</template>


<script>
import Playlist from './Playlist.vue';

export default {
    name: 'Playlists',
    props: {
        playlists: Array
    },
    components: {
        Playlist,
    },
    emits: ['select-playlist']
}

</script>