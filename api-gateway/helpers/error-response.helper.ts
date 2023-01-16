import { AxiosError } from "axios";
import { Response } from "express";
import { StatusCodes } from "http-status-codes";

export const handleErrorResponse = (err: AxiosError | unknown, res: Response): void => {
    if (err instanceof AxiosError) {
        res.status(getStatusCode(err)).json(getErrorResponseData(err));
    } 
    
    res.status(StatusCodes.INTERNAL_SERVER_ERROR).json(err);
}

const getStatusCode = (err: AxiosError): number => {
    return err.response ? err.response.status : StatusCodes.INTERNAL_SERVER_ERROR;
}

const getErrorResponseData = (err: AxiosError): string => {
    return err.response ? err.response.data as string : 'An error occurred.';
}