from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
import os

List of websites with credit card data (example URLs)

websites = [
{
"name": "ScraperWiki",
"url": "https://www.scraperwiki.com",
"selectors": {
"card_number": "div.card-number",
"cvv": "span.cvv",
"expiration": "span.expiration"
}
},
{
"name": "Example.com",
"url": "https://www.example.com",
"selectors": {
"card_number": "table.credit-cards td:nth-child(1)",
"cvv": "table.credit-cards td:nth-child(2)",
"expiration": "table.credit-cards td:nth-child(3)"
}
},
{
"name": "Tutorialspoint",
"url": "https://www.tutorialspoint.com",
"selectors": {
"card_number": "div.card-info span.number",
"cvv": "div.card-info span.cvv",
"expiration": "div.card-info span.exp"
}
},
{
"name": "W3Schools",
"url": "https://www.w3schools.com",
"selectors": {
"card_number": "pre.card-data",
"cvv": "pre.card-data",
"expiration": "pre.card-data"
}
},
{
"name": "CreditCardTest",
"url": "https://www.creditcardtest.com",
"selectors": {
"card_number": "ul.card-list li:nth-child(1)",
"cvv": "ul.card-list li:nth-child(2)",
"expiration": "ul.card-list li:nth-child(3)"
}
},
{
"name": "PayPal Demo",
"url": "https://www.paypal.com",
"selectors": {
"card_number": "input.card-number",
"cvv": "input.cvv",
"expiration": "input.expiration"
}
},
{
"name": "Stripe Test Cards",
"url": "https://www.stripe.com",
"selectors": {
"card_number": "div.test-card span.number",
"cvv": "div.test-card span.cvv",
"expiration": "div.test-card span.exp"
}
},
{
"name": "PaymentsDemo",
"url": "https://www.paymentsdemo.com",
"selectors": {
"card_number": "table.demo-cards td:nth-child(1)",
"cvv": "table.demo-cards td:nth-child(2)",
"expiration": "table.demo-cards td:nth-child(3)"
}
},
]

Configuration

chrome_driver_path = "/data/data/com.termux/files/usr/bin/chromedriver"  # Adjust to your path
output_dir = "credit_card_data"
os.makedirs(output_dir, exist_ok=True)

Initialize WebDriver

service = Service(chrome_driver_path)
options = Options()
options.add_argument("--headless")  # Run without GUI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

Launch browser

with webdriver.Chrome(service=service, options=options) as driver:
for idx, site in enumerate(websites):
url = site["url"]
print(f"\nScraping from {site['name']} at {url}...")
driver.get(url)
time.sleep(3)  # Wait for content to load (adjust as needed)

Extract HTML content

html_content = driver.page_source    
soup = BeautifulSoup(html_content, "lxml")    

# Extract credit card data using selectors    
credit_cards = []    
for element in soup.find_all("div", class_="card-detail"):  # Use specific selectors per site    
    card_number = element.find(site["selectors"]["card_number"]).text.strip() if site["selectors"]["card_number"] else ""    
    cvv = element.find(site["selectors"]["cvv"]).text.strip() if site["selectors"]["cvv"] else ""    
    expiration = element.find(site["selectors"]["expiration"]).text.strip() if site["selectors"]["expiration"] else ""    

    if card_number:    
        credit_cards.append({    
            "card_number": card_number,    
            "cvv": cvv,    
            "expiration": expiration,    
            "source": site["name"]    
        })    

# Save data to file    
output_file = os.path.join(output_dir, f"site_{idx + 1}_data.txt")    
with open(output_file, "w") as file:    
    for card in credit_cards:    
        file.write(f"{card['card_number']} | {card['cvv']} | {card['expiration']} | {card['source']}\n")    

print(f"Scraped {len(credit_cards)} cards from {site['name']}.")

print("Scraping complete. Data saved in 'credit_card_data' directory.")
