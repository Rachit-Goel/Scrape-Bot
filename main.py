# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import requests
import supabase
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Server is listening for API requests on port:8080"}

SUPABASE_URL = "https://arxgkzdinwrsnbqcfaiu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyeGdremRpbndyc25icWNmYWl1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTAzODc5NTYsImV4cCI6MjAwNTk2Mzk1Nn0.9yABkJYE6a401J9zaFd7LCIF4vp8JdZnsfFuv0Gfeqg"
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def remove_unwanted_characters(input_string):
    unwanted_characters = ['\n', '\t', '\r']
    for char in unwanted_characters:
        input_string = input_string.replace(char, ' ')
    return input_string

@app.post("/scrape")
async def scrape_page(request: Request):
    data = await request.json()
    url = data.get("url")
    print(url)
    if not url:
        return JSONResponse(status_code=400, content={"message": "URL not provided."})

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        text_content = soup.get_text()
        text_content = remove_unwanted_characters(text_content)

        table = "articles"
        new_record = {"content": text_content}
        print(new_record)
        supabase_client.table(table).insert(new_record).execute()

        return {"message": "Scraped content stored in the database."}
    
    except requests.exceptions.RequestException as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/search")
async def search_text(request: Request):
    data = await request.json()
    query = data.get("query")
    if not query:
        return JSONResponse(status_code=400, content={"message": "Search query not provided."})

    try:
        table = "articles"
        search_result = supabase_client.table(table).select("content").ilike("content", f"%{query}%").execute()
        print(search_result)
        data_json = json.loads(search_result.json())
        data_entries = data_json['data']

        snippets = []
        for row in data_entries:
            content = row.get("content")
            try:
                start_idx = content.lower().index(query.lower())
            except Exception as e:
                continue
            
            snippet = content[max(start_idx - 100, 0): start_idx + 100]
            snippets.append({"snippet": snippet})

        return snippets

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": str(e)})
