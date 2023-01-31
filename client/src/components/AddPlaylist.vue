<template>
    <div class="preview-header">
        <div class="playlist-title">
            <h1>Add playlist</h1>
        </div>
        <span @click="$emit('close-add', null)">&#10060;</span>
    </div>

    <div v-if="validationErrors.length" class="errors-container">
        <div v-for="error in validationErrors">
            {{ error }}
        </div>
    </div>
    <form v-on:submit.prevent="addPlaylist">
        <input type="text" v-model="name" placeholder="Insert playlist name..." />
        <input type="text" v-model="description" placeholder="Insert playlist description..." />
        <Tracks @track-added="addTrack" @track-removed="removeTrack" />
        <div class="button-container">
            <button class="btn" type="submit">Add</button>
        </div>
    </form>

</template>


<script>
import Tracks from './Tracks.vue';

export default {
    name: 'AddPlaylist',
    components: {
        Tracks
    },
    props: {
        playlistId: Number,
    },
    data: () => ({
        name: null,
        description: null,
        validationErrors: [],
        tracksId: [],
    }),
    async created() {
        this.validationErrors = []
    },
    emits: ['close-add', 'playlist-added'],
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
        async addPlaylist() {
            if (!this.name) {
                this.validationErrors.push('Name must be filled!')

                return;
            } else {
                this.validationErrors = [];
            }

            if (!this.description) {
                this.validationErrors.push('Description must be filled!')

                return
            } else {
                this.validationErrors = [];

            }
        
            const API_URL = `http://localhost:8080/api/playlists/`;
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(
                    {
                        title: this.name,
                        description: this.description,
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
                    this.validationErrors = [];
                    if (data && data.errors) {
                        Object.values(data.errors).forEach((value) => {
                            this.validationErrors.push(value.pop());
                        });

                        throw new Error("Validation errors have occured");
                    }

                    this.tracksId.forEach(async(trackId) => {
                        const requestOptions = {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(
                                {
                                    track_id: trackId,
                                    playlist_id: data,
                                }
                            )
                        };
                        await fetch(`http://localhost:8080/api/track-connections`, requestOptions)
                    })
                })
                .then(() => {
                    this.$emit('playlist-added');
                    this.$emit('close-add');
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