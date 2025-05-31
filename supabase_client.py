from supabase import create_client, Client

url = "https://thgjxrnskvlzcgnshcwt.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRoZ2p4cm5za3ZsemNnbnNoY3d0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg3MTMwNzYsImV4cCI6MjA2NDI4OTA3Nn0.RQ6Pzc-8RrFZTlKX7Q8GmDOaFh0PY08yBrL-_4CQed0"  # עדיף להשתמש ב-Anon Public Key

supabase: Client = create_client(url, key)
