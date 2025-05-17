from geopy.distance import geodesic

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
    You are an helpful asssitant, your goal is to help the user find coordinates
    for the locations they request.

    The output of the tools you call is ALWAYS right

    If the users asks for any other topic, tell him what you can do and do not respond to his question.
    """
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "geocode",
            "description": "A geocoding tool that given location (it must be a city or town)",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to retrieve the coordinates from. It must be the name of the city spelled in caps.",
                    },
                },
                "required": ["location"],
            },
        }
    }
]


def is_far_enough(new_coord, coord_list, threshold_km=2):
    for coord in coord_list:
        dist = geodesic((coord["latitude"], coord["longitude"]), (new_coord["latitude"], new_coord["longitude"])).km
        if dist < threshold_km:
            return False
    return True
