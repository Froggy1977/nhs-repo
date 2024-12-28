# test_search.py
from nhs_digital_agent import NHSDigitalAgent

def test_search():
    agent = NHSDigitalAgent()
    
    # Test 1: Basic search
    print("\nTest 1: Basic search")
    results = agent.search_datasets("mental health")
    print(f"Found {len(results)} results")
    for i, result in enumerate(results[:3], 1):
        print(f"\nResult {i}:")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Description: {result['description']}")

    # Test 2: Empty search
    print("\nTest 2: Empty search")
    results = agent.search_datasets("")
    print(f"Found {len(results)} results")

    # Test 3: Invalid search
    print("\nTest 3: Invalid search")
    results = agent.search_datasets("xyzabc123")
    print(f"Found {len(results)} results")

if __name__ == "__main__":
    test_search()