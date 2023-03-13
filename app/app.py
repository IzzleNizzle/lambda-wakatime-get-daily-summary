import os
from datetime import datetime, timedelta
import json
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
WAKATIME_API_KEY = os.environ.get("WAKATIME_API_KEY")


def lambda_handler(event, context):
    start_date, end_date = get_7_day_range(datetime.now())

    data = wakatime_api_get_summary(start_date, end_date)

    weekly_total = data["cumulative_total"]["text"]
    weekly_total_seconds = data["cumulative_total"]["seconds"]
    daily_average = data["daily_average"]["text"]
    daily_average_seconds = data["daily_average"]["seconds"]

    post_response = notion_api_create_db_page(
        start_date,
        end_date,
        weekly_total,
        weekly_total_seconds,
        daily_average,
        daily_average_seconds,
    )
    response_json = {
        "statusCode": post_response.status_code,
        "body": post_response.text,
    }
    print(response_json)
    return response_json


def get_7_day_range(end_date):
    date_format = "%Y-%m-%d"
    start_date = end_date - timedelta(days=7)
    return start_date.strftime(date_format), end_date.strftime(date_format)


def wakatime_api_get_summary(start_date, end_date):
    url = f"https://wakatime.com/api/v1/users/current/summaries?start={start_date}&end={end_date}&api_key={WAKATIME_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data


def notion_api_create_db_page(
    start_date,
    end_date,
    weekly_total,
    weekly_total_seconds,
    daily_average,
    daily_average_seconds,
):
    post_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "icon": {"emoji": "🧑‍💻"},
        "properties": {
            "Name": {"title": [{"text": {"content": f"{start_date} to {end_date}"}}]},
            "Weekly Total": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": weekly_total, "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": weekly_total,
                        "href": None,
                    },
                ]
            },
            "Weekly Total (seconds)": {"number": weekly_total_seconds},
            "Daily Average": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": daily_average, "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": daily_average,
                        "href": None,
                    },
                ]
            },
            "Daily Average (seconds)": {"number": daily_average_seconds},
            "Date": {"date": {"start": end_date}},
        },
    }
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    post_response = requests.post(
        "https://api.notion.com/v1/pages",
        data=json.dumps(post_data),
        headers=headers,
    )
    return post_response


if __name__ == "__main__":
    lambda_handler("event", "context")
