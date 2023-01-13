import express, { Request, Response } from 'express';
import { playlistRoute } from './routes/playlist.routes';

const app = express();

app.get('/', (req: Request, res: Response) => {
    res.send('Express + TypeScript Server 2');
});

app.use('/api/playlists', playlistRoute);

export default app;
