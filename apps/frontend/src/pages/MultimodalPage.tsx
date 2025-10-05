// comments are in English
import { useRef, useState } from "react"
import Tesseract from "tesseract.js"
import { aiChat } from "../lib/api"

export default function MultimodalPage() {
    const [ocrText, setOcrText] = useState("")
    const [sttText, setSttText] = useState("")
    const [aiResult, setAiResult] = useState<any>(null)
    const [busy, setBusy] = useState(false)
    const recogRef = useRef<SpeechRecognition | null>(null)

    async function runOCR(file: File) {
        setBusy(true)
        try {
            const res = await Tesseract.recognize(file, "eng", { logger: () => { } })
            setOcrText(res.data.text || "")
        } finally {
            setBusy(false)
        }
    }

    function startSTT() {
        const SR: any = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
        if (!SR) {
            alert("SpeechRecognition not supported in this browser")
            return
        }
        const recog: SpeechRecognition = new SR()
        recog.lang = "en-US"
        recog.continuous = false
        recog.interimResults = false
        recog.onresult = (e: SpeechRecognitionEvent) => {
            const transcript = Array.from(e.results).map(r => r[0].transcript).join(" ")
            setSttText(transcript)
        }
        recog.onerror = () => { }
        recog.onend = () => { }
        recogRef.current = recog
        recog.start()
    }

    return (
        <div className="space-y-6">
            <h1 className="text-lg font-semibold">Multimodal (client-side)</h1>

            <section className="space-y-2">
                <h2 className="font-semibold">Image → OCR</h2>
                <input type="file" accept="image/*" onChange={(e) => {
                    const f = e.target.files?.[0]; if (f) runOCR(f)
                }} />
                <textarea className="border rounded w-full h-32 px-2 py-1" value={ocrText} onChange={(e) => setOcrText(e.target.value)} />
            </section>

            <section className="space-y-2">
                <h2 className="font-semibold">Audio → Speech-to-Text (browser)</h2>
                <div className="flex items-center gap-2">
                    <button className="px-3 py-2 rounded bg-black text-white" onClick={startSTT}>Record</button>
                </div>
                <textarea className="border rounded w-full h-24 px-2 py-1" value={sttText} onChange={(e) => setSttText(e.target.value)} />
            </section>

            <section className="space-y-2">
                <h2 className="font-semibold">Send to /ai</h2>
                <button
                    disabled={busy}
                    className="px-3 py-2 rounded bg-black text-white disabled:opacity-50"
                    onClick={async () => {
                        setBusy(true)
                        try {
                            const prompt = [ocrText, sttText].filter(Boolean).join("\n\n")
                            if (!prompt.trim()) return
                            const data = await aiChat(prompt)
                            setAiResult(data)
                        } finally {
                            setBusy(false)
                        }
                    }}
                >
                    Send combined text
                </button>
                {aiResult && <pre className="p-3 bg-gray-50 rounded text-sm overflow-auto">{JSON.stringify(aiResult, null, 2)}</pre>}
            </section>
        </div>
    )
}
