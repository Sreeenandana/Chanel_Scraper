import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the Chanel website
base_url = 'https://www.chanel.com'
# Initial URL to start scraping
url = 'https://www.chanel.com/in/fragrance/bath-and-body/c/7x1x7x92/women/'

def scrape(url):
    """
    Scrapes Chanel product data from multiple pages.
    Args: url - The URL of the page to start scraping.
    Returns: A list of dictionaries containing product details.
    """

    data = []

    try:
        # Loop until there are no more "Load More" links
        while url:
            # Send an HTTP GET request to the URL
            response = requests.get(url)
            # Raise an exception if the request fails
            response.raise_for_status()  
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'lxml')

            # Find all product blocks on the page
            product_blocks = soup.find_all('div', class_='txt-product')
            for block in product_blocks:
                # Extract the product URL and retrieve details
                product_url = base_url + block.find("a").attrs['href']
                data.append(get_product_details(product_url))

            # Check if there's a viable "Load More" link
            load_more = soup.find('div', class_='container loadmore-container')
            load_more_url = load_more.find("a").attrs['href']
            if load_more_url:
            # Update the URL to the next page
              url=base_url+load_more_url
            else:
            # No more pages, exit the loop
               url = None
    except:
        print("An error occurred during the request")

    return data


def extract_title(soup):
    """
    Extracts the title of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product title.
    """
    title_element = soup.find('span', class_='heading product-details__title text-ltr-align')
    title = title_element.text.strip()
    return title if title else 'Not available'



def extract_type(soup):
    """
    Extracts the type of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product type.
    """
    type_element = soup.find('span', class_='product-details__description')
    type = type_element.text.strip()
    return type if type else 'Not available'


def extract_reference(soup):
    """
    Extracts the reference of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product reference.
    """
    reference_element = soup.find('div', class_='product-details-block')
    reference_text = reference_element.text.strip()
    reference = ''.join(filter(str.isdigit, reference_text))
    return reference if reference else 'Not available'


def extract_price(soup):
    """
    Extracts the price of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product price.
    """
    price_element = soup.find('p', class_='product-details__price')
    price_text = price_element.text.strip()
    price = ''.join(filter(str.isdigit, price_text))
    return price if price else 'Not available'


def extract_size(soup):
    """
    Extracts the size of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product size.
    """
    size_element =  soup.find('p', attrs={'data-test': 'lblVariantNameSingleVariant'})
    size_text = size_element.text.strip()
    size = ''.join(filter(str.isdigit, size_text))
    return size if size else 'Not available'


def extract_description(soup):
    """
    Extracts the description of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product description.
    """
    description_heading = soup.find('h3', string ='DESCRIPTION')
    description_element = description_heading.find_next('p')
    description = description_element.text.strip()  
    return description if description else 'Not available'


def extract_composition(soup):
    """
    Extracts the composition of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product composition.
    """
    composition_heading = soup.find('h3', string ='COMPOSITION')
    composition_element = composition_heading.find_next('p')
    composition = composition_element.text.strip() 
    return composition if composition else 'Not available'



def get_product_details(product_url):
    """
    Retrieves product details from a product page.
    Args: product_url - The URL of the product page.
    Returns: A dictionary containing product details.
    """
    try:
        # Send an HTTP GET request to the product URL
        response = requests.get(product_url)
        response.raise_for_status()  # Raise an exception if the request fails
        # Parse the HTML content of the product page
        soup = BeautifulSoup(response.content, 'lxml')

        # Extract product details using separate functions
        title = extract_title(soup)
        description = extract_description(soup)
        reference = extract_reference(soup)
        price = extract_price(soup)
        size = extract_size(soup)
        type = extract_type(soup)
        composition = extract_composition(soup)

        return {
            'URL': product_url,
            'Title': title,
            'Type': type,
            'Reference': reference,
            'Price': price,
            'Size': size,
            'Description': description,
            'Composition': composition
        }
    except:
        print("An error occurred while extracting details for " + product_url)
        # Return an empty dictionary to indicate that the extraction failed for this product
        return {}

def save_to_csv(data):
    """
    Saves scraped data to a CSV file.
    Args: A list of dictionaries containing product details.
    """
    try:
        # Create a Pandas DataFrame from the scraped data
        dataframe = pd.DataFrame(data)
        # Save the DataFrame to a CSV file named "chanel.csv"
        dataframe.to_csv("chanel.csv", index=False)
    except:
        print("An error occurred while saving to CSV")

def main():
    """
    Main function to initiate the scraping process.
    """
    # Start scraping Chanel product data
    data = scrape(url)
    # Save the scraped data to a CSV file
    save_to_csv(data)

if __name__ == "__main__":
    # Call the main function when the script is run
    main()
