import express from 'express';
import { playlistRoute } from './routes/playlist.routes';
import { trackRoute } from './routes/track.routes';

const app = express();
app.use(express.json());
app.use('/api/playlists', playlistRoute);
app.use('/api/tracks', trackRoute);


export default app;
