import axios from "axios"

const baseURL = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || ""
export const api = axios.create({
    baseURL,
    headers: { "Content-Type": "application/json" },
    withCredentials: false
})

// Helpers for endpoints you already have
export async function pingHealth() {
    const { data } = await api.get("/api/v1/health")
    return data
}

export async function uploadCV(file: File) {
    const fd = new FormData()
    fd.append("file", file)
    const { data } = await api.post("/api/v1/upload-cv", fd, {
        headers: { "Content-Type": "multipart/form-data" }
    })
    return data
}

export async function createJob(payload: { job_id?: string; content: string }) {
    const { data } = await api.post("/api/v1/job", payload)
    return data
}

export async function matchCV(payload: { cv_filename: string; job_id: string }) {
    const { data } = await api.post("/api/v1/match", payload)
    return data
}

export async function aiChat(prompt: string) {
    const { data } = await api.post("/api/v1/ai", { prompt })
    return data
}
