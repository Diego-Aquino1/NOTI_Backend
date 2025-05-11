from models.inc_incidents import IncIncident  # Asegúrate que el path sea correcto
from sqlmodel.ext.asyncio.session import AsyncSession

import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import time
import re
import googlemaps

url_base = "https://www.seal.com.pe/clientes/SitePages/Cortes.aspx"

# Reemplaza 'TU_CLAVE_API' con tu clave de Google Maps
gmaps = googlemaps.Client(key='AIzaSyCMo4rIxqVHcu1ZlU977Mc_VMEtH-1Jkdg')

def obtener_detalles(url_completa, titulo):
    try:
        response_detalle = requests.get(url_completa, timeout=10)
        if response_detalle.status_code == 200:
            soup_detalle = BeautifulSoup(response_detalle.text, 'html.parser')
            tabla = soup_detalle.find('table', class_='ms-formtable')
            
            if tabla:
                filas = tabla.find_all('tr')
                datos_corte = {}
                for fila in filas:
                    celdas = fila.find_all('td')
                    if len(celdas) > 1:
                        label = celdas[0].get_text(strip=True)
                        valor = celdas[1].get_text(strip=True)
                        datos_corte[label] = valor
                return {'titulo': titulo, 'url': url_completa, 'detalles': datos_corte}
            else:
                return {'titulo': titulo, 'url': url_completa, 'detalles': "No se encontró la tabla."}
        else:
            return {'titulo': titulo, 'url': url_completa, 'detalles': f"Error al acceder a la URL: {response_detalle.status_code}"}
    except Exception as e:
        return {'titulo': titulo, 'url': url_completa, 'detalles': f"Error: {e}"}

def extraer_distrito_y_urbanizaciones(descripcion):
    """Extrae el distrito y las urbanizaciones/manzanas de la descripción."""
    zonas = re.search(r"Zonas afectadas: (.+?)(?:\. Subestaciones|\.$)", descripcion, re.DOTALL)
    if not zonas:
        #print(f"No se encontró 'Zonas afectadas' en: {descripcion}")
        return []
    
    texto_zonas = zonas.group(1).replace('\r\n', ' ').strip()
    distritos_y_urbs = []

    # Normalizar texto para evitar problemas con espacios o codificación
    texto_zonas = ' '.join(texto_zonas.split())

    # Patrón principal para "Urbanizaciones del distrito de X: Y"
    pattern_principal = r"Urbanizaciones del distrito de ([A-Za-z\s]+): ([^.]*)"
    matches_principal = re.finditer(pattern_principal, texto_zonas)
    
    for match in matches_principal:
        distrito = match.group(1).strip()
        urbs_text = match.group(2).strip()
        urbanizaciones = [urb.strip() for urb in urbs_text.split(',') if urb.strip()]
        distritos_y_urbs.append((distrito, urbanizaciones))
        #print(f"Encontrado: {distrito} -> {urbanizaciones}")

    # Si no hay coincidencias, buscar formatos alternativos
    if not distritos_y_urbs:
        # Patrón para manzanas
        pattern_manzanas = r"Mz\.\s*([A-Za-z-Ññ\s]+)\s*(?:de\s+Urb\.\s*([A-Za-z\s]+))?\s*(?:\((?:Distrito de )?([A-Za-z\s]+)\))?"
        matches_manzanas = re.finditer(pattern_manzanas, texto_zonas)
        
        for match in matches_manzanas:
            manzanas = match.group(1).strip()
            urb = match.group(2).strip() if match.group(2) else "No especificada"
            distrito = match.group(3).strip() if match.group(3) else None
            if distrito:
                urbanizaciones = [f"Mz. {manzana} de Urb. {urb}" for manzana in manzanas.split('-')]
                distritos_y_urbs.append((distrito, urbanizaciones))
                #print(f"Encontrado (manzanas): {distrito} -> {urbanizaciones}")

        # Patrón simple para distritos sin urbanizaciones específicas
        if not distritos_y_urbs:
            pattern_distrito_simple = r"(?:Distrito de )?([A-Za-z\s]+)(?:[:,]|\s|$)"
            matches_distrito = re.finditer(pattern_distrito_simple, texto_zonas)
            for match in matches_distrito:
                distrito = match.group(1).strip()
                # Evitar falsos positivos como "Subestaciones"
                if not any(x in distrito.lower() for x in ["subestaciones", "eléctricas", "sed"]):
                    distritos_y_urbs.append((distrito, ["Zona general"]))
                    #print(f"Encontrado (simple): {distrito} -> ['Zona general']")

    if not distritos_y_urbs:
        print(f"No se pudo extraer distrito/urbanización de: {texto_zonas}")

    return distritos_y_urbs

def obtener_coordenadas(urbanizacion, distrito):
    """Obtiene las coordenadas usando Google Maps Geocoding API."""
    direccion = f"{urbanizacion}, {distrito}, Perú"
    try:
        geocode_result = gmaps.geocode(direccion)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return {"latitude": str(location['lat']), "longitude": str(location['lng'])}
        else:
            print(f"No se encontraron coordenadas exactas para {direccion}. Usando coordenadas del distrito.")
            # Fallback: buscar solo el distrito
            geocode_result = gmaps.geocode(f"{distrito}, Perú")
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return {"latitude": str(location['lat']), "longitude": str(location['lng'])}
            else:
                return {"latitude": "No disponible", "longitude": "No disponible"}
    except Exception as e:
        #print(f"Error al obtener coordenadas para {direccion}: {e}")
        return {"latitude": "No disponible", "longitude": "No disponible"}

def transformar_datos(datos_corte):
    """Transforma los datos al formato JSON deseado."""
    detalles = datos_corte['detalles']
    descripcion = detalles.get('Descripción', 'Sin descripción')
    start_time = detalles.get('Hora de inicio', '')
    end_time = detalles.get('Hora de finalización', '')
    type_id_original = detalles.get('Título', 'Sin tipo')  # Usar 'titulo' en lugar de 'Título'
    url = datos_corte['url']

    contiene_suspendido = "SUSPENDIDO" in type_id_original.upper()

    type_id = type_id_original.upper().replace("SUSPENDIDO", "").strip().rstrip('.')
    
    # Extraer distritos y urbanizaciones
    distritos_y_urbanizaciones = extraer_distrito_y_urbanizaciones(descripcion)
    
    # Obtener coordenadas para cada urbanización
    addresses = []
    if distritos_y_urbanizaciones:
        for distrito, urbanizaciones in distritos_y_urbanizaciones:
            for urb in urbanizaciones:
                coords = obtener_coordenadas(urb, distrito)
                addresses.append({
                    "address": f"{urb}, {distrito}",
                    "longitude": coords["longitude"],
                    "latitude": coords["latitude"]
                })
    else:
        #print(f"No se encontraron distritos/urbanizaciones para: {descripcion}")
        addresses.append({
            "address": "Zona no especificada",
            "longitude": "No disponible",
            "latitude": "No disponible"
        })
    
    return {
        "start_time": start_time,
        "end_time": end_time,
        "description": descripcion.replace('\r\n', ' ').strip(),
        "type_id": type_id,
        "suspendido": 1 if contiene_suspendido else 0,  # <- columna nueva
        "addresses": addresses,
        "url": url
    }

async def obtener_cortes(session: AsyncSession):
    #start_time = time.time()  
    response = requests.get(url_base, timeout=10)
    resultado = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        contenedor = soup.find('div', {'id': 'MSOZoneCell_WebPartWPQ3'})

        if contenedor:
            enlaces = contenedor.find_all('a', title=True)
            datos = []

            with ThreadPoolExecutor(max_workers=5) as executor:
                futuros = []
                for enlace in enlaces:
                    titulo = enlace['title']
                    url_completa = requests.compat.urljoin(url_base, enlace['href'])
                    futuros.append(executor.submit(obtener_detalles, url_completa, titulo))

                for futuro in futuros:
                    datos.append(futuro.result())

            # Transformar los datos al formato deseado
            for dato in datos:
                if isinstance(dato.get('detalles'), dict):
                    resultado.append(transformar_datos(dato))

        else:
            print("No se encontró el contenedor con id 'MSOZoneCell_WebPartWPQ3'.")
    else:
        print(f"Error al acceder a la página. Código de estado: {response.status_code}")

    #end_time = time.time()  
    #execution_time = end_time - start_time  
    #print(f"Tiempo de ejecución: {execution_time} segundos")
    #return resultado


    for dato in resultado:  # Asegúrate que `datos_scrapeados` exista
        corte = IncIncident(
            start_time = dato["start_time"],
            end_time = dato["end_time"],
            description = dato["description"],
            type_id = dato["type_id"],
            suspendido = dato["suspendido"],
            addresses = dato["addresses"],
            url = dato["url"]
        )
        session.add(corte)

    await session.commit()
    return resultado

# Guardar los datos en un archivo JSON
def guardar_en_json(data, filename='resultados_webscraping_test2.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Los datos han sido guardados en el archivo {filename}.")
    except Exception as e:
        print(f"Error al guardar los datos en el archivo JSON: {e}")

# Ejecución
if __name__ == "__main__":
    resultado = obtener_cortes()
    
    #guardar_en_json(resultado)
    print("Los datos han sido procesados y guardados en 'resultados_webscraping.json'.")