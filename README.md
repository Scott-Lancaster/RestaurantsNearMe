# Restaurants Near Me
## Summary
This script is a fun and interactive project to track the percentage of restaurants along a specified street that you’ve eaten at. By leveraging the Google Maps API, the script identifies all restaurants along a given stretch of road, filters them based on geographic boundaries, and saves the results to a CSV file. It’s perfect for foodies looking to explore their local culinary scene systematically!

## Requirements
- Google Maps API Access: The script requires access to Google Maps API (Geocoding and Places APIs). Make sure you have a valid API key and have enabled these APIs in your Google Cloud Console.
- Python Dependencies: The script uses the following Python libraries:
  requests
  csv
  time

## Code Structure
1. Parameters Section: Defines key inputs such as the street names, city, and radius for the search.

2. Functions:
  get_coordinates: Fetches the latitude and longitude for a given street intersection.
  fetch_restaurants_nearby: Retrieves a list of restaurants within a specified radius using the Google Places API.
  filter_by_bounding_box: Filters restaurants to ensure they are within the specified geographic bounds.
  save_to_csv: Saves the filtered restaurant data to a CSV file.
3. Main Function: Ties everything together by fetching start and end coordinates, searching for restaurants along the street, and saving the results to a file.

## Future Improvements
1. Improve Boundary Box for Streets: Address issues where some restaurants are included outside the intended bounds, ensuring more accurate filtering.
2. Add Radius-Based Search Option: Implement an alternative mode to search for restaurants in a circular area around a point, rather than along a street.
3. Progress Tracking and Visualization: Develop a second script to track and visualize progress in completing the list of restaurants. This could include plotting checked-off restaurants on a map or generating progress reports, eliminating the need for external tools like Google Sheets.
