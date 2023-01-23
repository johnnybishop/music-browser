import assert from "assert";
import { AxiosError } from "axios";
import { Request, Response, Router } from "express";
import { StatusCodes } from "http-status-codes";
import { HttpMethodEnum } from "../enums/HttpMethodEnum";
import * as apiClient from '../helpers/api-client.helper';
import { handleErrorResponse } from "../helpers/error-response.helper";

export const trackConnectionRoutes = Router();

const HOST = process.env.PLAYLISTS_SERVICE_HOST;
assert(HOST, "Missing PLAYLISTS_SERVICE_HOST Env Variable");

const PORT = process.env.PLAYLISTS_SERVICE_PORT;
assert(PORT, "Missing PLAYLISTS_SERVICE_PORT Env Variable");

const BASE_URL  = 'track_connection';

trackConnectionRoutes.post("/", async (req: Request, res: Response) => {
    const data = req.body;
    
    try {
        const response = await apiClient.performRequest(HOST, +PORT, BASE_URL, HttpMethodEnum.POST, data);
        res.status(StatusCodes.CREATED).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});
