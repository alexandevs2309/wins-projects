import os
import json
import datetime
import urllib.request
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Cargar el archivo JSON de loterías (función centralizada)
def load_lottery_json():
    lottery_file_path = os.path.join(settings.BASE_DIR, 'static', 'lottery.json')
    with open(lottery_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Cargar HTML (scraping)
def load_html(search_date=None):
    url1 = "https://loteriasdominicanas.com/"
    url2 = "https://loteriasdominicanas.com/anguila"

    if search_date:
        url1 += f"?date={search_date}"
        url2 += f"?date={search_date}"

    games_blocks = []
    try:
        html1 = urllib.request.urlopen(url1).read()
        html2 = urllib.request.urlopen(url2).read()

        soup1 = BeautifulSoup(html1, "html.parser")
        soup2 = BeautifulSoup(html2, "html.parser")

        blocks1 = soup1.find_all("div", class_="game-block")
        games_blocks.extend(blocks1)

        blocks2 = soup2.find_all("div", class_="game-block")
        games_blocks.extend(blocks2)
    except:
        return []

    return games_blocks

# Scraping y filtrado de loterías (función centralizada)
def scraping(search_date=None, search_lotery=None):
    data = load_lottery_json()
    loteries_parser = []
    
    if search_lotery:
        data = [item for item in data if search_lotery.lower() in item["name"].lower()]

    if len(data) == 0:
        return []

    games_blocks = load_html(search_date)

    for game_block in games_blocks:
        block = {}
        title = game_block.find("a", "game-title").getText().strip().lower()

        filtered_data = [item for item in data if item["name"].lower() == title]
        if len(filtered_data) == 0:
            continue

        pather_score = game_block.find_all("span", "score")
        pather_date = game_block.find("div", "session-date").getText().strip()
        score = "-".join(span.text.strip() for span in pather_score)

        block['id'] = filtered_data[0]["id"]
        block['name'] = filtered_data[0]["name"]
        block['date'] = pather_date
        block['number'] = score
        loteries_parser.append(block)

       
        img_tag = game_block.find("img", class_="lazy") 
        if img_tag:
            block['image_url'] = img_tag['data-src'] 
        else:
            block['image_url'] = None  


    return sorted(loteries_parser, key=lambda k: k["id"])

# Función para devolver respuesta JSON o XML (centralizada)
def get_response(request, data):
    accept_type = request.headers.get('Accept', 'application/json')

    # Devolver JSON
    if 'application/json' in accept_type:
        return JsonResponse(data, safe=False)

    # Devolver XML
    elif 'application/xml' in accept_type:
        root = ET.Element("lotteries")
        for lottery in data:
            lottery_element = ET.SubElement(root, "lottery")
            id_element = ET.SubElement(lottery_element, "id")
            id_element.text = str(lottery['id'])
            name_element = ET.SubElement(lottery_element, "name")
            name_element.text = lottery['name']

        return HttpResponse(ET.tostring(root, encoding='unicode'), content_type='application/xml')

    # Caso por defecto
    return HttpResponse(status=415)

# Vista principal para obtener las loterías
def get_lottery(request):
    lotteries = load_lottery_json()
    return get_response(request, lotteries)

# Vista para buscar una lotería por nombre
def search_lottery(request):
    search_date = request.GET.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))
    data = scraping(search_date)
    return get_response(request, data)

# Vista para buscar una lotería por nombre con parámetro 'name'
def search_lottery_by_name(request):
    search_query = request.GET.get('name', None)
    search_date = request.GET.get('date', datetime.datetime.now().strftime("%d-%m-%Y"))

    if not search_query:
        return JsonResponse({"error": "Missing 'name' parameter"}, status=400)

    data = scraping(search_date, search_query)
    return get_response(request, data)


def premios_hoy(request):
    """Obtiene los premios de hoy."""
    
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    data = scraping(search_date=today)  # Usamos tu función scraping
    return get_response(request, data)  # Usamos tu función get_response


def loteria_data(request):
    """Devuelve la información de las loterías."""
    
    data = load_lottery_json()  # Usamos tu función load_lottery_json
    return get_response(request, data)  # Usamos tu función get_response


def lotteries(request):
    """Devuelve todos los resultados de las loterías."""
    
    data = scraping()  # Usamos tu función scraping sin argumentos
    return get_response(request, data)  # Usamos tu función get_response