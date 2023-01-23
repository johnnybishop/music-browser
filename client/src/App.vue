<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <div class="browser">

    <div v-if="searchVisible" class="card-container">
      <Header />
      <form v-on:submit.prevent="fetchData">

        <div class="search-container">
          <input type="text" v-model="query" placeholder="Search playlist..." />
          <button class="btn" type="submit">Search</button>
          <button class="btn add-button" type="button" @click="addVisible = true">Add playlist</button>
        </div>
      </form>
      <Playlists @select-playlist="setSelectedPlaylist" :playlists="playlists" />
    </div>

    <div v-if="selectedPlaylist" class="card-container">
      <Preview :playlistId="selectedPlaylist.id" @close-preview="setSelectedPlaylist" @edit-completed="fetchData"/>
    </div>

    <div v-if="addVisible" class="card-container">
      <AddPlaylist @close-add="addVisible = false" @playlist-added="fetchData" />
    </div>

  </div>

</template>

<script>
import Header from './components/Header.vue';
import Playlists from './components/Playlists.vue';
import Preview from './components/Preview.vue';
import AddPlaylist from './components/AddPlaylist.vue'

export default {

  name: 'App',
  components: {
    Header,
    Playlists,
    Preview,
    AddPlaylist
  },
  data: () => ({
    query: null,
    selectedPlaylist: null,
    playlists: null,
    searchVisible: true,
    addVisible: false,
  }),
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      const API_URL = 'http://localhost:8080/api/playlists';
      await fetch(API_URL)
        .then((response) => response.json())
        .then((data) => {
          if (this.query && this.query.length > 0) {
            this.playlists = data.responseData.filter((playlist) => playlist.title.includes(this.query));

            return;
          }

          this.playlists = data;
        });
    },
    setSelectedPlaylist(playlistId) {
      this.selectedPlaylist = this.playlists.slice().find((playlist) => playlist.id === playlistId);
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Poppins', sans-serif;
}

.browser {
  display: flex;
  justify-content: center;
  width: 100%;
}

.card-container {
  width: 50%;
  margin: 30px;
  overflow: auto;
  min-height: 300px;
  border: 1px solid steelblue;
  padding: 30px;
  border-radius: 5px;
}

.btn {
  display: inline-block;
  background: #000;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 15px;
  font-family: inherit;
}

.btn:focus {
  outline: none;
}

.btn:active {
  transform: scale(0.98);
}

.btn-block {
  display: block;
  width: 100%;
}

input {
  width: 70%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}

.search-container {
  display: flex;
  justify-content: space-between;
}

.add-button-container {
  display: flex;
  justify-content: flex-start;
}

.add-button {
  background-color: green;
  color: black;
}
</style>
