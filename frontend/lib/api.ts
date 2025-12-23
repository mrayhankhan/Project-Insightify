import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
});

export const uploadDataset = async (type: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`/upload/${type}`, formData);
    return response.data;
};

export const getPreview = async (type: string) => {
    const response = await api.get(`/data/${type}/preview`);
    return response.data;
};

export const getStats = async (type: string) => {
    const response = await api.get(`/data/${type}/stats`);
    return response.data;
};

export const getKPIs = async (type: string) => {
    const response = await api.get(`/data/${type}/kpis`);
    return response.data;
};

export const getSegmentation = async (type: string, n_clusters: int = 3) => {
    const response = await api.get(`/data/${type}/segmentation?n_clusters=${n_clusters}`);
    return response.data;
};

export const getInsights = async (type: string) => {
    const response = await api.get(`/data/${type}/insights`);
    return response.data;
};
