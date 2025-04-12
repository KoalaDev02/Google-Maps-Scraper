# Google Maps Scraper

This script is designed to scrape business listings from Google Maps based on a user-provided search term. It extracts key details such as the name, address, website, phone number, reviews count, average rating, and business type. The results are saved to a CSV file for further analysis.

---

## **Disclaimer**
This script is intended for **educational purposes only**. Scraping data from Google Maps may violate their terms of service. Use this tool responsibly and ensure compliance with all applicable laws and regulations. The author is not responsible for any misuse or legal consequences arising from the use of this script.

---

## **Features**
- Extracts business details from Google Maps.
- Blocks unnecessary resources (e.g., ads, analytics) to improve performance.
- Handles dynamic content loading and ensures data integrity.
- Saves extracted data to a CSV file named after the search term.

---

## **Requirements**
Before running the script, ensure you have the following installed:
1. **Python 3.8 or higher**
2. **Playwright**: Install via `pip install playwright`
   - After installation, run `playwright install` to download the required browser binaries.
3. **Fake User-Agent**: Install via `pip install fake-useragent`
4. **CSV Module**: Included in Python's standard library, no additional installation required.

Install all dependencies using:
```bash
pip install -r requirements.txt
