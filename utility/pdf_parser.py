from io import BytesIO
import re
import PyPDF2
import requests
from PharmaBot.utility import util_func

class PdfParser:
    def __init__(self,pdf_url):
        try:
            r = requests.get(pdf_url)
            with BytesIO(r.content) as data:
                read_pdf = PyPDF2.PdfFileReader(data)
                data = ""
                for i in range(read_pdf.numPages):
                    pageObj = read_pdf.getPage(i)
                    data += pageObj.extract_text()
            self.pdf_data = data
        except:
            pdf_url = False

    '''
    By using a regex, filter the text in the pdf to extract only the medicine side effects.
    '''
    def get_side_effects(self):
        raw_side_effects = re.findall('(?i)[\d]\.\s*possibili effetti indesiderati(.*?)\.\n[\d]\.',self.pdf_data,re.DOTALL)[1]
        side_effects = util_func.clean_data(raw_side_effects)
        
        return side_effects
