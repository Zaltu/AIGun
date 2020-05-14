import json
from shotgun_api3 import Shotgun

# If it fails, we want it to crash. AIGIS will handle it.
with open("sg_creds.secret", "r") as SECRET_FILE:
    SECRETS = json.load(SECRET_FILE)

SG = Shotgun(SECRETS["URL"], SECRETS["API_NAME"], SECRETS["API_KEY"])

def fetch(fetch_request):
    """
    Fetch a set of data from the loaded Shotgun connection.
    Test version SKIPS OVER ERRONEOUS REQUESTS.

    :param dict fetch_request: request data in the below format
    {
        "ENTITY_TYPE":
            {
                "filters": SG_FILTERS,
                "return_fields": LIST
            },
        "Asset":
            {
                "filters": [["sg_link.CustomEntity07.code", "is", "Nosferatu"]],
                "return_fields": ["sg_status_list"]
            }
    }
    :returns: loaded data
    :rtype: dict in the below format
    {
        "ENTITY_TYPE":
            [
                SG_DICT
            ]
    }
    """
    return_data = {}

    for entity_type in fetch_request:
        try:
            return_data[entity_type] = SG.find(entity_type, fetch_request[entity_type].get("filters"), fetch_request[entity_type].get("return_fields"))
        except:  # Broad-except for testing
            print("Error processing \n%s" % fetch_request[entity_type])
    
    return return_data