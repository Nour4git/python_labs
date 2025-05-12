from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.post("/generate")
def generate(prompt: str):
    return {"response": f"You said: {prompt}"}
