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
    