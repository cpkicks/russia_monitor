import requests
import bs4
from discord_hooks import Webhook
from currency_converter import CurrencyConverter


c = CurrencyConverter()
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'

headers = {
    "User-Agent" : ua,
    }

webhook = "https://discordapp.com/api/webhooks/562545504907689994/jmZNPh9GdKP6DkKk7--IqqxY4lRfjECETzL6eJbj-feeLlNLnI9Ydgl_gu10t3RD-opj"

link = "https://www.km20.ru/catalog/brand/65567/"

def sendwebhook(href, name, k, l, price, usd):

    embed = Webhook(webhook, color=11473438)
    embed.set_title(title=name, url=href)
    embed.set_thumbnail(url=l)
    embed.add_field(name="Price", value=price)
    embed.add_field(name="Price in USD", value=usd)
    embed.add_field(name="Sizes", value=k)
    embed.set_footer(text='The Vault AIO', ts=True)
    embed.post()

def monitor():
    try:
        if("km20.ru" in link):
            r = requests.get(link, headers=headers)
            soup = bs4.BeautifulSoup(r.content, 'lxml')

            raw_links = soup.find_all('a', class_ = 'cat_item')
            hrefs = []
            names = []
            prices = []
            images = []
            sizes = []
            for raw_link in raw_links:
                try:
                    href = ("https://www.km20.ru" + raw_link.get('href'))
                    hrefs.append(href)
                    name = raw_link.find('span', class_ = 'cat_item_name').text
                    names.append(name)
                    size_a = raw_link.find_all('span', class_ = 'cat_item_size')
                    for size in size_a:
                        k = size.get_text()
                        sizes.append(k)
                    image = raw_link.find_all('span', class_ = 'cat_item_img')
                    for imag in image:
                        l = "https:" + imag.img['src']
                        images.append(l)
                    price = raw_link.find('span', class_ = 'cat_item_price').text
                    prices.append(price)
                    s = price.replace(' руб.', '')
                    lol = s.replace(' ', '')
                    usd = "$" + str(round(c.convert(lol, 'RUB', 'USD'), 2))

                    sendwebhook(href, name, k, l, price, usd)
                except:
                    pass
        #else if("sneakerhead.ru" in link):

        #else if("m.brandshop.ru" in link):

    except:
        pass

monitor()
