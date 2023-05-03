import os
import requests
from bs4 import BeautifulSoup
import csv

# Set headers to emulate browser behavior
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Make the HTTP request with headers
url = "https://www.bundesliga.com/en/bundesliga/table"
response = requests.get(url, headers=headers)

# Create the BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

# Find the table using the CSS selector
table_element = soup.select_one("#default > div > table-page > div > div.table > tablecomponent > div.table-wrapper > div > table > tbody")

# Check if the table was found
if table_element is not None:
    # Extract the data from the table
    data = []
    rows = table_element.find_all("tr")
    for row in rows:
        # Extract the cells from the row
        cells = row.find_all("td")
        row_data = [cell.text.strip().replace(":", ",").replace(", ", ",") for cell in cells if cell.text.strip()]

        # Check if the row does not contain empty cells
        if row_data:
            data.append(row_data)

    # Add the headers
    header = ["position", "team", "matches", "win", "draw", "loss", "goals_scored", "goals_conceded", "goal_balance", "points"]
    data.insert(0, header)

    # Create the "csv" folder if it doesn't exist
    os.makedirs("csv", exist_ok=True)

    # Save the data to a CSV file in the "csv" folder
    csv_file = os.path.join("csv", "bundesliga_table.csv")
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

    print("Data saved successfully to the file bundesliga_table.csv in the csv folder.")

    # Reopen the CSV file and remove double quotes
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.replace('"', '') for line in lines]

    # Write the updated lines back to the CSV file
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        file.writelines(lines)

    print("Double quotes removed from the CSV file.")
else:
    print("Table not found.")
