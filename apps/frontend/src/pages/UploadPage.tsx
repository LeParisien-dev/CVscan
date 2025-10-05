import { useState } from "react"
import { uploadCV, matchStatCV } from "../lib/api"
import { uploadToSupabase } from "../lib/storage"

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null)
    const [result, setResult] = useState<any>(null)
    const [uploadMode, setUploadMode] = useState<"render" | "supabase">("supabase")
    const [loading, setLoading] = useState(false)

    async function handleUploadAndMatch() {
        if (!file) return
        setLoading(true)
        try {
            let path: string

            // 1️⃣ Upload to chosen mode
            if (uploadMode === "render") {
                const data = await uploadCV(file)
                path = data.filename || data.path || data.name
            } else {
                const data = await uploadToSupabase(file)
                path = data.path
            }

            // 2️⃣ Call AI-Lite matching (local backend)
            const matchRes = await matchStatCV({
                cv_filename: path,
                job_id: "2148951b-852f-40c3-9a56-9a730fd1eb26" // adapt if needed
            })

            setResult(matchRes)
        } catch (err: any) {
            setResult({ error: err.message })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="space-y-5 p-6">
            <h1 className="text-lg font-semibold">AI-Lite CV Matching</h1>

            <div className="flex items-center gap-4">
                <label className="flex items-center gap-1">
                    <input
                        type="radio"
                        name="mode"
                        value="render"
                        checked={uploadMode === "render"}
                        onChange={() => setUploadMode("render")}
                    />
                    Backend (Render)
                </label>

                <label className="flex items-center gap-1">
                    <input
                        type="radio"
                        name="mode"
                        value="supabase"
                        checked={uploadMode === "supabase"}
                        onChange={() => setUploadMode("supabase")}
                    />
                    Direct (Supabase)
                </label>
            </div>

            <input
                type="file"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="block w-full border border-gray-300 rounded p-2"
            />

            <button
                className="px-4 py-2 rounded bg-black text-white disabled:opacity-50"
                disabled={!file || loading}
                onClick={handleUploadAndMatch}
            >
                {loading ? "Processing..." : "Upload & Match"}
            </button>

            {result && (
                <div className="p-4 bg-gray-50 rounded-lg mt-4 text-sm space-y-2">
                    {result.error && <p className="text-red-600">{result.error}</p>}
                    {result.score && (
                        <>
                            <p><strong>Score:</strong> {(result.score * 100).toFixed(1)}%</p>
                            <p><strong>Common words:</strong> {result.details?.n_common}</p>
                            <p><strong>Top:</strong> {result.details?.top_common?.slice(0, 8).join(", ")}</p>
                        </>
                    )}
                </div>
            )}
        </div>
    )
}
