import requests
from bs4 import BeautifulSoup
from twitter import Twitter  # Ensure this is correctly imported

# Usage
twitter = Twitter()

# Set a user agent to avoid a server error while trying to scrape
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
url = "https://www.cronista.com/informacion-de-mercados/"
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

prices = []

for section in soup.find_all("section", class_="marketsList", limit=1):
    for index, li in enumerate(section.find_all("li")):
        if index == 0:
            continue

        name_span = li.find("span", class_="name")
        value_span = li.find("span", class_="value")
        percentage_span = li.find("span", class_="percentage")

        name = name_span.get_text().strip().lower().title() if name_span else "N/A"
        value = value_span.get_text().strip() if value_span else "N/A"
        percentage = (
            list(percentage_span.stripped_strings)[-1] if percentage_span else "N/A"
        )

        price = f"\033[1m{name}\033[0m -> {value}, Variación: {percentage}"
        prices.append(price)


# Function to format the tweet content
def format_tweet_content(prices):
    formatted_prices = []
    for price in prices:
        # Split the string and reformat
        name, values = price.split(" -> ")
        value, variation = values.split(", Variación: ")
        formatted_price = f"{name}: {value} ({variation})"
        formatted_prices.append(formatted_price)

    return "\n".join(formatted_prices)


# Format the tweet
tweet_content = format_tweet_content(prices)
print(tweet_content)
# # Check if tweet content needs to be split

try:
    tweet_length_limit = 280
    if len(tweet_content) <= tweet_length_limit:
        twitter.create_tweet(tweet_content)
    else:
        print("Tweet content surpasses the max length")
except Exception as e:
    print(f"An error occurred: {e}")
