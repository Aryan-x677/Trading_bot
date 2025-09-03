import os, time, hmac, hashlib, requests
from dotenv import load_dotenv
from logger import log_error, log_info

class Trading_bot:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.base_url = "https://testnet.binancefuture.com"

    def sign(self, params):
        query = "&".join([f"{k}={v}" for k,v in params.items()])
        signature = hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()
        return query + "&signature=" + signature

    def get_open_orders(self, symbol):
        try:
            endpoint = "/fapi/v1/openOrders"
            params = {
                "symbol": symbol,
                "timestamp": int(time.time() * 1000)
            }

            query = self.sign(params)
            url = self.base_url + endpoint + "?" + query
            headers = {"X-MBX-APIKEY": self.api_key}
            r = requests.get(url, headers=headers)
            data = r.json()
            return data
        except Exception as e:
            log_error(f"Error fetching open orders: {e}")
            return None
        
    def create_order(self, symbol, side, quantity):
        try:
            endpoint = "/fapi/v1/order"
            params = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity,
                "timestamp": int(time.time() * 1000)
            }

            query = self.sign(params)
            url = self.base_url + endpoint + "?" + query
            headers = {"X-MBX-APIKEY": self.api_key}

            print("Sending request to:", url)  
            r = requests.post(url, headers=headers)

            data = r.json()
            if "orderId" in data:
                log_info(f"SUCCESS: MARKET {side} {quantity} {symbol} (orderId={data['orderId']})")
            else:
                log_error(f"FAILED: MARKET {side} {quantity} {symbol} → {data}")

            return data
        
        except Exception as e:
            log_error(f"Error placing order: {e}")
            return None
       
    def place_limit_order(self, symbol, side, quantity, price):
        try:

            endpoint = "/fapi/v1/order"
            params = {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "quantity": quantity,
                "price": price,
                "timeInForce": "GTC",
                "timestamp": int(time.time() * 1000)
            }

            query = self.sign(params)
            url = self.base_url + endpoint + "?" + query
            headers = {"X-MBX-APIKEY": self.api_key}

            r = requests.post(url, headers=headers)
            data = r.json()

            if "orderId" in data:
                log_info(f"SUCCESS: LIMIT {side} {quantity} {symbol} @ {price} (orderId={data['orderId']})")
            else:
                log_error(f"FAILED: LIMIT {side} {quantity} {symbol} @ {price} → {data}")

            return data
        
        except Exception as e:
            log_error(f"Error placing LIMIT order: {e}")
            return None
        
    
    def cancel_order(self, symbol, orderId):
        try:

            endpoint = "/fapi/v1/order"
            params = {
                "symbol": symbol,
                "orderId": orderId,
                "timestamp": int(time.time() * 1000)
            }

            query = self.sign(params)
            url = self.base_url + endpoint + "?" + query
            headers = {"X-MBX-APIKEY": self.api_key}
            r = requests.delete(url, headers=headers)
            data = r.json()

            if data.get("status") == "CANCELED":
                log_info(f"SUCCESS: Cancelled order {orderId} for {symbol}")
            else:
                log_error(f"FAILED to cancel order {orderId} for {symbol} → {data}")

            return data
        except Exception as e:
            log_error(f"Error cancelling order: {e}")
            return None
    