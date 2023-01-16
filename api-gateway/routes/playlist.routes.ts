import assert from "assert";
import { AxiosError } from "axios";
import { Request, Response, Router } from "express";
import { StatusCodes } from "http-status-codes";
import { HttpMethodEnum } from "../enums/HttpMethodEnum";
import * as apiClient from '../helpers/api-client.helper';
import { handleErrorResponse } from "../helpers/error-response.helper";

export const playlistRoute = Router();

const HOST = process.env.PLAYLISTS_SERVICE_HOST;
assert(HOST, "Missing PLAYLISTS_SERVICE_HOST Env Variable");

const PORT = process.env.PLAYLISTS_SERVICE_PORT;
assert(PORT, "Missing PLAYLISTS_SERVICE_PORT Env Variable");

const BASE_URL  = 'playlists';

playlistRoute.get("/", async (req: Request, res: Response) => {
    try {
        const response = await apiClient.performRequest(HOST, +PORT, BASE_URL, HttpMethodEnum.GET);
        res.json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});

playlistRoute.get("/:playlistId", async (req: Request, res: Response) => {
    const playlistId = req.params['playlistId'];
    
    try {
        const response = await apiClient.performRequest(HOST, +PORT, `${BASE_URL}/${playlistId}`, HttpMethodEnum.GET);
        res.status(StatusCodes.OK).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});

playlistRoute.post("/", async (req: Request, res: Response) => {
    const data = req.body;
    
    try {
        const response = await apiClient.performRequest(HOST, +PORT, BASE_URL, HttpMethodEnum.POST, data);
        res.status(StatusCodes.CREATED).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});

playlistRoute.put("/:playlistId", async (req: Request, res: Response) => {
    const data = req.body;
    const playlistId = req.params['playlistId'];

    try {
        const response = await apiClient.performRequest(HOST, +PORT, `${BASE_URL}/${playlistId}`, HttpMethodEnum.PUT, data);
        res.status(StatusCodes.NO_CONTENT).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});


playlistRoute.delete("/:playlistId", async (req: Request, res: Response) => {
    const playlistId = req.params['playlistId'];

    try {
        const response = await apiClient.performRequest(HOST, +PORT, `${BASE_URL}/${playlistId}`, HttpMethodEnum.DELETE);
        res.status(StatusCodes.OK).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});