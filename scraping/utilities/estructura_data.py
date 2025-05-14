from models.inc_incidents import IncIncident, IncIncidentAddress, GeoLocation
from sqlmodel.ext.asyncio.session import AsyncSession
import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import time
import re
import googlemaps
from datetime import datetime

url_base = "https://www.seal.com.pe/clientes/SitePages/Cortes.aspx"
gmaps = googlemaps.Client(key='AIzaSyCQ8rlV8W0vpEOAgWZaZWl2_Abrcp2hrQo')

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
    zonas = re.search(r"Zonas afectadas: (.+?)(?:\. Subestaciones|\.$)", descripcion, re.DOTALL)
    if not zonas:
        return []
    
    texto_zonas = zonas.group(1).replace('\r\n', ' ').strip()
    distritos_y_urbs = []
    texto_zonas = ' '.join(texto_zonas.split())

    pattern_principal = r"Urbanizaciones del distrito de ([A-Za-z\s]+): ([^.]*)"
    matches_principal = re.finditer(pattern_principal, texto_zonas)
    
    for match in matches_principal:
        distrito = match.group(1).strip()
        urbs_text = match.group(2).strip()
        urbanizaciones = [urb.strip() for urb in urbs_text.split(',') if urb.strip()]
        distritos_y_urbs.append((distrito, urbanizaciones))

    if not distritos_y_urbs:
        pattern_manzanas = r"Mz\.\s*([A-Za-z-Ññ\s]+)\s*(?:de\s+Urb\.\s*([A-Za-z\s]+))?\s*(?:\((?:Distrito de )?([A-Za-z\s]+)\))?"
        matches_manzanas = re.finditer(pattern_manzanas, texto_zonas)
        
        for match in matches_manzanas:
            manzanas = match.group(1).strip()
            urb = match.group(2).strip() if match.group(2) else "No especificada"
            distrito = match.group(3).strip() if match.group(3) else None
            if distrito:
                urbanizaciones = [f"Mz. {manzana} de Urb. {urb}" for manzana in manzanas.split('-')]
                distritos_y_urbs.append((distrito, urbanizaciones))

        if not distritos_y_urbs:
            pattern_distrito_simple = r"(?:Distrito de )?([A-Za-z\s]+)(?:[:,]|\s|$)"
            matches_distrito = re.finditer(pattern_distrito_simple, texto_zonas)
            for match in matches_distrito:
                distrito = match.group(1).strip()
                if not any(x in distrito.lower() for x in ["subestaciones", "eléctricas", "sed"]):
                    distritos_y_urbs.append((distrito, ["Zona general"]))

    return distritos_y_urbs

def obtener_coordenadas(urbanizacion, distrito):
    direccion = f"{urbanizacion}, {distrito}, Perú"
    try:
        geocode_result = gmaps.geocode(direccion)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return {
                "latitude": location['lat'],
                "longitude": location['lng'],
                "address": direccion,
                "city": distrito,
                "country": "Perú"
            }
        else:
            geocode_result = gmaps.geocode(f"{distrito}, Perú")
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return {
                    "latitude": location['lat'],
                    "longitude": location['lng'],
                    "address": f"{distrito}, Perú",
                    "city": distrito,
                    "country": "Perú"
                }
            else:
                return None
    except Exception as e:
        return None

def transformar_datos(datos_corte):
    detalles = datos_corte['detalles']
    descripcion = detalles.get('Descripción', 'Sin descripción')
    start_time = detalles.get('Hora de inicio', '')
    end_time = detalles.get('Hora de finalización', '')
    type_id_original = datos_corte.get('titulo', 'Sin tipo')
    url = datos_corte['url']

    contiene_suspendido = "SUSPENDIDO" in type_id_original.upper()
    
    # Extraer solo el tipo de incidente (después de las fechas)
    type_id_match = re.search(r'\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}\s*-\s*\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}\s+(.+)', type_id_original, re.IGNORECASE)
    if type_id_match:
        type_id = type_id_match.group(1).upper().replace("SUSPENDIDO", "").strip().rstrip('.')
    else:
        type_id = type_id_original.upper().replace("SUSPENDIDO", "").strip().rstrip('.')

    # Convertir fechas a datetime (ajusta el formato según los datos)
    try:
        start_time = datetime.strptime(start_time, '%d/%m/%Y %H:%M') if start_time else datetime.now()
        end_time = datetime.strptime(end_time, '%d/%m/%Y %H:%M') if end_time else datetime.now()
    except ValueError:
        start_time = datetime.now()
        end_time = datetime.now()

    # Extraer distritos y urbanizaciones
    distritos_y_urbanizaciones = extraer_distrito_y_urbanizaciones(descripcion)
    
    # Obtener coordenadas para cada urbanización
    locations = []
    if distritos_y_urbanizaciones:
        for distrito, urbanizaciones in distritos_y_urbanizaciones:
            for urb in urbanizaciones:
                coords = obtener_coordenadas(urb, distrito)
                if coords:
                    locations.append(coords)
    else:
        locations.append({
            "latitude": 0.0,
            "longitude": 0.0,
            "address": "Zona no especificada",
            "city": None,
            "country": None
        })
    
    return {
        "title": datos_corte['titulo'],
        "start_time": start_time,
        "end_time": end_time,
        "description": descripcion.replace('\r\n', ' ').strip(),
        "type_id": type_id,
        "suspendido": contiene_suspendido,
        "locations": locations,
        "url": url
    }

async def obtener_cortes(session: AsyncSession):
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

            for dato in datos:
                if isinstance(dato.get('detalles'), dict):
                    transformed = transformar_datos(dato)
                    resultado.append(transformed)

                    # Guardar en la base de datos
                    incident = IncIncident(
                        start_time=transformed["start_time"],
                        end_time=transformed["end_time"],
                        description=transformed["description"],
                        type_id=transformed["type_id"],
                        suspendido=transformed["suspendido"],
                        url=transformed["url"]
                    )
                    session.add(incident)
                    await session.commit()
                    await session.refresh(incident)

                    # Guardar ubicaciones
                    for loc in transformed["locations"]:
                        if loc["latitude"] != 0.0 and loc["longitude"] != 0.0:
                            location = GeoLocation(
                                name=loc["address"],
                                latitude=loc["latitude"],
                                longitude=loc["longitude"],
                                city=loc["city"],
                                country=loc["country"],
                                address=loc["address"]
                            )
                            session.add(location)
                            await session.commit()
                            await session.refresh(location)

                            # Relacionar incidente con ubicación
                            incident_address = IncIncidentAddress(
                                incident_id=incident.id,
                                location_id=location.id
                            )
                            session.add(incident_address)
                    await session.commit()
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
            title = dato["title"],
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

def guardar_en_json(data, filename='resultados_webscraping_test2.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Los datos han sido guardados en el archivo {filename}.")
    except Exception as e:
        print(f"Error al guardar los datos en el archivo JSON: {e}")

if __name__ == "__main__":
    import asyncio
    from sqlmodel import create_engine, SQLModel
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as AsyncSessionBase

    # Configura la base de datos
    DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/noti"
    engine = create_async_engine(DATABASE_URL, echo=True)

    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def main():
        await init_db()
        async with AsyncSessionBase(engine) as session:
            resultado = await obtener_cortes(session)
            guardar_en_json(resultado)

    asyncio.run(main())