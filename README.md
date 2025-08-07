# jules-worldnewsapi

## Thai News Fetcher

This project contains a Python script (`thai_news_fetcher.py`) to fetch news articles from the [World News API](https://worldnewsapi.com).

The script is configured to search for economic news from Thailand for a specific date.

### Prerequisites

Before running the script, you need to have Python installed. You will also need to install the `requests` library.

You can install it using pip:
```bash
pip install requests
```

### How to Run

You can run the script directly from your terminal:

```bash
python thai_news_fetcher.py
```

By default, the script is set to fetch news for the date `2024-07-15`.

### How to Modify the Date

To fetch news for a different date, open the `thai_news_fetcher.py` file and modify the `news_date` variable inside the `if __name__ == "__main__":` block:

```python
if __name__ == "__main__":
    # You can change this date to any date you want in 'YYYY-MM-DD' format.
    news_date = "2024-07-16" # <-- Change this value
    # ...
```

### API Key

The script uses a pre-configured API key. If the key has expired or is invalid, the script will print an error message. You can obtain a free API key from the [World News API website](https://worldnewsapi.com) and replace the `api_key` variable in the `fetch_thai_economic_news` function.