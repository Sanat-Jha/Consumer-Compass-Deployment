import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

# Headers to set the request as a browser request
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

# Function to extract HTML from each Amazon review page
def reviewsHtml(url, len_page):
    # Empty list to store all page's HTML data
    soups = []
    
    for page_no in range(1, len_page + 1):
        try:
            # Parameters for page number
            params = {
                'ie': 'UTF8',
                'reviewerType': 'all_reviews',
                'filterByStar': 'critical',  # Remove this if you want all reviews
                'pageNumber': page_no,
            }

            # Make a request for each page with headers and parameters
            response = requests.get(url, headers=headers, params=params)

            # Check if request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                # Check for Captcha
                if soup.find('form', {'action': '/errors/validateCaptcha'}):
                    print(f"Captcha encountered on page {page_no}. Skipping...")
                    continue

                # Add the soup object to the list
                soups.append(soup)
            else:
                print(f"Failed to retrieve page {page_no}, status code: {response.status_code}")
                continue
            
            # Random sleep between requests to avoid detection
            time.sleep(random.uniform(2, 5))
        
        except requests.exceptions.RequestException as e:
            print(f"Request failed for page {page_no}: {e}")
            continue

    return soups

# Function to extract review details from HTML
def getReviews(html_data):
    # Create an empty list to hold review data
    data_dicts = []

    # Select all review boxes using CSS selector
    boxes = html_data.select('div[data-hook="review"]')

    # Iterate through all review boxes
    for box in boxes:
        try:
            name = box.select_one('[class="a-profile-name"]').text.strip()
        except Exception as e:
            name = 'N/A'
        
        try:
            stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
        except Exception as e:
            stars = 'N/A'

        try:
            title = box.select_one('[data-hook="review-title"]').text.strip()
        except Exception as e:
            title = 'N/A'

        try:
            # Convert date string to dd/mm/yyyy format
            datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
            date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
        except Exception as e:
            date = 'N/A'

        try:
            description = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception as e:
            description = 'N/A'

        # Create a dictionary with all the review data
        data_dict = {
            'Name': name,
            'Stars': stars,
            'Title': title,
            'Date': date,
            'Description': description
        }

        # Add dictionary to the master list
        data_dicts.append(data_dict)

    return data_dicts

# Function to scrape reviews and return list of review strings
def fetch_amazon_reviews(url, len_page=4):
    # Get the HTML data for the specified number of pages
    html_datas = reviewsHtml(url, len_page)

    # Empty list to hold all reviews data
    reviews = []

    # Iterate through all the HTML pages and extract review data
    for html_data in html_datas:
        review = getReviews(html_data)
        reviews += review

    # Create a DataFrame with the reviews data
    df_reviews = pd.DataFrame(reviews)

    # Return the 'Description' column as a list of review strings
    return df_reviews['Description'].tolist()

# Example of calling this function from an external file
if __name__ == "__main__":
    url = 'https://www.amazon.com/Legendary-Whitetails-Journeyman-Jacket-Tarmac/product-reviews/B013KW38RQ/'
    reviews_list = fetch_amazon_reviews(url, len_page=4)
    for review in reviews_list:
        print(review)
