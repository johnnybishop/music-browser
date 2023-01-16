require('dotenv').config();

import assert from 'assert';
import app from './app';

const PORT = process.env.API_GATEWAY_PORT;
const HOST = process.env.API_GATEWAY_HOST ;
assert(PORT, "Missing PORT Env Variable");
assert(HOST, "Missing HOST Env Variable");

app.listen(PORT, () => {
    console.log(`[server]: Server is running at http://${HOST}:${PORT}`);
});

process.on("unhandledRejection", (err) => {
    console.error("unhandledRejection", err);
    // process.exit(1);
});