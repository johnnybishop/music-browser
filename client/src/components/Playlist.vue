<template>
    <div class="playlist" @click="onClick(playlist.id)">
        <h3>{{ playlist.title }}</h3>
        <p>{{ playlist.createdAt }} </p>
        <!-- <div style="display:flex; justify-content:space-between; border: none; border-radius: 4px"><button style="background-color: red">Delete</button></div> -->
    </div>
</template>


<script>
export default {
    name: 'Playlist',
    props: {
        playlist: Object
    },
    methods: {
        onClick(playlistId) {
            this.$emit('select-playlist', playlistId);
        }
    },
    emits: ['select-playlist']
}

</script>

<style scope>
.playlist {
    background: lightgray;
    margin: 5px 0;
    padding: 10px 20px;
    cursor: pointer;
}
/*  */
</style>