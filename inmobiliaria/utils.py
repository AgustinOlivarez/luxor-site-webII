import requests
def clasificar_categoria(mensaje):
    mensaje = mensaje.lower()

    if any(palabra in mensaje for palabra in ["precio", "costo", "tarifa", "compra"]):
        return "Consulta Comercial"

    if any(palabra in mensaje for palabra in ["soporte", "error", "problema", "ayuda"]):
        return "Consulta Técnica"

    if any(palabra in mensaje for palabra in ["trabajo", "cv", "empleo", "linkedin"]):
        return "Consulta de RRHH"

    return "Consulta General"

def obtener_novedades_externas():
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Tomamos 6 como "novedades"
        novedades = data[:6]

        resultado = [
            {
                "titulo": item["title"],
                "descripcion": item["body"]
            }
            for item in novedades
        ]

        return resultado

    except requests.exceptions.RequestException:
        return []
