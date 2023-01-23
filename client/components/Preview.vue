<template>

    <div v-if="!editVisible">
        <div class="preview-header">
            <div class="playlist-title">
                <h1>Playlist details</h1>
            </div>
            <span @click="this.editVisible = true"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                    fill="currentColor" class="bi bi-pen-fill" viewBox="0 0 16 16">
                    <path
                        d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001z" />
                </svg>
            </span>
            <span @click="$emit('close-preview', null)">&#10060;</span>
        </div>

        <div class="playlist-preview-container">
            <div class="playlist-preview">
                <dl>
                    <dt>Name</dt>
                    <dd>{{ playlistData?.name }}</dd>

                    <dt>Description</dt>
                    <dd>{{ playlistData?.description }}</dd>

                    <dt>Created at</dt>
                    <dd>{{ playlistData?.createdAt }}</dd>
                </dl>
            </div>
            <div class="playlist-tracks">
                <dl>
                    <dt>Tracks</dt>
                    <dd v-for="track in playlistData?.tracks.slice(0, 10)">
                        <div style="font-weight: bold">
                            &#9835; {{ track.name }}
                        </div>
                        <div>
                            <svg style="margin-top:5px; margin-bottom: -2px; margin-right: -2px;" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-person-fill" viewBox="0 0 16 16">
                                <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
                            </svg>
                            {{ track.artist }}
                        </div>

                    </dd>
                </dl>
            </div>
            <div class="playlist-tracks">
                <dl>
                    <dt>&nbsp;</dt>
                    <dd v-for="track in playlistData?.tracks.slice(10, 20)">
                        <div style="font-weight: bold">
                            &#9835; {{ track.name }}
                        </div>
                        <div>
                            <svg style="margin-top:5px; margin-bottom: -2px; margin-right: -2px;" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-person-fill" viewBox="0 0 16 16">
                                <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
                            </svg>
                            {{ track.artist }}
                        </div>
                    </dd>
                </dl>
            </div>
        </div>
    </div>

    <div v-if="editVisible">
        <EditPlaylist :playlist="playlistData" @close-edit="this.editVisible = false"
            @playlist-updated="afterUpdated" />
    </div>

</template>


<script>
import EditPlaylist from './EditPlaylist.vue';

export default {
    name: "Preview",
    props: {
        playlistId: Number,
    },
    data: () => ({
        playlistData: null,
        editVisible: false,
    }),
    emits: ["close-preview", "edit-completed"],
    async created() {
        await this.fetchData();
    },
    watch: {
        playlistId() {
            this.fetchData();
        }
    },
    methods: {
        async fetchData() {
            const API_URL = `https://localhost:49157/api/PlaylistApi/GetPlaylistsById/${this.playlistId}`;
            await fetch(API_URL)
                .then((response) => response.json())
                .then((data) => {
                    this.playlistData = data.responseData;
                });
        },
        async afterUpdated() {
            this.fetchData();
            this.$emit('edit-completed');
        }
    },
    components: { EditPlaylist }
}

</script>

<style scope>
span {
    cursor: pointer;
}

span:first-of-type {
    margin-left: auto;
    margin-right: 20px;
}

dt {
    font-weight: bold;
    margin-bottom: 0.2em;
    font-size: 18px;
}

dl,
dd {
    font-size: 0.9rem;
}

dd {
    margin-bottom: 1.7em;
}

.preview-header,
.playlist-preview-container {
    display: flex;
    justify-content: space-between;
}

.playlist-title {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 45px;
}

.playlist-tracks {
    width: 30%;
}

.playlist-preview {
    width: 40%;
}
</style>