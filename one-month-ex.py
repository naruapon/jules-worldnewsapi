import requests
import pandas as pd
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
        'limit': 1
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('news') and len(data['news']) > 0:
            return data['news'][0]
        return None
    except requests.exceptions.HTTPError as e:
        print(f"API Error on {target_date}: {e}")
        if e.response.status_code == 401:
            print("\nCRITICAL: API Key Error. Halting script.")
            return "STOP"
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error on {target_date}: {e}")
        return None

def daterange(start_date, end_date):
    """Generator for iterating through a range of dates."""
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def collect_news_and_save_to_excel(start_str: str, end_str: str, filename="news-month.xlsx"):
    """
    Collects news articles over a period and saves them to an Excel file.
    """
    try:
        start_date = date.fromisoformat(start_str)
        end_date = date.fromisoformat(end_str)
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    all_articles_data = []

    print(f"Starting news collection from {start_date} to {end_date}.")

    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime("%Y-%m-%d")
        print(f"Fetching news for {date_str}...")

        article = fetch_one_news_for_date(date_str)

        if article == "STOP":
            break

        if article:
            # Prepare a dictionary for the current article's data
            article_data = {
                "วันที่ของข่าว": article.get('publish_date', date_str),
                "ประเภทข่าว": 'economics',
                "แหล่งที่มา": article.get('source_country', 'th'),
                "ข่าว": article.get('title', 'N/A')
            }
            all_articles_data.append(article_data)
            print(f"  -> Success: Collected article '{article.get('title', 'No Title')}'")
        else:
            print(f"  -> Failure: No news found for {date_str}.")

        # Respect the rate limit
        time.sleep(1)

    if not all_articles_data:
        print("\nNo articles were collected. The Excel file will not be created.")
        return

    print(f"\nCollection complete. Saving {len(all_articles_data)} articles to Excel file: {filename}")

    # Create a pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(all_articles_data)

    # Save the DataFrame to an Excel file
    try:
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Successfully saved data to '{filename}'.")
    except Exception as e:
        print(f"An error occurred while saving the Excel file: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Specify the start and end dates for news collection.
    # Format: YYYY-MM-DD
    START_DATE = "2024-06-01"
    # Using a shorter period for demonstration purposes
    END_DATE = "2024-06-05"

    days_to_run = (date.fromisoformat(END_DATE) - date.fromisoformat(START_DATE)).days + 1

    print("--- Multi-Day News Collector (Excel Export) ---")
    print(f"This script will run for {days_to_run} day(s), from {START_DATE} to {END_DATE}.")

    collect_news_and_save_to_excel(START_DATE, END_DATE)
