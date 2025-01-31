import os
import requests

from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.typing import LambdaContext

# NOTION_API_TOKEN = os.environ['NOTION_API_TOKEN']
notion_secret:dict = parameters.get_secret(os.environ['NOTION_SECRETS'], transform='json')

NOTION_API_TOKEN = notion_secret.get('token')
NOTION_DATABASE_ID = notion_secret.get('database_id')


NOTION_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

def get_to_notion():
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "filter": {
            "property": "マルチセレクト",
            "multi_select": {
                "contains": "未読"
            }
        }
    }

    response = requests.post(NOTION_URL, headers=headers, json=payload)
    return response

def lambda_handler(event: dict, context: LambdaContext):

    # Notionに情報を登録
    response = get_to_notion()

    # レスポンスの処理
    if response.status_code == 200:
        data = response.json()
        return {
            "statusCode": 200,
            "body": data
        }
    else:
        return {
            "statusCode": response.status_code,
            "error": response.text
        }
    