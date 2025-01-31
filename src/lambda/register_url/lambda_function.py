import json
import os
import requests

from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.typing import LambdaContext

notion_secret:dict = parameters.get_secret(os.environ['NOTION_SECRETS'], transform='json')

NOTION_API_TOKEN = notion_secret.get('token')
NOTION_DATABASE_ID = notion_secret.get('database_id')
NOTION_URL = "https://api.notion.com/v1/pages"

def register_to_notion(title, url):
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "タイトル": {"title": [{"text": {"content": title}}]},
            "URL": {"url": url},
            "マルチセレクト": {"multi_select": [{"name": "未読"}]}
        }
    }
    print(payload)

    response = requests.post(NOTION_URL, headers=headers, json=payload)
    return response

def lambda_handler(event: dict, context: LambdaContext):
    print(event)
    for record in event['Records']:
        try:
            # SQSのBodyをJSONとして解析
            message = json.loads(record['body'])
            url = message['url']
            title = message['title']
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            print(f"Failed to parse message: {record['body']}. Error: {e}")
            continue

        # Notionに情報を登録
        response = register_to_notion(title, url)

        if response.status_code == 200:
            print(f"Successfully registered: {title} ({url})")
        else:
            print(f"Failed to register: {title} ({url}). Response: {response.text}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Messages processed successfully."})
    }