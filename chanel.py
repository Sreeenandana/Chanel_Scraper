import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import re

# Base URL for the Chanel website
base_url = 'https://www.chanel.com'
# Initial URL to start scraping
url = 'https://www.chanel.com/us/fragrance/women/c/7x1x1/'

def get_soup(url):
    ''' 
    Creates a BeautifulSoup object
    Args: url - The URL of the page to start scraping.
    Returns: A BeautifulSoup object
    '''
    try:
            # Send an HTTP GET request to the URL
            response = requests.get(url)
            # Raise an exception if the request fails
            response.raise_for_status()  
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'lxml')
    except:
        print("An error occurred during htt request")        
    return soup

def get_product_page(url):
    """
    Scrapes Chanel product data from multiple pages.
    Args: url - The URL of the page to start scraping.
    Returns: A list of dictionaries containing product details.

    After the product data in the current page are extracted, we check whether there is a 'load more' link. 
    If so the variable 'url'  is now updated with the url of the new page. 
    Else the loop is exited.
    """
    data = []

    try:
        # Loop until there are no more "Load More" links
        while url:
            # Get the BeautifulSoup object
            soup = get_soup(url)
            # Find all product blocks on the page

            product_blocks = soup.find_all('div', class_='txt-product')
            for block in product_blocks:
                # Extract the product URL and retrieve details
                product_url = base_url + block.find("a").attrs['href']
                data.append(get_product_details(product_url))

            # Check if there's a viable "Load More" link
            load_more = soup.find('p', class_='box has-text-centered')
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
    if title:
        return title
    else:
        return 'Not available'



def extract_type(soup):
    """
    Extracts the type of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product type.
    """
    type_element = soup.find('span', class_='product-details__description')
    type = type_element.text.strip()
    if type:
        return type
    else:
        return 'Not available'



def extract_reference(soup):
    """
    Extracts the reference of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product reference.

    The 'reference_text' variable is cleaned to retain only the numerical values and saved to the 'reference' variable.
    """
    reference_element = soup.find('p', class_='product-details__reference')
    reference_text = reference_element.text.strip()
    reference = ''.join(filter(str.isdigit, reference_text))
    if reference:
        return reference
    else:
        return 'Not available'



def extract_price(soup):
    """
    Extracts the price of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product price.

    The 'price_text' variable is cleaned to retain only the numerical values and saved to the 'price' variable.
    """
    price_element = soup.find('p', class_='product-details__price')
    price_text = price_element.text.strip()
    price = ''.join(filter(str.isdigit, price_text))
    if price:
        return price
    else:
        return 'Not available'



def extract_size(soup):
    """
    Extracts the available sizes of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: A string with the available product sizes.

    The product could either be available in a single size or many. 
    If only a single size is there it is in a 'p' tag with data-test 'lblVariantNameSingleVariant'
    Else the sizes are in the span tag with class 'dropdown_size_text'

    The 'size_num' is the cleaned version of 'size_text' variable.
    It is cleaned firstly by removing all non numeric characters except period using the 're' library.
    Then unwanted periods at the end are removed.

    The available sizes are appended to a list 'size' and then joined.
    """
    size=[]
    size_element =  soup.find('p', attrs={'data-test': 'lblVariantNameSingleVariant'})
    if size_element:
       size_text = size_element.text.strip()
       size_num = re.sub(r'[^0-9.]', '', size_text).replace("..","")
       size.append(size_num)

    else:
       size_element =  soup.find_all('span',class_='dropdown_size_text')  
       for s in size_element:
            size_text = s.text.strip()
            size_num = re.sub(r'[^0-9.]', '', size_text).replace("..","")
            size.append(size_num)
    if size:
        return ', '.join(size)
    else:
        return 'Not available'



def extract_description(soup):
    """
    Extracts the description of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product description.

    The description is in the 'p' tag after the 'h3' tag with the string 'PRODUCT'
    """
    description_heading = soup.find('h3', string ='PRODUCT')
    description_element = description_heading.find_next('p')
    description = description_element.text.strip()  
    if description:
        return description
    else:
        return 'Not available'
    


def extract_composition(soup):
    """
    Extracts the composition of a product from the product page.
    Args: soup - The BeautifulSoup object representing the product page.
    Returns: The product composition.

    The composition is in the 'p' tag after the 'h3' tag with the string 'COMPOSITION'
    """
    composition_heading = soup.find('h3', string ='COMPOSITION')
    composition_element = composition_heading.find_next('p')
    composition = composition_element.text.strip() 
    if composition:
        return composition
    else:
        return 'Not available'



def get_product_details(product_url):
    """
    Retrieves product details from a product page.
    Args: product_url - The URL of the product page.
    Returns: A dictionary containing product details.
    """
    try:

        soup = get_soup(product_url)
        
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
            'Price (in Dollars)': price,
            'Available Sizes (in Oz.)': size,
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
    data = get_product_page(url)
    # Save the scraped data to a CSV file
    save_to_csv(data)

if __name__ == "__main__":
    # Call the main function when the script is run
    main()


