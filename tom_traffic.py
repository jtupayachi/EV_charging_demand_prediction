import requests
import xmltodict
import json

def get_traffic_data(api_key, latitude, longitude):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/xml?key={api_key}&point={latitude},{longitude}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"

def xml_to_json(xml_data):
    dict_data = xmltodict.parse(xml_data)
    json_data = json.dumps(dict_data, indent=4)
    return json_data

# Replace with your actual API key and coordinates
api_key = "dd6AR99b85lX9OsHf4UPEgTjyQYBVddA"
latitude = 52.41072
longitude = 4.84239

# Fetch traffic data
traffic_data_xml = get_traffic_data(api_key, latitude, longitude)

# Convert XML to JSON
if "Error" not in traffic_data_xml:
    traffic_data_json = xml_to_json(traffic_data_xml)
    print(traffic_data_json)
else:
    print(traffic_data_xml)