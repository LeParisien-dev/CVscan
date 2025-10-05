import axios from "axios"

const baseURL = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || ""
export const api = axios.create({
    baseURL,
    headers: { "Content-Type": "application/json" },
    withCredentials: false
})

// --- SYSTEM HEALTH ---
export async function pingHealth() {
    const { data } = await api.get("/api/v1/health")
    return data
}

// --- UPLOAD (Render backend direct) ---
export async function uploadCV(file: File) {
    const fd = new FormData()
    fd.append("file", file)
    const { data } = await api.post("/api/v1/upload-cv", fd, {
        headers: { "Content-Type": "multipart/form-data" }
    })
    return data
}

// --- JOB CREATION ---
export async function createJob(payload: { job_id?: string; content: string }) {
    const { data } = await api.post("/api/v1/job", payload)
    return data
}

// --- LEGACY MATCH (random/LLM placeholder) ---
export async function matchCV(payload: { cv_filename: string; job_id: string }) {
    const { data } = await api.post("/api/v1/match", payload)
    return data
}

// --- NEW: AI-Lite Statistical Match ---
export async function matchStatCV(payload: { cv_filename: string; job_id: string }) {
    const { data } = await api.post("/api/v1/match-stat", payload)
    return data
}

// --- AI CHAT (not used here but kept for completeness) ---
export async function aiChat(prompt: string) {
    const { data } = await api.post("/api/v1/ai", { prompt })
    return data
}
