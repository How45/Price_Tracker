def web_price(soup):
    """All ids of the HTML page for Amazon and eBay"""
    identifiers = [
        'priceblock_ourprice',
        'priceblock_saleprice',
        'priceblock_dealprice',
        'a-price-whole',
        'a-offscreen',
        'prcIsum'
    ]

    for identifier in identifiers:
        price_element = soup.find('span', id=identifier, class_='a-price-whole' if identifier == 'a-offscreen' else None)
        if price_element:
            return price_element.get_text()
    return '£-1'
