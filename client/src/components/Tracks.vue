<template>
        <div class="tracks-container">
            <div class="playlist-tracks">
                <dl>
                    <dt>Add tracks</dt>
                    <dd v-for="track in tracks">
                        <span @click="addTrack(track)">&#65291;</span> 
                           <span style="margin-left: 5px; font-weight: bolder"> {{ track.title }}</span>
                           <div style="margin-left: 20px" >
                            <span> {{ track.author }}</span>
                            
                        </div>
                        <div>
                            <span style="margin-left: 20px" >
                                <a v-bind:href="track.track_url" target="_blank">Listen on youtube</a>
                            </span>
                        </div>
                    </dd>
                </dl>
            </div>

            <div class="playlist-tracks">
                <dl>
                    <dt>Selected tracks</dt>
                    <dd v-for="selectedTrack in selectedTracks">
                        <span @click="removeTrack(selectedTrack)">&#10060;</span> 
                           <span style="margin-left: 5px; font-weight: bolder"> {{ selectedTrack.title }}</span>
                           <div style="margin-left: 20px" >
                            <span> {{ selectedTrack.author }}</span>
                            
                        </div>
                        <!-- <div>
                            <span style="margin-left: 20px" >
                                <a v-bind:href="selectedTrack.track_url" target="_blank">Listen on youtube</a>
                            </span>
                        </div> -->
                    </dd>
                </dl>
            </div>
        </div>

        <div class="load-tracks">
            <span @click="pageBack">&#8592;</span>&nbsp;
            <span>{{ page * 10 }} from {{ count }} tracks</span>
            &nbsp;<span @click="pageForward">&#8594;</span>
        </div>
</template>


<script>
export default {
    name: 'Tracks',
    data: () => ({
        tracks: [],
        selectedTracks: [],
        page: 1,
        count: 0,
    }),
    props: {
        state: Object,
        default: [],
    },
    emits: ['track-added', 'track-removed'],
    async created() {
        await this.fetchData();
        await this.getCount();
    },
    async mounted() {
        if (this.state) {
            this.selectedTracks = this.state.tracks;
        }
    },
    watch: {
        state(value) {
            this.selectedTracks = value.tracks;
        },
        page(value) {
            console.log(value);
        }
    },
    methods: {
        async fetchData() {
            const API_URL = `http://localhost:8080/api/tracks?page=${this.page}`;
            await fetch(API_URL)
                .then((response) => response.json())
                .then((data) => {
                    this.tracks = data;
                });
        },
        async getCount() {
            const API_URL = `http://localhost:8080/api/tracks/count`;
            await fetch(API_URL)
                .then((response) => response.json())
                .then((data) => {
                    this.count = data;
                });
        },
        async addTrack(track) { 
            if (!this.selectedTracks.find((selectedTrack) => selectedTrack.id === track.id)) {
                this.selectedTracks.push(track);
                this.$emit('track-added', track.id);
            }
        },
        async removeTrack(track) {
            const filtered = this.selectedTracks.filter((selectedTrack) => selectedTrack.id !== track.id);
            this.selectedTracks = filtered;
            this.$emit('track-removed', track.id);
        },
        async pageForward() {
            if (this.page < this.count / 10) {
                this.page++;
                this.fetchData();
            }
        },
        async pageBack() {
            if (this.page > 1) {
                this.page--;
                this.fetchData();
            }
        }
    }
}
</script>

<style scoped>

.playlist-tracks {
    width: 50%;
}

.tracks-container {
    display: flex;
    flex-direction: row;
}
</style>