import pandas as pd
import pdfplumber 
import re

def pages_to(pdf_data):

    n = int(len(pdf_data.pages)/10)
    data_out = {}
    for i, page in enumerate(pdf_data.pages[1:n]):
        data_out[i] = page.extract_text()
    out = pd.Series(data_out)
    return out

if __name__ == '__main__':
    test_data = pdfplumber.open('input.pdf')

    print(pages_to(test_data))