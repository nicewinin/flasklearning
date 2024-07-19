import requests

# 如何使用python模拟浏览器，发起http请求
def fetch_data_with_get():
    # URL to send the GET request to
    url = "https://jsonplaceholder.typicode.com/posts"
    
    # Prepare GET request
    response = requests.request("GET", url)
    
    # Check status code and print result
    if response.status_code == 200:
        data = response.json()
        print("GET request successful. Here's a preview of the response data:")
        print(data[:2])  # Print first two items for brevity
    else:
        print(f"GET request failed with status code: {response.status_code}")

def send_data_with_post():
    # URL to send the POST request to
    url = "https://jsonplaceholder.typicode.com/posts"
    
    # Data payload to be sent in the POST request
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    
    # Prepare POST request
    response = requests.request("POST", url, json=payload)
    
    # Check status code and print result
    if response.status_code == 201:
        data = response.json()
        print("POST request successful. Here's the response data:")
        print(data)
    else:
        print(f"POST request failed with status code: {response.status_code}")

# Run the example functions
if __name__ == "__main__":
    print("Performing GET request...")
    fetch_data_with_get()
    
    print("\nPerforming POST request...")
    send_data_with_post()