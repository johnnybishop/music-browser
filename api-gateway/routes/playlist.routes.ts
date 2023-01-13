import { Router } from "express";
import * as apiClient from '../helpers/api-client';

export const playlistRoute = Router();

playlistRoute.get("/", async (req, res) => {
    console.log('Todo get playlists')
    await apiClient.performPlaylistRequest('', 'get');
    res.json({});
});

playlistRoute.get("/:playlistId", (req, res) => {
    const playlistId = req.params['playlistId'];
    console.log(`Todo get playlist with id=${playlistId}`);
    res.json({playlistId});
});
