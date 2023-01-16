import axios, { Axios, AxiosError, AxiosResponse } from 'axios';

export const performRequest = async (host: string, port: number, route: string, method: string, data?: object): Promise<AxiosResponse> => {
    return await axios({
        method: method,
        url: `http://${host}:${port}/${route}`,
        data,
        headers: {
            apiKey: process.env.API_KEY
        }
    })
    .catch((err) => {
        throw err;
    });
}