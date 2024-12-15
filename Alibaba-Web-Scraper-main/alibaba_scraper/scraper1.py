from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
url = "https://sale.alibaba.com/category/half_trust_lp/index.html?spm=a27aq.cp_3.3164994960.1.70365b91O5fdIN&wx_navbar_transparent=true&path=/category/half_trust_lp/index.html&topOfferIds=1600955583980&cardType=101002784&cardId=3&categoryIds=3&tracelog=fy23_all_categories_home_lp"

# Set up the Selenium WebDriver (Ensure you have the appropriate ChromeDriver for your version of Chrome)
driver = webdriver.Chrome()

# Open the URL
driver.get(url)

# Optionally wait for the page to load
time.sleep(10)

# Start scrolling and check if content is loading
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  # Wait for new content to load

    # Calculate new scroll height and compare with the last one
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # If the height hasn't changed, we've reached the bottom of the page
    last_height = new_height

# Get the page source after scrolling
page_source = driver.page_source
driver.quit()

# Parse the HTML content of the page
soup = BeautifulSoup(page_source, 'html.parser')

# Prepare CSV file for writing
csv_file = "extracted_data.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Price", "Pieces", "Shipping", "Guaranteed Delivery"])

    # Wrap your scraping logic in a try-except block to avoid the script crashing
    try:
        # Find all waterfall-column divs
        waterfall_columns = soup.find_all('div', class_='waterfall-column')
        if waterfall_columns:
            for column in waterfall_columns:
                # Find all grid items inside each waterfall column
                grid_items = column.find_all('div', class_='hugo4-pc-grid-item')
                for grid_item in grid_items:
                    # Extract the <a href> link
                    link_tag = grid_item.find('a', href=True)
                    product_url = link_tag['href'] if link_tag else "N/A"

                    # Extract the product price
                    wrap_div = grid_item.find('div', class_='hugo4-product-wrap-margin wrap-margin-left wrap-margin-pc hugo3-f')
                    if wrap_div:
                        # Extract price
                        price_area = wrap_div.find('div', class_='hugo4-product-price-area')
                        if price_area:
                            price_div = price_area.find('div', class_='hugo4-product-element price price-pc line-2 hugo3-util-ellipsis undefined')
                            price_span = price_div.find('span', class_='hugo3-fw-heavy hugo3-fz-medium') if price_div else None
                            product_price = price_span.text.strip() if price_span else "N/A"

                            # Extract pieces information and remove unwanted text
                            pieces_span = price_div.find('span', class_='moq text hugo3-fc-light') if price_div else None
                            product_pieces = pieces_span.text.strip() if pieces_span else "N/A"
                            if '/' in product_pieces:
                                product_pieces = product_pieces.split('/')[1].strip()  # Keep only the part after the slash

                        else:
                            product_price = "N/A"
                            product_pieces = "N/A"

                        # Extract shipping information
                        shipping_div = wrap_div.find('div', class_='hugo4-product-element shipping-text price-pc hugo3-fw-heavy line-2 hugo3-util-ellipsis undefined')
                        shipping_info = shipping_div.text.strip() if shipping_div else "N/A"

                        # Extract guaranteed delivery information
                        delivery_div = wrap_div.find('div', class_='hugo4-product-element showAlibabaGuaranteed delivery delivery-pc hugo3-util-ellipsis line-2')
                        delivery_span = delivery_div.find('span') if delivery_div else None
                        guaranteed_delivery = delivery_span.text.strip() if delivery_span else "N/A"

                        # Write the data to CSV
                        writer.writerow([product_url, product_price, product_pieces, shipping_info, guaranteed_delivery])
                        print(f"Extracted: URL={product_url}, Price={product_price}, Pieces={product_pieces}, Shipping={shipping_info}, Guaranteed Delivery={guaranteed_delivery}")
                    else:
                        print("Wrap margin div not found for a grid item.")
        else:
            print("No waterfall columns found on the page.")
    except Exception as e:
        print(f"Error occurred: {e}")

print(f"\nData successfully written to {csv_file}")
