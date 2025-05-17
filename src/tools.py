import requests

def geocode(location: str):
    headers = {
        "User-Agent": "MyGeolocationApp/1.0 (UMA: Big Data & AI)"
    }
    endpoint = "https://nominatim.openstreetmap.org/search"
    params = {"q": location, "format": "json"}

    response = requests.get(endpoint, params=params, headers=headers)

    if response.ok:
        data = response.json()
        if not data:
            return {"location": location, "error": "No se encontraron resultados"}

        top_result = data[0]
        return {
            "location": location,
            "latitude": top_result.get("lat"),
            "longitude": top_result.get("lon"),
            "display_name": top_result.get("display_name")
        }
    else:
        return {"location": location, "error": "Falló la petición"}
