from bs4 import BeautifulSoup
from twitter import Twitter
from scrapper import Scrapper
from datetime import datetime
import pytz

twitter = Twitter()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
url_infobae = "https://www.infobae.com/economia/divisas/dolar-hoy/"
url_invertir = "https://iol.invertironline.com/mercado/cotizaciones/argentina"

infobae_scrapper = Scrapper(url_infobae, headers)
invertir_online_scrapper = Scrapper(url_invertir, headers)

data = infobae_scrapper.get_data()
data2 = invertir_online_scrapper.get_data()

soup = BeautifulSoup(data, "html.parser")
soup2 = BeautifulSoup(data2, "html.parser")

prices = []

for div in soup.find_all(class_="exchange-dolar-container"):
    for item in div:
        name = item.find(class_="exchange-dolar-title").get_text()
        amount = item.find(class_="exchange-dolar-amount").get_text()
        variation = item.find(class_="exchange-dolar-percentage").get_text()
        prices.append(f"{name}: {amount} ({variation})")


for tr in soup2.find_all("tr"):
    name = tr.find("b")
    value = tr.find("span", class_="ml15")
    if name and value:
        print("--------------------------")
        print(f"{name.text.strip()}: {value.text.strip()}")

# Timezone object for Buenos Aires
buenos_aires = pytz.timezone('America/Argentina/Buenos_Aires')
buenos_aires_time = datetime.now(buenos_aires)
# Extract the hour and minutes
current_hour = buenos_aires_time.hour
current_minute = buenos_aires_time.minute

tweet = f"Mercados a las {current_hour}:{
    current_minute:02d}:\n\n{"\n".join(prices)}"
# twitter.create_tweet(tweet)
