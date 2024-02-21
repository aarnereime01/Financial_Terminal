import requests

def yahoo_api_request(url: str, query_params: dict):
    headers = {
        'Postman-Token': '',
        'Host': 'query1.finance.yahoo.com',
        'User-Agent': 'PostmanRuntime/7.36.1',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None