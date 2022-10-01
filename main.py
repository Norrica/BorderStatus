import io

import requests
import uvicorn
import json
from fastapi import FastAPI
from starlette.responses import StreamingResponse, HTMLResponse

def request_img(coords):
    req = f"https://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&size=650,450&z=13&l=sat,skl,trf"
    im_png = requests.get(req).content
    return im_png

app = FastAPI()
with open("APPS.json", "r") as f:
    kpps:dict = json.load(f)

@app.get("/",response_class=HTMLResponse)
def index():
    with open("index.html","r") as f:
        return HTMLResponse(content=f.read())

for k,v in kpps.items():
    @app.get(f"/{k}")
    def KPP(coords=v):
        im_png = request_img(coords)
        return StreamingResponse(io.BytesIO(im_png), media_type="image/png")

# uvicorn.run(app)