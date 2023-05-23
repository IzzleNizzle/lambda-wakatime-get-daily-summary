import os
from datetime import datetime, timedelta
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
WAKATIME_API_KEY = os.environ.get("WAKATIME_API_KEY")
CREDENTIALS_FILE = os.environ.get("CREDENTIALS_FILE")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
SHEET_RANGE = os.environ.get("SHEET_RANGE")


def lambda_handler(event, context):
    start_date, end_date = get_7_day_range(datetime.now())

    data = wakatime_api_get_summary(start_date, end_date)

    weekly_total = data["cumulative_total"]["text"]
    weekly_total_seconds = data["cumulative_total"]["seconds"]
    daily_average = data["daily_average"]["text"]
    daily_average_seconds = data["daily_average"]["seconds"]

    leaderboard_data = wakatime_api_get_leader_rank()
    leaderboard_100_data = wakatime_api_get_leader_rank(leaderboard_page=0)
    user_leaderboard_rank = leaderboard_data["current_user"]["rank"]
    top_100_leaderboard_total = leaderboard_100_data["data"][99]["running_total"][
        "total_seconds"
    ]
    top_100_leaderboard_daily_average = leaderboard_100_data["data"][99][
        "running_total"
    ]["daily_average"]
    top_10_leaderboard_total = leaderboard_100_data["data"][9]["running_total"][
        "total_seconds"
    ]
    top_10_leaderboard_daily_average = leaderboard_100_data["data"][9]["running_total"][
        "daily_average"
    ]

    sheet_values = [
        start_date,
        end_date,
        weekly_total,
        weekly_total_seconds,
        daily_average,
        daily_average_seconds,
        user_leaderboard_rank,
        top_10_leaderboard_total,
        top_10_leaderboard_daily_average,
        top_100_leaderboard_total,
        top_100_leaderboard_daily_average,
    ]

    google_sheet_response = append_values_to_google_sheet(
        SPREADSHEET_ID,
        SHEET_RANGE,
        "USER_ENTERED",
        sheet_values,
    )

    response_json = {
        "statusCode": 200,
        "body": {
            "sheets_api_response": google_sheet_response,
        },
    }
    print(response_json)
    return response_json


def get_7_day_range(end_date):
    date_format = "%Y-%m-%d"
    start_date = end_date - timedelta(days=7)
    return start_date.strftime(date_format), end_date.strftime(date_format)


def wakatime_api_get_summary(start_date, end_date):
    url = (
        f"https://wakatime.com/api/v1/users/current/summaries"
        f"?start={start_date}&end={end_date}&api_key={WAKATIME_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    return data


def wakatime_api_get_leader_rank(leaderboard_page=None):
    url = (
        f"https://wakatime.com/api/v1/leaders"
        f"?country_code=US&api_key={WAKATIME_API_KEY}"
    )
    if leaderboard_page is not None:
        url += f"&page={leaderboard_page}"
    response = requests.get(url)
    data = response.json()
    return data


def append_values_to_google_sheet(
    spreadsheet_id,
    range_name,
    value_input_option,
    values,
):
    if CREDENTIALS_FILE is None:
        raise ValueError("Environment variable not set")
    current_file_path = os.path.abspath(__file__)
    relative_file_path = os.path.join(
        os.path.dirname(current_file_path), CREDENTIALS_FILE
    )
    creds = service_account.Credentials.from_service_account_file(relative_file_path)
    try:
        service = build("sheets", "v4", credentials=creds)
        body = {"values": [values]}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == "__main__":
    lambda_handler("event", "context")
