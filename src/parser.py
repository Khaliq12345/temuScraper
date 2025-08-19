from typing import List
from selectolax.parser import HTMLParser, Node
from src.model import Good


def extract_one_good(el: Node) -> Good:
    # Title
    title_el = el.css_first("._2D9RBAXL")
    title = title_el.text(strip=True) if title_el else None

    # Price
    price_el = el.css_first("._2de9ERAH")
    price = price_el.text(strip=True) if price_el else None

    # Cents
    cents_el = el.css_first("._3SrxhhHh")
    if price and cents_el:
        price += cents_el.text(strip=True)

    # Market Price
    market_price_el = el.css_first("._3TAPHDOX")
    market_price = market_price_el.text(strip=True) if market_price_el else None

    # Image
    image_el = el.css_first(".wxWpAMbp")
    image = image_el.attributes.get("src") if image_el else None

    # Product link
    link_el = el.css_first("a._2Tl9qLr1")
    link = link_el.attributes.get("href") if link_el else None
    if link and not link.startswith("http"):
        link = "https://www.temu.com/" + link.lstrip("/")

    # Total Sold
    sold_parts = el.css("._3vfo0XTx")
    total_sold = (
        " ".join([part.text(strip=True) for part in sold_parts]) if sold_parts else ""
    )

    # Créer un objet Good
    good = Good(
        title=title,
        price=price,
        image=image,
        product_link=link,
        market_price=market_price,
        total_sold=total_sold,
    )
    return good


def extract_goods_from_html(page_html: str) -> List[Good]:
    goods_list: List[Good] = []

    # Parse HTML avec Selectolax
    tree = HTMLParser(page_html)

    # Trouver tous les items
    goods = tree.css(".EKDT7a3v")
    print(f"Got {len(goods)} new goods !")

    for el in goods:
        good = extract_one_good(el)
        try:
            goods_list.append(good)
        except Exception as e:
            print(f"Erreur de parsing d'un item : {e}")
            continue

    print("Parsing Ended")
    return goods_list
