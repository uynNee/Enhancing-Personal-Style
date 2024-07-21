# /utils/integrate_link.py
def generate_search_urls(keywords):
    amazon_base_url = "https://www.amazon.com/s?k="

    # Join keywords with '+' for Amazon and '%20' for Shopee
    amazon_keywords = "+".join(keywords)

    amazon_search_url = amazon_base_url + amazon_keywords

    return amazon_search_url
