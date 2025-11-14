import requests
import json
from mealie.mealie_base_module import *

base_url = "/api/groups/mealplans"

def get_plan(plan_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.get("{}{}/{}".format(api_url, base_url, plan_id), headers=headers)

    if response.status_code == 200:
        print("\Strumento trovato! - Status Code: {}".format(response.status_code))
        return response.json()
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def get_all_plans(api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    params = {"perPage": 10**4}
    response = requests.get(
        "{}{}".format(api_url, base_url), headers=headers, params=params
    )

    if response.status_code == 200:
        print(
            "\nTrovati {} risultati - Status Code: {}".format(
                response.json()["total"], response.status_code
            )
        )
        return [i for i in response.json()["items"]]
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )


def delete_plan(plan_id, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    response = requests.delete(
        "{}{}/{}".format(api_url, base_url, plan_id), headers=headers
    )

    if response.status_code == 200:
        print("\nEliminato {} - Status Code: {}".format(plan_id, response.status_code))
    else:
        print(
            "\nErrore in fase di eliminazione {} - Status Code: {} - Response: {}".format(
                plan_id, response.status_code, response.text
            )
        )


def create_plan(plan_name, api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    data = {"name": plan_name}

    response = requests.post(
        "{}{}".format(api_url, base_url),
        data=json.dumps(data, ensure_ascii=False),
        headers=headers,
    )

    if response.status_code == 201:
        print(
            "\nplan creato! - Status Code: {}, Response: {}".format(
                response.status_code, response.json()
            )
        )
        return response.json()
    else:
        print(
            "\nErrore in fase di creazione! - Status Code: {}, Response: {}".format(
                response.status_code, response.text
            )
        )


def get_today_plan(api_url=mealie_url, token=api_token):
    headers = get_headers(token)
    params = {"perPage": 10**4}
    response = requests.get(
        "{}{}/today".format(api_url, base_url), headers=headers, params=params
    )

    if response.status_code == 200:
        print(
            "\nTrovati {} risultati - Status Code: {}".format(
                len(response.json()), response.status_code
            )
        )
        return response.json()
    else:
        print(
            "\nErrore in fase di ricerca - Status Code: {} - Response: {}".format(
                response.status_code, response.text
            )
        )
