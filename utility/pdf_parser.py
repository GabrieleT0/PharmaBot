from io import BytesIO
import re
import PyPDF2
import requests
from utility import util_func

class PdfParser:
    def __init__(self,pdf_url):
        r = requests.get(pdf_url)
        with BytesIO(r.content) as data:
            read_pdf = PyPDF2.PdfReader(data)
            data = ""
            for i in range(len(read_pdf.pages)):
                pageObj = read_pdf.pages[i]
                data += pageObj.extract_text()
        self.pdf_data = data

    '''
    By using a regex, filter the text in the pdf to extract only the medicine side effects.
    '''
    def get_side_effects(self):
        if isinstance(self.pdf_data,str):
            raw_side_effects = util_func.clean_header(self.pdf_data)
            try:
                raw_side_effects = re.findall('(?i)[\d]\.\s*possibili effetti indesiderati(.*?)\.\n[\d]\.',raw_side_effects,re.DOTALL)[1]
                side_effects = util_func.clean_data(raw_side_effects)

                return side_effects
            except IndexError:
                return False
        else:
            return False
    
    def get_what_is_name(self):
        self.pdf_data = self.pdf_data.replace('informazioni.','informazioni')
        self.pdf_data = self.pdf_data.replace('10','00')
        if isinstance(self.pdf_data,str):
            try:
                raw_medicine_name = re.findall(r'^.*\b(?i)1.\b.*$',self.pdf_data,re.M)[0]
                raw_what_is = re.findall(f"(?i){raw_medicine_name}(.*?)\.\n[\d]\.",self.pdf_data,re.DOTALL)[0] 
                try:
                    what_is = raw_what_is.split(raw_medicine_name)[1]
                except:
                    what_is = raw_what_is.split('cosa serve')[1]
                what_is = util_func.clean_data(what_is)
            except IndexError:
                return False

            return what_is
        else:
            return False
    
    def get_how_take(self):
        if isinstance(self.pdf_data,str):
            raw_how_take = util_func.clean_header(self.pdf_data)
            try:
                raw_how_take = re.findall('(?i)[\d]\.\s*Come prendere(.*?)(\.\n|\n)[\d]\.',raw_how_take,re.DOTALL)[1]
                how_take = util_func.clean_data(raw_how_take[0])

                return how_take
            except IndexError:
                return False            
        else:
            
            return False

    def before_take(self):
        if isinstance(self.pdf_data,str):
            before_take = util_func.clean_header(self.pdf_data)
            try:
                before_take = re.findall('(?i)[\d]\.\s*Cosa deve sapere prima di prendere(.*?)(\.\n|\n)[\d]\.',before_take,re.DOTALL)[1]
                before_take = util_func.clean_data(before_take[0])
                
                return before_take
            except IndexError:
                return False
        else:
            return False
    
    def get_preservation(self):
        if isinstance(self.pdf_data,str):
            preservation = util_func.clean_header(self.pdf_data)
            try:
                preservation = re.findall('(?i)[\d]\.\s*Come conservare(.*?)(\.\n|\n)[\d]\.',preservation,re.DOTALL)[1]
                preservation = util_func.clean_data(preservation[0])
            
                return preservation
            except IndexError:
                return False
        else:
            return False