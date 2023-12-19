import os
import sys
# add the directory containing the db module to the Python path
crawl_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(crawl_path)
from crawl.db_crawl import get_data
from db.db_actions import *
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import schedule
import time

# Load environment variables from .env file
load_dotenv()


# Docker
TEMPLATES = os.getenv('TEMPLATESDOCKER')

# TEMPLATES = os.getenv('TEMPLATES')

app = FastAPI()

app.mount("/static", StaticFiles(directory=f"{TEMPLATES}/static"), name="static")
templates = Jinja2Templates(directory=TEMPLATES)

# Get index template
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    total_count_all = count_product()
    return templates.TemplateResponse("index.html", {"request": request, "total_count_all": total_count_all})

# Get title template
@app.get("/title", response_class=HTMLResponse)
async def read_title(request: Request):
    return templates.TemplateResponse("title.html")

# Search by title
@app.post("/title", response_class=HTMLResponse)
async def do_search(request: Request, title: str = Form(...)):
    titles = search_product(title)
    total_count = count_product(title)
    return templates.TemplateResponse("title.html", {'request': request, "results": titles, "total_count": total_count})

# AutoComplete suggestions
@app.get("/suggest")
async def suggest(title: str):
    titles = search_title(title)
    return {"suggestions": titles}

@app.post('/add')
def add(product_id: int, product_name: str, product_price: str, product_finalprice: str, product_url: str, image_src: str, discount: int):
    data = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'product_finalprice': product_finalprice,
        'product_url': product_url,
        'image_src': image_src,
        'discount': discount
    }
    val = insert_data(data)
    if val:
        return {'status': 200, 'message': 'Thêm Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}

@app.put('/products/{product_id}')
def edit(product_id: int, product_name: str, product_price: str, product_finalprice: str, product_url: str, image_src: str, discount: int):
    data = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'product_finalprice': product_finalprice,
        'product_url': product_url,
        'image_src': image_src,
        'discount': discount
    }

    if edit_product(product_id, data):
        return {'status': 200, 'message': 'Sửa Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}

@app.delete('/products/{product_id}')
def remove(product_id: int):
    if remove_product(product_id):
        return {'status': 200, 'message': 'Xóa Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}


@app.get('/crawl')
def crawl():
    get_data()
    return {"status": "Hoàn thành !!!"}

# Crawl data automatically every day at 00:00
@app.get('/crawl_auto')
def crawl_auto():
    # Lập lịch công việc cào dữ liệu hàng ngày lúc 00:00
    schedule.every().day.at("00:00").do(get_data)
    #schedule.every(3).minutes.do(get_data)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    # import uvicorn
    # uvicorn.run(app, port=8000, reload=True)
    pass