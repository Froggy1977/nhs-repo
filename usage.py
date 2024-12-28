# usage.py

from nhs_digital_agent import NHSDigitalAgent

def demonstrate_basic_usage():
    # Initialize the agent
    print("Initializing NHS Digital Agent...")
    agent = NHSDigitalAgent()

    # Example 1: Get all datasets
    print("\n1. Getting all datasets:")
    print("-" * 50)
    datasets = agent.get_datasets()
    print(f"Found {len(datasets)} datasets")
    # Display first 3 datasets as example
    for dataset in datasets[:3]:
        print(f"\nTitle: {dataset['title']}")
        print(f"URL: {dataset['url']}")
        print(f"Description: {dataset['description']}")

    # Example 2: Search for specific datasets
    print("\n2. Searching for 'mental health' datasets:")
    print("-" * 50)
    search_results = agent.search_datasets("mental health")
    print(f"Found {len(search_results)} matching datasets")
    for result in search_results[:2]:  # Show first 2 results
        print(f"\nTitle: {result['title']}")
        print(f"URL: {result['url']}")

    # Example 3: Get details for a specific dataset
    if search_results:
        print("\n3. Getting details for first search result:")
        print("-" * 50)
        details = agent.get_dataset_details(search_results[0]['url'])
        if details:
            print(f"Title: {details['title']}")
            print(f"Last Updated: {details['last_updated']}")
            print("\nFirst few content sections:")
            for section in details['content'][:2]:
                print(f"{section['type'].upper()}: {section['text']}")

def demonstrate_advanced_usage():
    agent = NHSDigitalAgent()

    # Example 4: Custom search and error handling
    print("\n4. Custom search with error handling:")
    print("-" * 50)
    try:
        results = agent.search_datasets("diabetes")
        if results:
            print(f"Found {len(results)} datasets related to diabetes")
        else:
            print("No datasets found for this search term")
    except Exception as e:
        print(f"Error occurred during search: {str(e)}")

    # Example 5: Working with dataset details
    print("\n5. Extracting specific information:")
    print("-" * 50)
    datasets = agent.get_datasets()
    if datasets:
        first_dataset = datasets[0]
        details = agent.get_dataset_details(first_dataset['url'])
        if details:
            # Extract and display related links
            print("Related links:")
            for link in details['related_links'][:3]:
                print(f"- {link['title']}: {link['url']}")

if __name__ == "__main__":
    print("NHS Digital Agent Usage Examples")
    print("=" * 50)
    
    print("\nBasic Usage Examples:")
    demonstrate_basic_usage()
    
    print("\nAdvanced Usage Examples:")
    demonstrate_advanced_usage()