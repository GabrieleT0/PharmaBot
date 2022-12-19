import re
import requests


def get_pdf_link(links):
    try:
        for link in links:
            response = requests.get(link)
            if response.headers['Content-Type'] == 'application/pdf':
                return link
        return False
    except:
        return False
    
def duplicate_new_line(string):
    str = string.replace('\n•','\n\n•')
    str = str.replace('\n-','\n\n-')
    return str

def clean_data(pdf_data):
    pdf_data = re.sub(r"Documento reso disponibile da AIFA il \d{2}\/\d{2}\/\d{4}(.*?)\)\.","",pdf_data,flags=re.DOTALL)
    pdf_data = re.sub(r"\s[\d]\n","",pdf_data,flags=re.DOTALL)
    pdf_data = re.sub(r"\s?Pagina [\d]+ (diNon nota)","",pdf_data)
    pdf_data = re.sub(r"\s?Pagina [\d]+ (di\s?[\d]+)","",pdf_data)
    pdf_data = pdf_data.replace('','-')

    return pdf_data