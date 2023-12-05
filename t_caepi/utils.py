import requests
from bs4 import BeautifulSoup
import re

def get_url_download(ca: str) -> str:
    ca = str(ca)
    # Endpoint para onde a requisição será enviada
    url = 'https://consultaca.com/TypeaheadJson.aspx'

    payload = {
        'q': ca,  
        't': '1'     
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://consultaca.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.post(url, data=payload)

    if response.status_code == 200:
        try:
            data = response.json()[0]
            url = data['url']
            return url, data
        except ValueError as e:
            print(f'Erro na decodificação do JSON: {e}')
            print(f'Resposta bruta: {response.text}')
    else:
        print(f'Falha na requisição: Status code {response.status_code}')
        


def download_certificado(ca: str):
    login_page_url = 'https://consultaca.com/logon'
    login_url = 'https://consultaca.com/logon'

    session = requests.Session()

    response = session.get(login_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    viewstate = soup.select_one('#__VIEWSTATE')['value']
    eventvalidation = soup.select_one('#__EVENTVALIDATION')['value']

    login_data = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btnLogon',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__EVENTVALIDATION': eventvalidation,
        'searchType': '1',
        'typeaheadSearch[query]': '',
        'ctl00$ContentPlaceHolder1$txtEmailLogon': 'fabio5489b@gmail.com',
        'ctl00$ContentPlaceHolder1$txtSenhaLogon': 'sEPHINX123',
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 ...',  
    }

    response = session.post(login_url, headers=headers, data=login_data)

    if response.status_code == 200 or response.status_code == 302:   
        url, data = get_url_download(ca=ca)

        pdf_page_url = f'https://consultaca.com/{url}'
        response = session.get(pdf_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        viewstate = soup.select_one('#__VIEWSTATE')['value']
        eventvalidation = soup.select_one('#__EVENTVALIDATION')['value']
        viewstategenerator = soup.select_one('#__VIEWSTATEGENERATOR')['value']

        pdf_payload = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$hlkSalvarCertificado',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            'ctl00$cboOpcoesUsuario': 'FABIO',
            'searchType': '1',
        }

        response = session.post(pdf_page_url, headers=headers, data=pdf_payload)

        numeros = re.findall(r'\d+', url)
        nome_arquivo = ''.join(numeros)
        if response.status_code == 200:
            return response.content, data
        else:
            print("Falha na requisição.")
            print(f'Status code: {response.status_code}')

    else:
        print("Login falhou.")
        print(f'Status code: {response.status_code}')
        print(f'Resposta: {response.text}')
