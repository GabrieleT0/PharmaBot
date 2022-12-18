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