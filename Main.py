from playwright.sync_api import sync_playwright
import fake_useragent
import csv
import time
import argparse
# Generate a Windows-specific user agent or else it won't work!
ua = fake_useragent.UserAgent()
while True:
    generated_ua = ua.random
    if "Windows" in generated_ua:
        break
# rev_count=0
# search = input("What do you want to search?: ")

def extract_data(page, selector, attribute=None,):
    try:
        if page.locator(selector).count() > 0:
            if attribute:
                return page.locator(selector).get_attribute(attribute).strip()
            return page.locator(selector).inner_text().strip()
        return ""
    except Exception as e:
        print(f"Error extracting data: {e}")
        return ""

def extract_reviews_count(page):
    raw_text = extract_data(page, '//span[@aria-label and contains(text(), "reviews")]')
    if raw_text:
        return int(raw_text.strip("()").replace(",", ""))
    return 0
def extract_website(page):
    raw_text =extract_data(page, '//a[@aria-label and contains (text(),"Website")]','href')
    if raw_text:
        return str(raw_text)
    return ""
def extract_average_rating(page):
    raw_text = extract_data(page, '//div[@class="fontDisplayLarge"]')
    if raw_text:
        return float(raw_text)
    return 0.0
def extract_title(page):
    raw_text =extract_data(page, '//button[@class="DkEaL "]')
    if raw_text:
        return str(raw_text)
    return ""
def extract_open_hours(page):
    return extract_data(page, '//div[@aria-label="Hours"]//span[@style]')
def extract_phone(page):
    raw_text =extract_data(page, '//button[contains(@data-item-id, "phone:tel:")]')
    if raw_text:
        return str(raw_text)
    return ""
def extract_star_ratings(page):
    star_ratings = {
        "5 Stars": 0,
        "4 Stars": 0,
        "3 Stars": 0,
        "2 Stars": 0,
        "1 Star": 0,
    }
    rows = page.locator('//tr[@class="BHOKXe"]')
    count = rows.count()

    for i in range(count):
        aria_label = rows.nth(i).get_attribute("aria-label")
        if aria_label:
            parts = aria_label.split(", ")
            stars = parts[0].split()[0]
            reviews = int(parts[1].split()[0])
            star_ratings[f"{stars} Stars"] = reviews

    return star_ratings

def extract_listing_details(page):
    # star_ratings = extract_star_ratings(page)
    return {
        "Name": extract_data(page, '//div[@class="TIHn2 "]//h1'),
        "Address": extract_data(page, '//button[@data-item-id="address"]',"aria-label"),
        "Website":extract_website(page) ,
        "Phone": extract_phone(page),
        "Reviews Count": extract_reviews_count(page),
        # "5 Stars": star_ratings["5 Stars"],
        # "4 Stars": star_ratings["4 Stars"],
        # "3 Stars": star_ratings["3 Stars"],
        # "2 Stars": star_ratings["2 Stars"],
        # "1 Star": star_ratings["1 Star"],
        "Average Rating": extract_average_rating(page),
        "Type": extract_title(page),
        # "Open Hours": extract_open_hours(page),
    }

def scroll_until_target_found(page):
    max_scrolls = 1500
    scroll_attempts = 0

    while scroll_attempts < max_scrolls:
        if page.locator('div.m6QErb.XiKgde.tLjsW.eKbjU').first.count() > 0:
            break
        page.get_by_role("feed").press("ArrowDown")
        if scroll_attempts % 50 == 0:
            page.wait_for_timeout(300)
        scroll_attempts += 1
        
    if scroll_attempts == max_scrolls:
        print("Reached max scroll limit, getting results...")

def write_to_csv(data, filename):
    fieldnames = [
        "Name", "Address", "Website", "Phone", "Reviews Count", "Average Rating", "Type"
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
BLOCK_RESOURCE_TYPES = [
    'beacon',
    'csp_report',
    'font',
    'image',
    'imageset',
    # 'media',
    # 'object',
    # 'texttrack',
    # 'stylesheet',
    # 'script',  
    # 'xhr',
]

BLOCK_RESOURCE_NAMES = [
    'adzerk',
    'analytics',
    'cdn.api.twitter',
    'doubleclick',
    'exelator',
    'facebook',
    'fontawesome',
    'google-analytics',
    'googletagmanager',
]
#intercepting unnecessary requests to boost time 
def intercept_route(route):
    if route.request.resource_type in BLOCK_RESOURCE_TYPES:
        return route.abort()
    if any(key in route.request.url for key in BLOCK_RESOURCE_NAMES):
        return route.abort()
    return route.continue_()

def main():
    parser = argparse.ArgumentParser(description="Scrape business listings from Google Maps.")
    parser.add_argument("search", type=str, help="The search term for Google Maps (e.g., 'restaurants in New York')")
    args = parser.parse_args()

    search = args.search
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent=generated_ua)
        page = context.new_page()
        page.route("**/*", intercept_route)
        try:
            page.goto("https://www.google.com/maps/")
            page.locator("#searchboxinput").fill(search)
            page.locator("#searchboxinput").press("Enter")
            scroll_until_target_found(page)

            listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
            results = []

            for listing in listings:
                listing.click()
                time.sleep(0.5)
                page.wait_for_selector('//div[@class="TIHn2 "]//h1', timeout=5000)
                details = extract_listing_details(page)
                results.append(details)

            filename = f"{args.search.replace(' ', '_')}.csv"
            write_to_csv(results, filename)
            print(f"Data successfully written to '{search}.csv'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()
