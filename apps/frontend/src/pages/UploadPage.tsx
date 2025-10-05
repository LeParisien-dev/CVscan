import { useState } from "react"
import { uploadCV } from "../lib/api"
import { uploadToSupabase } from "../lib/storage"

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null)
    const [result, setResult] = useState<any>(null)
    const [uploadMode, setUploadMode] = useState<"render" | "supabase">("supabase")
    const [loading, setLoading] = useState(false)

    async function handleUpload() {
        if (!file) return
        setLoading(true)
        try {
            let data
            if (uploadMode === "render") {
                data = await uploadCV(file)
            } else {
                data = await uploadToSupabase(file)
            }
            setResult(data)
        } catch (err: any) {
            setResult({ error: err.message })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="space-y-4">
            <h1 className="text-lg font-semibold">Upload CV</h1>

            <div className="flex items-center gap-3">
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

            <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />

            <button
                className="px-3 py-2 rounded bg-black text-white disabled:opacity-50"
                disabled={!file || loading}
                onClick={handleUpload}
            >
                {loading ? "Uploading..." : "Upload"}
            </button>

            {result && (
                <pre className="p-3 bg-gray-50 rounded text-sm overflow-auto">
                    {JSON.stringify(result, null, 2)}
                </pre>
            )}
        </div>
    )
}
