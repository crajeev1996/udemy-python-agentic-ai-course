from fastapi import FastAPI, Body, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ollama import Client

app = FastAPI()
client = Client(host="http://localhost:11434")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/contact-us")
def contact_us():
    return {"email": "crajeev1996@gmail.com"}

@app.post("/chat")
def chat(message: str = Body(..., description="The Message")):
    response = client.chat(model="gemma3:4b", messages=[
        {"role": "user", "content": message}
    ])
    return {"response": response.message.content}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")
    return {"filename": file.filename, "content": text}

## Run with "fastapi dev server.py"