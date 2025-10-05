import { createClient } from "@supabase/supabase-js"

const url = import.meta.env.VITE_SUPABASE_URL!
const key = import.meta.env.VITE_SUPABASE_KEY!

// Create Supabase client
export const supabase = createClient(url, key)

// Upload file directly to Supabase Storage
export async function uploadToSupabase(file: File) {
    const bucket = "cvscan-files"
    const filename = `${Date.now()}-${file.name}`
    const { data, error } = await supabase.storage.from(bucket).upload(filename, file)
    if (error) throw error

    // Construct public URL
    const publicUrl = `${url}/storage/v1/object/public/${bucket}/${filename}`
    return { path: data.path, publicUrl }
}
