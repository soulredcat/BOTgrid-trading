
def place_order(side, amount, price):
    order = None
    try:
        order = exchange.create_order(
            symbol=symbol, 
            type='limit', 
            side=side, 
            amount=amount / price,
            price=price
        )
        print(f"Placed {side} order for {amount / price} {symbol} at {price}")
    except Exception as e:
        print(f"Error placing order: {str(e)}")
    return order


def order_exists(price, side):
    open_orders = exchange.fetch_open_orders(symbol)
    for order in open_orders:
        if float(order['price']) == price and order['side'] == side:
            return True
    return False

def create_dynamic_grid(current_price, percentage_step, levels_up_down=5):
    levels = []

    for i in range(1, levels_up_down + 1):
        price_up = current_price * (1 + (percentage_step / 100) * i)
        price_down = current_price * (1 - (percentage_step / 100) * i)
        levels.append(price_up)
        levels.append(price_down)
    return sorted(levels)   

def run_custom_price_grid():
    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            print(f"Current price: {current_price}")

            for price in custom_price_levels:
                
                if current_price <= price and not order_exists(price, 'buy'):
                    place_order('buy', investment_amount, price)

                
                if current_price >= price and not order_exists(price, 'sell'):
                    place_order('sell', investment_amount, price)

            time.sleep(60)

        except Exception as e:
            print(f"Error in grid bot: {str(e)}")
            time.sleep(60)


if __name__ == "__main__":
    run_custom_price_grid()