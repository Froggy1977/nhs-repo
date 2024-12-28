# nhs_digital_agent.py
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

class NHSDigitalAgent:
    def __init__(self):
        self.base_url = "https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-sets"
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=f'nhs_digital_agent_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def get_datasets(self):
        try:
            print("Fetching datasets...")  # Debug print
            response = requests.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Update the selector to match the current NHS Digital website structure
            datasets = soup.find_all('div', class_='nhsd-t-grid-item')
            
            results = []
            for dataset in datasets:
                title_element = dataset.find('h2', class_='nhsd-t-heading-s')
                link_element = dataset.find('a')
                desc_element = dataset.find('p')
                
                if title_element and link_element:
                    result = {
                        'title': title_element.text.strip(),
                        'url': f"https://digital.nhs.uk{link_element['href']}" if link_element['href'].startswith('/') else link_element['href'],
                        'description': desc_element.text.strip() if desc_element else 'No description available'
                    }
                    results.append(result)
                    print(f"Found dataset: {result['title']}")  # Debug print
            
            return results
        except Exception as e:
            logging.error(f"Error fetching datasets: {str(e)}")
            print(f"Error: {str(e)}")  # Debug print
            return []

    def search_datasets(self, query):
        try:
            print(f"Searching for: {query}")  # Debug print
            all_datasets = self.get_datasets()
            query = query.lower()
            
            matching_datasets = [
                dataset for dataset in all_datasets
                if query in dataset['title'].lower() or 
                   query in dataset['description'].lower()
            ]
            
            print(f"Found {len(matching_datasets)} matching datasets")  # Debug print
            return matching_datasets
        except Exception as e:
            logging.error(f"Error searching datasets: {str(e)}")
            print(f"Search error: {str(e)}")  # Debug print
            return []