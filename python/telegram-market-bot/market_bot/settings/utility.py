def _convert(list_convert):
    """
    Конвертирует список с p[(5,),(8,),...] к [5,8,...]
    """
    return [itm[0] for itm in list_convert]


def total_coast(list_quantity, list_price):
    """
    Считает общую сумму заказа и возвращает результат
    """

    order_total_cost = 0

    for ind, itm in enumerate(list_price):
        order_total_cost += list_quantity[ind]*list_price[ind]

        return order_total_cost


def total_quantity(list_quantity):
    """
    Считает общее количество заказанной единицы товара и возвращает результат
    """
    order_total_quantity = 0

    for itm in list_quantity:
        order_total_quantity += itm

        return order_total_quantity


def get_total_coas(BD):
    """
    Возвращает общую стоимость товара
    """

    all_product_id = BD.select_all_product_id()
    all_price = [BD.select_single_product_price(itm) for itm in all_product_id]
    all_quantity = [BD.select_order_quantity(itm) for itm in all_product_id]
    return total_coast(all_quantity,all_price)


def get_total_quantity(BD):
    """
    Возвращает общее количество заказанной единицы товара
    """
    all_product_id = BD.select_all_product_id()
    all_quantity = [BD.select_order_quantity(itm) for itm in all_product_id]
    return total_quantity(all_quantity)