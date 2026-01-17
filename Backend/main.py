from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/submit")
async def submit_data(request: Request):
    data = await request.json()
    return {"status": "received", "data": data}

