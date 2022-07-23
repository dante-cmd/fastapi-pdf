from re import template
from fastapi import FastAPI, Request,  File, Form, UploadFile
from fastapi.responses import RedirectResponse ,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
import pandas as pd
import pdfplumber 
import re
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import Response
import xlsxwriter
from extract_pages import pages_to

app = FastAPI()
templates = Jinja2Templates(directory='frontend/templates')

@app.get('/home', response_class=HTMLResponse)
def home(request:Request):
    app.mount(
         "/frontend/static/styles", 
         StaticFiles(directory= "frontend/static/styles"), 
         name="styles")
    result = "Type a campaing and country"
    
    return templates.TemplateResponse('form.html', {'request':request,  'result' : result})

@app.post('/home', response_description='xlsx')
def post_home( 
    request:Request, 
    campaign:int = Form(...), 
    country:str = Form(...), 
    page_range:str = Form(...), 
    type_name: str = Form(...),
    file: UploadFile = File(...)
    ):
    # read pdf file
    
    test_data = pdfplumber.open(file.file)
    # extract pages
    df = pages_to(test_data)
    # create io file
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    output.seek(0)
    # Here we specify that campaing and country are string an these have the same name 
    # in the form of the HTML page
    
    # The key `request: Request` always is the same
    # The key must coincide with `Result: {{ result }}` of html page
    # the value result can be anytype that support a json
    
    #campaing = num
    #country = num**2
    # result = f'country: {country} and campaing: {campaign} {type_name} {page_range}'
    # return templates.TemplateResponse(
    #     'form.html', 
    #     {'request':request,  'result':result}) #,'result_num': result_num, 'result_val':result_val 
    headers = {
        'Content-Disposition': 'attachment; filename="filename.xlsx"'
    }
    return StreamingResponse(output, headers=headers)
