import { createClient } from "@supabase/supabase-js"

// Pull vars from environment
const url = import.meta.env.VITE_SUPABASE_URL!
const key = import.meta.env.VITE_SUPABASE_ANON_KEY!

// Debug in prod (optional, can be removed later)
console.log("Supabase URL:", url)
console.log("Supabase Key defined:", !!key)

// Create Supabase client
export const supabase = createClient(url, key)

// Upload file directly to Supabase Storage
export async function uploadToSupabase(file: File) {
    const bucket = "cvscan-files"
    const filename = `${Date.now()}-${file.name}`

    // Upload to Supabase Storage
    const { data, error } = await supabase
        .storage
        .from(bucket)
        .upload(filename, file)

    if (error) throw error

    // Build public URL manually (Supabase convention)
    const publicUrl = `${url}/storage/v1/object/public/${bucket}/${filename}`
    return { path: data.path, publicUrl }
}
