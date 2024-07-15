import requests
from bs4 import BeautifulSoup
import csv

def extract_product_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        product_containers = soup.find_all('div', class_='product-card__details')
        
        for container in product_containers:
            # Extract product name
            product_name = container.find('h3', class_='product-card__title').text.strip()
            
            # Extract product price
            price_container = container.find('span', class_='money')
            product_price = price_container.text.strip() if price_container else 'N/A'
            
            # Append data to products list
            products.append({
                'Product Name': product_name,
                'Price': product_price,
            })
        
        return products
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None

def save_to_csv(products, filename='products4.csv'):
    if products:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Product Name', 'Price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for product in products:
                writer.writerow(product)
        print(f"Data saved to {filename}")

if __name__ == '__main__':
    all_products = []
    base_url = 'https://www.darimooch.com/collections/all-products?page='
    
    for page in range(1, 7):  
        url = base_url + str(page)
        products = extract_product_data(url)
        all_products.extend(products)

    if products:
        save_to_csv(all_products)
