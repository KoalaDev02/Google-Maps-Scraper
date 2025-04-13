# Google Maps Scraper

A Python-based tool that utilizes Playwright to extract business listings from Google Maps based on user-defined search terms. It captures essential details such as business name, address, website, phone number, reviews count, average rating, and business type, saving them into a CSV file for further analysis.

---

## 🚀 Features

- **Comprehensive Data Extraction**: Gathers key business information from Google Maps search results.
- **Performance Optimization**: Blocks unnecessary resources (e.g., ads, analytics) to improve scraping efficiency.
- **Dynamic Content Handling**: Manages dynamic loading of content to ensure complete data retrieval.
- **User-Friendly Output**: Saves extracted data into a CSV file named after the search term.
- **Customizable Parameters**: Allows users to specify search terms and the number of results to scrape.

---

## ⚠️ Disclaimer

This script is intended for educational purposes only. Scraping data from Google Maps may violate their terms of service. Use this tool responsibly and ensure compliance with all applicable laws and regulations. The author is not responsible for any misuse or legal consequences arising from the use of this script.

---

## 🛠️ Requirements

Before running the script, ensure you have the following installed:

1. **Python**: Version 3.10 or higher.
2. **Playwright**: Install via `pip install playwright`
   - After installation, run `playwright install` to download the required browser binaries.
3. **Fake User-Agent**: Install via `pip install fake-useragent`

---

## 📦 Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/KoalaDev02/Google-Maps-Scraper.git
   cd Google-Maps-Scraper

---

## 🚀 Usage
Run the script from the terminal:

`python Main.py "your search query"`

##Example:

`python Main.py "coffee shops in San Francisco"`

---

##Notes:
The script will simulate a search on Google Maps, scroll until listings load, and click each listing to extract details.

Results are saved in a file named after your search query (underscores replace spaces), e.g., coffee_shops_in_San_Francisco.csv.

---

## 📤 Output

The output will be a CSV file containing the following fields for each business:
- Name
- Address
- Website
- Phone
- Reviews Count
- 5 Stars
- 4 Stars
- 3 Stars
- 2 Stars
- 1 Star
- Average Rating
- Type

Each file is named after the search query you provided, with spaces replaced by underscores.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
