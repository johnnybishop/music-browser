import express from 'express';
import { playlistRoute } from './routes/playlist.routes';
import { trackRoute } from './routes/track.routes';
import { trackConnectionRoutes } from './routes/track-connection.routes';
var cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());
app.use('/api/playlists', playlistRoute);
app.use('/api/tracks', trackRoute);
app.use('/api/track-connections', trackConnectionRoutes);


export default app;
