import requests
import csv
import time

# Google Maps API key
API_KEY = 'Google_Maps_API'

# Define the base URL for the APIs
PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

# Parameters
street = 'Union Street'
city = 'San Francisco'
start_street = 'Gough Street'
end_street = 'Pierce Street'
radius = 100  # Radius in meters for each search point

# Function to get coordinates of an address

def get_coordinates(street1, street2, city):
    """
    Fetches coordinates for an intersection of two streets in a specified city.

    :param street1: Name of the first street (e.g., '10th Avenue').
    :param street2: Name of the second street (e.g., 'Clement Street').
    :param city: Name of the city (e.g., 'San Francisco').
    :return: A dictionary with 'lat' and 'lng' or None if not found.
    """
    address = f"{street1} at {street2}, {city}"
    print(f"Fetching coordinates for: {address}")

    params = {
        'address': address,
        'key': API_KEY
    }
    response = requests.get(GEOCODE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            location = results[0]['geometry']['location']
            print(f"Coordinates for {address}: {location}")
            return location
        else:
            print(f"No results found for: {address}. Response: {data}")
    else:
        print(f"Error fetching coordinates for: {address}. HTTP Status: {response.status_code}. Response: {response.text}")
    return None


# Function to fetch restaurants using Nearby Search
def fetch_restaurants_nearby(api_key, location, radius):
    params = {
        'location': f"{location['lat']},{location['lng']}",
        'radius': radius,
        'type': 'restaurant',  # Specific type for restaurants
        'key': api_key
    }
    results = []
    while True:
        response = requests.get(PLACES_URL, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            break
        data = response.json()
        results.extend(data.get('results', []))
        # Check for next page token
        next_page_token = data.get('next_page_token')
        if not next_page_token:
            break
        params['pagetoken'] = next_page_token
        time.sleep(2)  # Add delay for token activation
    return results

# Function to filter restaurants within the bounding box
def filter_by_bounding_box(restaurants, min_lat, max_lat, min_lng, max_lng, street_filter=None):
    filtered = []
    for restaurant in restaurants:
        location = restaurant.get('geometry', {}).get('location', {})
        lat = location.get('lat')
        lng = location.get('lng')
        address = restaurant.get('vicinity', '')

        # Check if the restaurant is within the bounding box
        if (min_lat <= lat <= max_lat) and (min_lng <= lng <= max_lng):
            # Optionally filter by street name
            if street_filter and street_filter.lower() not in address.lower():
                continue
            filtered.append(restaurant)
    return filtered

# Function to save data to CSV
def save_to_csv(restaurants, filename='restaurants_on_street.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Restaurant Name', 'Address'])  # CSV headers
        for restaurant in restaurants:
            name = restaurant.get('name')
            address = restaurant.get('vicinity')  # Nearby Search uses 'vicinity' for address
            writer.writerow([name, address])

# Main function
def main():
    print("Fetching coordinates for start and end streets...")
    start_location = get_coordinates(start_street, street, city)
    end_location = get_coordinates(end_street, street, city)

    if not start_location or not end_location:
        print("Error: Could not determine coordinates for start or end streets. Check address format.")
        return

    # Define bounding box
    min_lat = min(start_location['lat'], end_location['lat'])
    max_lat = max(start_location['lat'], end_location['lat'])
    min_lng = min(start_location['lng'], end_location['lng'])
    max_lng = max(start_location['lng'], end_location['lng'])

    print("Fetching restaurant data along the street...")
    restaurants = []
    seen_places = set()  # To deduplicate results
    
    # Calculate longitude step for moving along the street
    steps = 20  # Number of steps between start and end
    lng_step = (end_location['lng'] - start_location['lng']) / steps

    current_location = start_location
    for step in range(steps + 1):
        print(f"Fetching restaurants near: {current_location}")
        new_restaurants = fetch_restaurants_nearby(API_KEY, current_location, radius)
        
        # Deduplicate restaurants
        for restaurant in new_restaurants:
            place_id = restaurant.get('place_id')
            if place_id not in seen_places:
                seen_places.add(place_id)
                restaurants.append(restaurant)
        
        # Move west along the street
        current_location['lng'] += lng_step

    # Filter restaurants within the bounding box
    filtered_restaurants = filter_by_bounding_box(
        restaurants, min_lat, max_lat, min_lng, max_lng, street_filter=street
    )

    if filtered_restaurants:
        print(f"Found {len(filtered_restaurants)} restaurants within the specified range. Saving to CSV...")
        save_to_csv(filtered_restaurants, filename='restaurants_on_street.csv')
        print("Data saved successfully to 'restaurants_on_street.csv'!")
    else:
        print("No restaurants found within the specified range.")

if __name__ == '__main__':
    main()

