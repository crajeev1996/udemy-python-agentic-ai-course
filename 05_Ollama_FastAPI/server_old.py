from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434",
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact-us")
def read_root():
    return {"email": "crajeev1996@gmail.com"}

@app.post("/chat")
def chat(
        message: str = Body(..., description="The Message")
):
    response = client.chat(model="gemma3:4b", messages=[
        { "role": "user", "content":message  }
    ])

    return { "response": response.message.content }

## Run base "fastapi dev server.py" when you want to run this Python script as a FastAPI server