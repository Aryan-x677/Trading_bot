import argparse
from binance_client import Trading_bot

parser = argparse.ArgumentParser(description="Crypto Trading Bot")

parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
parser.add_argument("--side", type=str, choices=["BUY", "SELL"], help="Order side")
parser.add_argument("--qty", type=float, help="Order quantity")
parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], help="Order type")
parser.add_argument("--price", type=float, help="Price for LIMIT orders only")

parser.add_argument("--cancel", type=int, help="Cancel an order by ID")
parser.add_argument("--open-orders", action="store_true", help="List open orders")

args = parser.parse_args()

bot = Trading_bot()

if args.cancel:
    result = bot.cancel_order(symbol=args.symbol, orderId=args.cancel)
    if result.get("status") == "CANCELED":
        print(f"✅ Successfully canceled order {args.cancel} for {args.symbol}")
    else:
        print(f"❌ Failed to cancel order {args.cancel}: {result}")

elif args.open_orders:
    result = bot.get_open_orders(symbol=args.symbol)
    if isinstance(result, list) and result:
        print(f"📋 Open orders for {args.symbol}:")
        for order in result:
            print(f"  - {order['side']} {order['origQty']} {order['symbol']} @ {order['price']} (status: {order['status']})")
    elif result == []:
        print(f"No open orders for {args.symbol}")
    else:
        print(f"❌ Failed to fetch open orders: {result}")

elif args.type == "MARKET":
    if not args.side or not args.qty:
        parser.error("--side and --qty are required for MARKET orders")
    result = bot.create_order(symbol=args.symbol, side=args.side, quantity=args.qty)
    if "orderId" in result:
        print(f"✅ MARKET {args.side} order placed for {args.qty} {args.symbol} (orderId={result['orderId']})")
    else:
        print(f"❌ Failed to place MARKET order: {result}")

elif args.type == "LIMIT":
    if not args.price or not args.side or not args.qty:
        parser.error("--price, --side, --qty are required for LIMIT orders")
    result = bot.place_limit_order(symbol=args.symbol, side=args.side, quantity=args.qty, price=args.price)
    if "orderId" in result:
        print(f"✅ LIMIT {args.side} order placed for {args.qty} {args.symbol} at {args.price} (orderId={result['orderId']})")
    else:
        print(f"❌ Failed to place LIMIT order: {result}")
