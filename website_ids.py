def web_price(soup):
    """
    All ids of the HTML page for Amazon and/or eBay
    """

    identifiers = [
        'priceblock_ourprice',
        'priceblock_saleprice',
        'priceblock_dealprice',
        'prcIsum'
    ]

    class_identifiers = [
        'a-price-whole',
        'a-offscreen',
    ]

    try:
        for ids in identifiers:
            price_element = soup.find('span', id=ids)
            if price_element:
                return price_element.get_text()
    except AttributeError:
        for classes in class_identifiers:
            price_element = soup.find('span', class_=classes)
            if price_element:
                return price_element.get_text()
    return '£-1'
