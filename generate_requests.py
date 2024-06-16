import requests

def main(): 
    url = "http://127.0.0.1:8081/predict"
    for i in range(10, 90):
        payload = {
            "building_type_int": 6,
            "latitude": 55.71711349487305,
            "longitude": 37.78112030029297,
            "ceiling_height": 2.640000104904175,
            "flats_count": 84,
            "floors_total": 12,
            "has_elevator": True,
            "floor": 9,
            "kitchen_area": 9.899999618530272+i,
            "living_area": 19.899999618530277+i,
            "rooms": 1,
            "is_apartment": False,
            "total_area": 35.099998474121094+i,
            "build_year": 1965+i
        }

        response = requests.post(url, json=payload)
        print(response.json())

if __name__ == "__main__":
    main()