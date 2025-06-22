from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
async def get_outline(country: str):
    try:
        url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                raise HTTPException(status_code=404, detail="Wikipedia page not found.")

        soup = BeautifulSoup(resp.text, "html.parser")

        markdown = "## Contents\n\n"

        # Find all heading tags in order
        for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(header.name[1])
            text = header.get_text().strip()
            markdown += f"{'#' * level} {text}\n\n"

        return markdown.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
