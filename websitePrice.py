def webPrice(soup):
    try: 
        return soup.find("span",id="priceblock_ourprice").get_text()
    except:
        pass
    try:
        return soup.find("span",id="priceblock_saleprice").get_text()
    except:
        pass
    try:
        return soup.find("span",id="priceblock_dealprice").get_text()
    except:
        pass
    try:
        return soup.find("span",class_="a-price-whole").get_text()
    except:
        pass
    try:
        return soup.find("span",class_="a-offscreen").get_text()
    except:
        pass
    # Ebay
    try:
        return soup.find("span",id="prcIsum").get_text()
    except:
        return "£-1"