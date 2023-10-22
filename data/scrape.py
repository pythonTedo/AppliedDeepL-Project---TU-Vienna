import os
import re
import html
from typing import Dict, List
import pandas as pd

from tqdm import tqdm
import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
}
BASE_URL = "https://receptite.com/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B7%D0%B8-%D1%81-%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82%D0%B8"

OUT_FILENAME = "bg-recipes.tsv"


def main():
    scraped_data = {
        "title": [],
        "rating": [],
        "complexity": [],
        "products": [],
        "description": [],
    }
    response = requests.get(BASE_URL, headers=HEADERS).text
    
    # Get HTML with all recipe categories.
    base_html = re.findall(r"shapka_head.+?search_konteineri\"([^~]+)dude2_head", response)[0]
    categories_urls = re.findall(r"(https:\/\/receptite\.com\/.+?)\"", base_html)

    progressbar = tqdm(categories_urls)

    # Scrape each category in `BASE_URL`.
    for cat_url in progressbar:
        cat_html = requests.get(cat_url, headers=HEADERS).text
        try:
            n_pages = get_n_pages(cat_html)
        # When the category has only a single page of recipes.
        except Exception:
            n_pages = 1

        progressbar.set_description(f"Num. pages: {n_pages}")

        # Iterate through each page in the category.
        for page in range(n_pages):
            page_url = f"{cat_url}/{page + 1}"
            page_html = requests.get(page_url, headers=HEADERS).text

            recipes_urls = re.findall(r"class=\"zagS\".*?><a[^>]+href=\"([^\"]+)\"", page_html)
        
            # Scrape each recipe in `cat_url`.
            for recipe_url in recipes_urls:
                try:
                    recipe_data = scrape_recipe(recipe_url)
                    # print(f"Downloaded recipe: {recipe_data['title']}")
                    scraped_data = append_scraped_data(scraped_data, recipe_data)
                except Exception as e:
                    print(f"Error occurred: {e}")

    df = pd.DataFrame.from_dict(data=scraped_data)
    print("Dataframe:\n", df.head())

    df.to_csv(OUT_FILENAME, sep="\t")
    print(f"Output file created at {OUT_FILENAME}")


def get_n_pages(category_html):
    pages_block = re.findall(r"class=\"pages_bar\"[^>]+>(.+?)<\/div", category_html)[0]
    last_page_num = re.findall(r"<a\s+href=\"[^\"]+\/(\d+)\"\s*>\s*\d+\s*<", pages_block)[-1]

    return int(last_page_num)


def scrape_recipe(recipe_url: str):
    src = requests.get(recipe_url, headers=HEADERS).text
    src = html.unescape(src)

    title = get_title(src)
    rating = get_rating(src)
    complexity = get_complexity(src)
    products = get_products(src)

    description = get_description(src)

    return {
        "title": title, 
        "rating": rating, 
        "complexity": complexity, 
        "products": products, 
        "description": description,
    }


def get_title(src: str) -> str:
    title = re.findall(r"itemprop=\"name\">([^<]+)<", src)[0]
    return title


def get_rating(src: str) -> str:
    rating = re.findall(r"Рейтинг.+?graphs\/rating\/([^\.]+)\.png", src)[0]
    return rating


def get_complexity(src: str) -> str:
    complexity = re.findall(r"Сложност:[^~]+?hats\/hat([^\.]+)\.png", src)[0]
    return complexity


def get_products(src: str) -> str:
    products = re.findall(r"div[^>]+?class=\"recepta_produkti\">(.+?)<\/div", src)[0]
    # Replace </li> with [EOL], which is a tag for end of line.
    products = re.sub(r"<\/li>", "[EOL]", products)
    # Remove the symbol •.
    products = re.sub(r"•\s+", "", products)
    # Remove all HTML tags.
    products = re.sub(r"<.+?>", "", products)
    # Remove the final [EOP] tag.
    products = re.sub(r"\[EOL\]$", "", products)

    return products


def get_description(src: str) -> str:
    recipe = re.findall(r"recepta_prigotviane\"[^>]+?>([^<]+)<", src)[0]
    return recipe


def append_scraped_data(scraped_data: Dict[str, List[str]], recipe_data: Dict[str, str]):
    for dtype in scraped_data:
        scraped_data[dtype].append(recipe_data[dtype])

    return scraped_data


if __name__ == "__main__":
    main()