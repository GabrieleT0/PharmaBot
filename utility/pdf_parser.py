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
    
    def get_what_is_name(self):
        self.pdf_data = self.pdf_data.replace('informazioni.','informazioni')
        self.pdf_data = self.pdf_data.replace('10','00')
        raw_medicine_name = re.findall(r'^.*\b(?i)1.\b.*$',self.pdf_data,re.M)[0]
        raw_what_is = re.findall(f"(?i){raw_medicine_name}(.*?)\.\n[\d]\.",self.pdf_data,re.DOTALL)[0] 
        try:
            what_is = raw_what_is.split(raw_medicine_name)[1]
        except:
            what_is = raw_what_is.split('cosa serve')[1]
        what_is = util_func.clean_data(what_is)

        return what_is
    
    def get_how_take(self):
        #raw_side_effects = re.findall('(?i)[\d]\.\s*Come prendere(.*?)\.\n[\d]\.',self.pdf_data,re.DOTALL)[1]
        raw_how_take = re.findall('(?i)[\d]\.\s*Come prendere(.*?)(\.\n|\n)[\d]\.',self.pdf_data,re.DOTALL)[1]
        how_take = util_func.clean_data(raw_how_take[0])
        
        return how_take




        

    