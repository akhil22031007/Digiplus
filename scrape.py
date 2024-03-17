import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#import googlesearch as gsr

# Function to extract details of a business from its GMB listing
def extract_business_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    details = {}
    
    # Extract business name
    business_name_tag = soup.find('h1', class_='section-hero-header-title-title')
    if business_name_tag is not None:
        business_name = business_name_tag.text.strip()
        details['Business Name'] = business_name
    else:
        print(f"Error: Business name not found for URL {url}")
        details['Business Name'] = ''
    
    # Extract contact details
    contact_info = soup.find_all('span', class_='widget-pane-link')
    contacts = []
    for info in contact_info:
        contacts.append(info.text.strip())
    if contacts:
        details['Contact'] = ', '.join(contacts)
    else:
        details['Contact'] = ''
    
    # Extract address
    address_info = soup.find_all('div', class_='ugiz4pqJLAG__primary-text gm2-body-2')
    addresses = []
    for info in address_info:
        addresses.append(info.text.strip())
    if addresses:
        details['Address'] = ', '.join(addresses)
    else:\
        details['Address'] = ''
    
    # Extract website
    website_info = soup.find('a', class_='QqG1Sd')
    if website_info:
        details['Website'] = website_info.get('href')
    else:
        details['Website'] = ''
    
    return details

# Function to authenticate and write data to Google Sheet
def Web_scraping(data):
    scope = ['https://docs.google.com/spreadsheets/d/1czNLrC3HkNpUlZmTnH-MiErxDFpq0ooneAZc5Zb1GZs/edit?usp=sharing','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('web-scraping.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open('Business Details').sheet1
    
    headers = ['Business Name', 'Contact', 'Address', 'Website']
    
    # Write headers
    sheet.insert_row(headers, index=1)
    
    # Write data
    for i, business in enumerate(data, start=2):
        row = [business.get(header, '') for header in headers]
        try:
            sheet.insert_row(row, index=i)
        except KeyError:
            print(f"Error: Access token not found for URL {business['URL']}")

# Main function
def main():
    urls = [
        'https://www.google.com/maps/place/Vaishali+Super+Store',
        'https://www.google.com/maps/place/Jay+Bhavani+Super+Markets',
        # Add more URLs here for other businesses
    ]
    
    business_data = []
    
    for url in urls:
        business_data.append(extract_business_details(url))
    
    Web_scraping(business_data)

if __name__ == "__main__":
    main()
