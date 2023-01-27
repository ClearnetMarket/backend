
def put_online_allowed(item):


    if item.item_title:
        # check item has a title
        if len(item.item_title) <= 6:
            return 'Item Title not Long Enough'
    else:
        return 'Item Title not Long Enough'
    if item.image_one_url_250:
        # Check there is a main image
        if len(item.image_one_url_250) <= 10:
            return 'There must be a main image'
    else:
        return 'There must be a main image'
        
    # Check there is a count greater than 0
    if item.item_count == 0:
        return 'Item count is 0 cannot put online'

    # Check there is an item condition
    if item.item_condition == 0:
        return 'There must be an item condition set.'

    # Check there is a price
    if item.price == 0:
        return 'Item price must be set'

    # Check there is a category
    if item.category_id_0 == 0:
        return 'There must be an item category'

    # check if there is a digital currency selected
    if item.digital_currency_1 is True \
            or item.digital_currency_2 is True \
            or item.digital_currency_3 is True:
        pass
    else:
        return 'Need to select a Digital Currency'

    # Shipping checks
    if item.shipping_free is True \
            or item.shipping_two is True \
            or item.shipping_three is True:
        pass
    else:
        return 'Shipping has not been selected'

    # check if shipping info specified
    # free shipping
    if item.shipping_free is True:
        if len(item.shipping_info_0) > 3:
            pass
        else:
            return 'Free Shipping needs a better description'

    # check if shipping info specified
    # shipping two
   
    if item.shipping_two is True:
        if len(item.shipping_info_2) > 3:
            pass
        else:
            return 'Shipping Two needs a better description'

    # check if shipping info specified
    # shipping three
    if item.shipping_three is True:
        if len(item.shipping_info_3) > 3:
            pass
        else:
            return 'Shipping Three needs a better description'

    return True
