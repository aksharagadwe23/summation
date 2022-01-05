import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import json


def pdf_reader(filepath):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams(char_margin=4,line_margin=2)
    device = TextConverter(rsrcmgr, retstr,laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 50
    caching = True
    fp = open(filepath, 'rb')
    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=maxpages,password=password,caching=caching,check_extractable=False):
        interpreter.process_page(page)

    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text

