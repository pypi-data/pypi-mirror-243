import requests
import json
class WriterWrapper:
    def complete(self, prompt):
        url = "https://enterprise-api.qordobadev.com/llm/organization/7532/model/palmyra-x/completions"
        headers = {
            "Authorization": "Bearer xxxxxx",
            "accept": "application/json",
            "content-type": "application/json",
        }

        data = {
            "prompt":prompt,
            "maxTokens": 1000,
        }

        # Convert the data to JSON format
        json_data = json.dumps(data)

        response = requests.post(url, headers=headers, data=json_data)

        return response.json()