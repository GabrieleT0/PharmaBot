import re
import requests
import bcrypt

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

def get_hashed_pwd(password):
    byte_pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(byte_pwd,salt)

    return pwd_hash.decode()

def check_pwd(password,pwd_hash):
    password = password.encode('utf-8')
    return bcrypt.checkpw(password,pwd_hash)

def medicine_parser(medicine_account):
    if isinstance(medicine_account,list):
                if len(medicine_account) > 0:
                    medicineLi = []
                    for medicine in medicine_account:
                        name = medicine['name']
                        type = medicine['type']
                        grams = medicine['grams']
                        expiration_date = medicine['expirationDate']
                        if type is None:
                            type = ''
                        if grams is None:
                            grams = ''
                        medicine_str = f"{name} {type} {grams} Data scadenza: {expiration_date}"
                        medicineLi.append(medicine_str.strip())
                    return medicineLi
                else:
                    return False
    else:
        return False

def printMedicineLi(medicineLi):
    medicine_str = ''
    for medicine in medicineLi:
        medicine_str += medicine.capitalize() + '\n\n'
    return medicine_str