import os
import requests
import json

CATEGORY_API_URL = "https://www.selver.ee/api/catalog/vue_storefront_catalog_et/category/_search"


def get_categorys_and_ids():

    with open(os.path.join(os.getcwd(), "src/selver/category_request.json"), "r", encoding="UTF-8") as file:
        request = file.read()
        request = request.replace(" ", "").replace("\n", "")

        response = requests.get(
            CATEGORY_API_URL + "?request=" + request + "&size=4000")
        response = json.loads(response.text)

        ids_and_categorys = [
            [
                int(category["_source"]["path"].split("/")[-1]),
                category["_source"]["name"]
            ] for category in response["hits"]["hits"]
        ]

        return ids_and_categorys
