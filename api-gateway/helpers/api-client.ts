import axios from 'axios';

const PLAYLISTS_HOST = process.env.PLAYLISTS_SERVICE_HOST;
const TRACKS_HOST = process.env.TRACKS_SERVICE_HOST;

const PLAYLISTS_PORT = process.env.PLAYLISTS_SERVICE_PORT;
const TRACKS_PORT = process.env.TRACKS_SERVICE_PORT;

export const performPlaylistRequest = async (route: string, method: string) => {
    axios({
        method: method,
        url: `http://${PLAYLISTS_HOST}:${PLAYLISTS_PORT}/${route}/playlists`,
    }).then((res) => {
        console.log(res);
    })
}