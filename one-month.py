import requests
import csv
import time
from datetime import date, timedelta

def fetch_one_news_for_date(target_date: str):
    """
    Fetches a single economic news article from Thailand for a specific date.
    Returns the article or None if not found.
    Returns "STOP" on critical API errors like 401.
    """
    url = "https://api.worldnewsapi.com/search-news"
    api_key = "2df338b8696b4d83aa2a3d0b52197256"

    headers = {'x-api-key': api_key}
    params = {
        'source-countries': 'th',
        'category': 'economics',
        'date': target_date,
        'limit': 1  # Limit the result to one article
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('news') and len(data['news']) > 0:
            return data['news'][0]  # Return the first news article
        return None
    except requests.exceptions.HTTPError as e:
        print(f"API Error on {target_date}: {e}")
        # Check for 401 Unauthorized specifically to stop the script
        if e.response.status_code == 401:
            print("\n--- CRITICAL: API Key Error ---")
            print("The API key is invalid or has expired. Halting script.")
            print("Please get a new key from https://worldnewsapi.com\n")
            return "STOP"
        return None
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred on {target_date}: {e}")
        return None


def daterange(start_date, end_date):
    """Generator for iterating through a range of dates."""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def collect_news_for_period(start_str: str, end_str: str, filename="news-month.csv"):
    """
    Collects one news article per day over a given period and saves to a CSV file.
    """
    try:
        start_date = date.fromisoformat(start_str)
        end_date = date.fromisoformat(end_str)
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    csv_header = ["วันที่ของข่าว", "ประเภทข่าว", "แหล่งที่มา", "ข่าว"]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)

        print(f"Starting news collection from {start_date} to {end_date}.")

        for single_date in daterange(start_date, end_date):
            date_str = single_date.strftime("%Y-%m-%d")
            print(f"Fetching news for {date_str}...")

            article = fetch_one_news_for_date(date_str)

            if article == "STOP":
                break  # Exit the loop if a critical API error occurred

            if article:
                # Prepare row data
                row_data = [
                    article.get('publish_date', date_str),
                    'economics', # The category is fixed
                    article.get('source_country', 'th'),
                    article.get('title', 'N/A')
                ]
                writer.writerow(row_data)
                print(f"  -> Success: Saved article '{article.get('title', 'No Title')}'")
            else:
                print(f"  -> Failure: No news found for {date_str}.")

            # Respect the rate limit of 1 request per second
            time.sleep(1)

    print(f"\nNews collection complete. Data saved to '{filename}'.")


if __name__ == "__main__":
    # --- Configuration ---
    # Specify the start and end date for news collection.
    # Format: YYYY-MM-DD
    START_DATE = "2024-06-01"
    # Using a shorter period for demonstration purposes to avoid using too many API points.
    # You can change this to a full month, e.g., "2024-06-30"
    END_DATE = "2024-06-05"

    days_to_run = (date.fromisoformat(END_DATE) - date.fromisoformat(START_DATE)).days + 1

    print("--- Multi-Day News Collector ---")
    print(f"This script will run for {days_to_run} day(s), from {START_DATE} to {END_DATE}.")
    print("It will make one API request per day, waiting 1 second between each.")
    print("Please ensure your API key has enough credits.\n")

    collect_news_for_period(START_DATE, END_DATE)
