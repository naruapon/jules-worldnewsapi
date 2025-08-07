import requests

def fetch_thai_economic_news(target_date: str):
    """
    Fetches economic news from Thailand for a specific date from the World News API.

    Args:
        target_date: The date for which to fetch news, in 'YYYY-MM-DD' format.

    Returns:
        A dictionary with the news data or an error string.
    """
    # We use the 'search-news' endpoint as it is more suitable for filtering.
    url = "https://api.worldnewsapi.com/search-news"
    api_key = "2df338b8696b4d83aa2a3d0b52197256"

    headers = {
        'x-api-key': api_key
    }

    # Parameters for the API request based on the user's requirements.
    # The parameter 'category' is used for filtering by news category.
    params = {
        'source-countries': 'th',
        'category': 'economics',
        'date': target_date  # Using the 'date' parameter as in the original example
    }

    try:
        # We use the 'params' argument to let the requests library handle URL encoding.
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Example: Fetch news for a specific date. You can change this date.
    # Note: The API may not have news for every single day.
    news_date = "2024-07-15"
    print(f"Fetching economic news from Thailand for the date: {news_date}...")

    news_data = fetch_thai_economic_news(news_date)

    # The provided API key might be expired or invalid, so we check for a 401 error.
    if isinstance(news_data, dict) and news_data.get('code') == 401:
        print("\n--------------------------------------------------")
        print("API Call Failed: Unauthorized (401).")
        print("Please check if your API key is correct and active.")
        print("You can get a free API key from https://worldnewsapi.com")
        print("--------------------------------------------------\n")

    if isinstance(news_data, dict) and 'news' in news_data:
        if news_data['news']:
            print(f"Successfully fetched {len(news_data['news'])} news articles.")
            # Print the top 5 articles as an example
            for i, article in enumerate(news_data['news'][:5], 1):
                print(f"\n--- Article {i} ---")
                print(f"Title: {article.get('title')}")
                print(f"Source: {article.get('source_country')}")
                print(f"Published: {article.get('publish_date')}")
                print(f"URL: {article.get('url')}")
        else:
            print(f"No economic news found for Thailand on {news_date}.")
            print("This could be because there were no articles for that day or the 'economics' category might be named differently (e.g., 'business').")
    else:
        print("\nCould not retrieve news. The server responded with:")
        print(news_data)
