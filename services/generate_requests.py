import requests
import random


def main(): 
    url = "http://127.0.0.1:8081/predict"
    for i in range(10, 90):
        random_value = random.randint(1, 90)
        print(random_value)
        payload = {
            "building_type_int": 6,
            "latitude": 55.71711349487305,
            "longitude": 37.78112030029297,
            "ceiling_height": 2.640000104904175,
            "flats_count": 84,
            "floors_total": 12,
            "has_elevator": True,
            "floor": 9,
            "kitchen_area": 9.899999618530272 + random_value,
            "living_area": 19.899999618530277 + random_value,
            "rooms": 1,
            "is_apartment": False,
            "total_area": 35.099998474121094 + random_value,
            "build_year": 1965 + random_value
        }

        response = requests.post(url, json=payload)
        print(response.json())

if __name__ == "__main__":
    main()
