import assert from "assert";
import { AxiosError } from "axios";
import { Request, Response, Router } from "express";
import { StatusCodes } from "http-status-codes";
import { HttpMethodEnum } from "../enums/HttpMethodEnum";
import * as apiClient from '../helpers/api-client.helper';
import { handleErrorResponse } from "../helpers/error-response.helper";

export const trackRoute = Router();

const HOST = process.env.TRACKS_SERVICE_HOST;
assert(HOST, "Missing TRACKS_SERVICE_HOST Env Variable");

const PORT = process.env.TRACKS_SERVICE_PORT;
assert(PORT, "Missing TRACKS_SERVICE_PORT Env Variable");

const BASE_URL  = 'track';

trackRoute.get("/", async (req: Request, res: Response) => {
    try {
        const response = await apiClient.performRequest(HOST, +PORT, BASE_URL, HttpMethodEnum.GET);
        res.json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});

trackRoute.get("/:trackId", async (req: Request, res: Response) => {
    const trackId = req.params['trackId'];
    
    try {
        const response = await apiClient.performRequest(HOST, +PORT, `${BASE_URL}/${trackId}`, HttpMethodEnum.GET);
        res.status(StatusCodes.OK).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});

trackRoute.post("/", async (req: Request, res: Response) => {
    const data = req.body;
    
    try {
        const response = await apiClient.performRequest(HOST, +PORT, BASE_URL, HttpMethodEnum.POST, data);
        res.status(StatusCodes.CREATED).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});

trackRoute.put("/:trackId", async (req: Request, res: Response) => {
    const data = req.body;
    const trackId = req.params['trackId'];

    try {
        const response = await apiClient.performRequest(HOST, +PORT, `${BASE_URL}/${trackId}`, HttpMethodEnum.PUT, data);
        res.status(StatusCodes.NO_CONTENT).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});


trackRoute.delete("/:trackId", async (req: Request, res: Response) => {
    const trackId = req.params['trackId'];

    try {
        const response = await apiClient.performRequest(HOST, +PORT, `${BASE_URL}/${trackId}`, HttpMethodEnum.DELETE);
        res.status(StatusCodes.OK).json(response.data);
    } catch (err) {
        handleErrorResponse(err, res);
    }
});

