import axios, { Axios, AxiosError, AxiosResponse } from 'axios';

export const performRequest = async (host: string, port: number, route: string, method: string, data?: object, pageParam?: string): Promise<AxiosResponse> => {
    const config = {
        method: method,
        params: {
          page: pageParam
        },
        url: `http://${host}/${route}`,
        data,
        headers: {
            apiKey: process.env.API_KEY
        }
    }

    return await axios(config)
    .catch((err) => {
        console.log(err);
        throw err;
    });
}