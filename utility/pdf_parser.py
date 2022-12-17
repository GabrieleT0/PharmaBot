from io import BytesIO
import re
import PyPDF2
import requests
class PdfParser:
    def __init__(self,pdf_url):
        try:
            r = requests.get(pdf_url)
            with BytesIO(r.content) as data:
                read_pdf = PyPDF2.PdfFileReader(data)
                data = ''
                for i in range(read_pdf.numPages):
                    pageObj = read_pdf.getPage(i)
                    data += pageObj.extract_text()
            self.pdf_data = data
        except:
            return 'PDF recovery error'

    '''
    By using a regex, filter the text in the pdf to extract only the medicine side effects
    '''
    def get_side_effects(self):
        raw_side_effects = re.findall('(?i)[\d]\.\s*possibili effetti indesiderati(.*?)\.\n[\d]\.',self.pdf_data,re.DOTALL)[1]
        filtered_side_effects = re.sub(r"Documento reso disponibile da AIFA il \d{2}\/\d{2}\/\d{4}(.*?)\)\.","",raw_side_effects,flags=re.DOTALL)
        side_effects = re.sub(r"\s[\d]\n","",filtered_side_effects,flags=re.DOTALL)
        side_effects = side_effects.replace('','-')

        return side_effects

#(?i)^(\d.+Possibili effetti indesiderati)([^\d]+)
pdfFileObj = open("D:/Desktop/footer_003827_028245_FI.pdf",'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

data = ''
for i in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(i)
    data += pageObj.extract_text()
pdfFileObj.close()
#(\s[\d]+. Possibili effetti indesiderati).+?(?=(.\n[\d]\.))

#side_effects_pattern = re.compile('[\d]\. Possibili effetti indesiderati(.*?)\.\n[\d]\.',re.DOTALL)
#side_effects = side_effects_pattern.search(data)
#print(side_effects.group(1))

r = re.findall('(?i)[\d]\.\s*possibili effetti indesiderati(.*?)\.\n[\d]\.',data,re.DOTALL)[1]
sub = re.sub(r"Documento reso disponibile da AIFA il \d{2}\/\d{2}\/\d{4}(.*?)\)\.","",r,flags=re.DOTALL)
final = re.sub(r"\s[\d]\n","",sub,flags=re.DOTALL)
#final = re.sub(r'[^\x00-\x7F]+','-', final)
final = final.replace('','-')
#print(final)


