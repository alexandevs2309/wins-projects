import os
import re
import json
import urllib.request
from dateutil.parser import parse
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime


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
    except Exception as e:
        print(f"Error cargando HTML: {e}")
        return []

    return games_blocks

# Scraping y filtrado de loterías (función centralizada)
def scraping(search_date=None, search_lottery=None):
    data = load_lottery_json()
    loteries_parser = []

    if search_lottery:
        data = [item for item in data if search_lottery.lower() in item["name"].lower()]

    if len(data) == 0:
        return []

    games_blocks = load_html(search_date)

    for game_block in games_blocks:
        block = {}
        try:
            # Extraer y normalizar la fecha
            raw_date = game_block.find("div", "session-date").getText().strip()
            current_year = datetime.now().year

            # Validar y normalizar el formato de la fecha
            if raw_date.lower() == "no sorteo hoy":
                block['date'] = None  
                return "No Sorteo Hoy"
                # O un valor adecuado para "No Sorteo Hoy"
            elif re.match(r"^\d{1,2}-\d{1,2}$", raw_date):  # dd-mm (sin año)
                normalized_date = f"{raw_date}-{current_year}"  # Añadir el año actual
            elif re.match(r"^\d{1,2}-\d{1,2}-\d{4}$", raw_date):  # dd-mm-yyyy (con año)
                normalized_date = raw_date
            else:
                print(f"Formato de fecha inválido: {raw_date}")
                continue  # Si el formato no es válido, se omite este bloque

            # Intentar procesar la fecha
            try:
                block['date'] = parse(normalized_date, dayfirst=True).strftime("%d-%m-%Y")
            except Exception as e:
                print(f"Error al procesar la fecha '{normalized_date}': {e}")
                continue  # Si hay error en la fecha, omite el bloque

            # Continuar con el procesamiento del bloque (como ya lo tenías)
            title = game_block.find("a", "game-title").getText().strip().lower()
            filtered_data = [item for item in data if item["name"].lower() == title]
            if len(filtered_data) == 0:
                continue

            block['id'] = filtered_data[0].get("id", 0)
            block['name'] = filtered_data[0].get("name", "Desconocido")
            block['number'] = "-".join(span.text.strip() for span in game_block.find_all("span", "score"))

            img_tag = game_block.find("img", class_="lazy")
            block['image_url'] = img_tag['data-src'] if img_tag else None

            # Extraer números principales
            numeros_tags = game_block.find_all("span", class_="score")
            numeros = [tag.text.strip() for tag in numeros_tags]
            block['primero'] = numeros[0] if len(numeros) > 0 else None
            block['segundo'] = numeros[1] if len(numeros) > 1 else None
            block['tercero'] = numeros[2] if len(numeros) > 2 else None

            # Extraer información del título
            title_tag = game_block.find("a", class_="game-title")
            if title_tag:
                titulo = title_tag.text.strip()
                block['titulo'] = titulo

                # Extraer la hora del título
                match = re.search(r"(\d{2}:\d{2})", titulo)
                if match:
                    hora = match.group(1)
                    hora_numero = int(hora.split(":")[0])
                    if hora_numero >= 0 and hora_numero < 12:
                        block['horario_abreviatura'] = "M"
                    elif hora_numero >= 12 and hora_numero < 18:
                        block['horario_abreviatura'] = "T"
                    else:
                        block['horario_abreviatura'] = "N"
                else:
                    block['horario_abreviatura'] = None
            else:
                block['titulo'] = None
                block['horario_abreviatura'] = None

            loteries_parser.append(block)
        except Exception as e:
            print(f"Error procesando bloque: {e}")

    # Eliminar duplicados y ordenar resultados
    unique_data = {item['id']: item for item in loteries_parser}.values()

    # Ordenar por fecha y hora, manejando los valores None
    return sorted(unique_data, key=lambda k: k.get("datetime", datetime.min), reverse=True)
# Función para devolver respuesta JSON o XML (centralizada)
def get_response(request, data):
    accept_type = request.headers.get('Accept', 'application/json')

    if 'application/json' in accept_type:
        return JsonResponse(data, safe=False)
    elif 'application/xml' in accept_type:
        root = ET.Element("lotteries")
        for lottery in data:
            lottery_element = ET.SubElement(root, "lottery")
            ET.SubElement(lottery_element, "id").text = str(lottery['id'])
            ET.SubElement(lottery_element, "name").text = lottery['name']
        return HttpResponse(ET.tostring(root, encoding='unicode'), content_type='application/xml')
    return HttpResponse(status=415)

# Vista principal para obtener las loterías
def get_lottery(request):
    lotteries = load_lottery_json()
    return get_response(request, lotteries)

# Vista para buscar una lotería por fecha
def search_lottery(request):
    search_date = request.GET.get('date', datetime.now().strftime("%d-%m-%Y"))
    data = scraping(search_date)
    return get_response(request, data)

# Vista para buscar una lotería por nombre
def search_lottery_by_name(request):
    search_query = request.GET.get('name', None)
    search_date = request.GET.get('date', datetime.now().strftime("%d-%m-%Y"))

    if not search_query:
        return JsonResponse({"error": "Missing 'name' parameter"}, status=400)

    data = scraping(search_date, search_query)
    return get_response(request, data)

# Vista para premios del día
def premios_hoy(request):
    today = datetime.now().strftime("%d-%m-%Y")
    data = scraping(search_date=today)
    return get_response(request, data)

# Vista para datos de loterías
def loteria_data(request):
    data = load_lottery_json()
    return get_response(request, data)

# Vista para todos los resultados
def lotteries(request):
    data = scraping()
    return get_response(request, data)
