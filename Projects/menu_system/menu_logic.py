# menu_logic.py

menu = [
    {"id": 1, "name": "Burger",    "price": 5.99, "category": "Food"},
    {"id": 2, "name": "Pizza",     "price": 8.49, "category": "Food"},
    {"id": 3, "name": "Pasta",     "price": 7.99, "category": "Food"},
    {"id": 4, "name": "Coke",      "price": 1.99, "category": "Drinks"},
    {"id": 5, "name": "Lemonade",  "price": 2.49, "category": "Drinks"},
    {"id": 6, "name": "Ice Cream", "price": 3.49, "category": "Dessert"},
]

cart = []


# Find item by id
def find_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item    # found — return it
        else:
            continue       # not this one — keep looking
    return None            # not found


# Add item to cart
def add_to_cart(item_id):
    item = find_item(item_id)

    if item is None:
        return "Not found"

    for c in cart:
        if c["id"] == item_id:
            c["qty"] = c["qty"] + 1
            return "Added"

    cart.append({"id": item["id"], "name": item["name"], "price": item["price"], "qty": 1})
    return "Added"


# Remove item from cart
def remove_from_cart(item_id):
    i = 0
    while i < len(cart):
        if cart[i]["id"] == item_id:
            cart.pop(i)
            return "Removed"
        else:
            i = i + 1
    return "Not found"


# Update qty — if qty is 0, remove it
def update_qty(item_id, qty):
    if qty <= 0:
        return remove_from_cart(item_id)
    elif qty > 0:
        for c in cart:
            if c["id"] == item_id:
                c["qty"] = qty
                return "Updated"
    return "Not found"


# Get cart total
def get_cart():
    subtotal = 0
    items    = []

    for c in cart:
        if c["qty"] <= 0:
            continue        # skip bad items

        line = c["price"] * c["qty"]
        subtotal = subtotal + line
        items.append({"id": c["id"], "name": c["name"], "price": c["price"], "qty": c["qty"], "line_total": round(line, 2)})

    tax   = round(subtotal * 0.08, 2)
    total = round(subtotal + tax, 2)

    return {"items": items, "subtotal": round(subtotal, 2), "tax": tax, "total": total}


# Clear cart
def clear_cart():
    while len(cart) > 0:
        cart.pop(0)         # keep removing first item until empty


# Place order
def place_order():
    if len(cart) == 0:
        return None

    data = get_cart()
    clear_cart()
    return {"message": "Order placed!", "total": data["total"], "items": len(data["items"])}
