import api from "./api";

export const getDashboard = async () => {
    const response = await api.get("/dashboard/latest");
    return response.data;
};

export const getStats = async () => {
    const response = await api.get("/dashboard/stats");
    return response.data;
};

export const getExecutiveBrief = async (industry: string) => {
    const response = await api.get(`/brief/${industry}`);
    return response.data;
};