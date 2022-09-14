import io
import json
import uvicorn
import requests
from fastapi import FastAPI
from starlette.responses import StreamingResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/give-me-beauty/{keyword}")
async def discover_beauty(keyword: str):
    print(keyword)
    client_id = "0mBiGS_e6Yibx1I-bGTXj6RBM09BDFmXzp-zxG1dxFM"
    url = 'https://api.unsplash.com/photos/random?client_id={}&q={}'.format(client_id, keyword)
    print(url)
    response = requests.get(url=url)
    assert response.status_code == 200
    info = response.text
    info_dict = json.loads(info)
    raw_url = info_dict.get("urls").get("full")
    print(raw_url)
    def iter():
        with requests.get(url=raw_url) as resp:
            yield from io.BytesIO(resp.content)
    return StreamingResponse(iter(), media_type="image/png")


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=8080)