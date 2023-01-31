<template>
    <div class="preview-header">
        <div class="playlist-title">
            <h1>Edit playlist</h1>
        </div>
        <span @click="$emit('close-edit', null)">&#10060;</span>
    </div>

    <div v-if="validationErrors.length" class="errors-container">
        <div v-for="error in validationErrors">
            {{ error }}
        </div>
    </div>
    <form v-on:submit.prevent="savePlaylist">
        <input type="text" v-model="playlist.name" placeholder="Insert playlist name..." />
        <input type="text" v-model="playlist.description" placeholder="Insert playlist description..." />
        <!-- <Tracks :state="playlist" @track-added="addTrack" @track-removed="removeTrack" /> -->
        <div class="button-container">
            <button class="btn" type="submit">Save</button>
        </div>
    </form>

</template>


<script>
import Tracks from './Tracks.vue';

export default {
    name: 'EditPlaylist',
    components: {
        Tracks
    },
    props: {
        playlist: Object,
    },
    data: () => ({
        name: null,
        description: null,
        validationErrors: [],
        tracksId: [],
    }),
    mounted () {
        this.name = this.playlist.name;
        this.description = this.playlist.description;
        this.tracksId = this.playlist.tracks.map((track) => track.id);
    },
    emits: ['close-edit', 'playlist-updated'],
    methods: {
        async addTrack(trackId) {
            if (!this.tracksId.includes(trackId)) {
                this.tracksId.push(trackId);
            }
        },
        async removeTrack(trackId) {
            const filtered = this.tracksId.filter((id) => id !== trackId);
            this.tracksId = filtered;
        },
        async savePlaylist() {
            const API_URL =`http://localhost:8080/api/playlists/${this.playlist.id}`;
            const tracksId = this.playlist.tracks.map((track) => track.id);
            const requestOptions = {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(
                    {
                        title: this.playlist.name,
                        description: this.playlist.description,
                    }
                )
            };

            await fetch(API_URL, requestOptions)
                .then((response) => {
                    if (response.status > 400 && response.status < 600) {
                        throw new Error("Exception has occurred");
                    }
                    return response.json()
                })
                .then((data) => {
                    console.log(data);
                    this.validationErrors = [];
                    if (data.errors) {
                        Object.values(data.errors).forEach((value) => {
                            this.validationErrors.push(value.pop());
                        });

                        throw new Error("Validation errors have occured");
                    }

                    tracksId.forEach(async(trackId) => {
                        const requestOptions = {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(
                                {
                                    track_id: trackId,
                                    playlist_id: this.playlist.id,
                                }
                            )
                        };
                        await fetch(`http://localhost:8080/api/track-connections`, requestOptions)
                    })
                })
                .then(() => {
                    this.$emit('playlist-updated');
                    this.$emit('close-edit');
                });
        }
    }
}

</script>

<style scope>
input {
    width: 60%;
}

form {
    display: flex;
    flex-direction: column;
}

button {
    max-width: 200px;
}

.button-container {
    display: flex;
    justify-content: flex-end;
}

.load-tracks {
    font-weight: bold;
    cursor: pointer;
    color: green;
}

.errors-container {
    border: 1px red solid;
    background-color: #f247475e;
    border-radius: 3px;
    padding: 10px;
    color: red;
}
</style>