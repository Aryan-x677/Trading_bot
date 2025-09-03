# 🚀 Crypto Trading Bot (Binance Futures Testnet)

A simple Python trading bot that interacts with the **Binance Futures Testnet**.  
Supports placing **market orders**, **limit orders**, canceling existing orders, and fetching open orders.  
All actions and errors are logged for easy debugging.

---

## 📦 Features
- Place **Market Orders**
- Place **Limit Orders**
- Cancel orders by ID
- Fetch all open orders
- Separate logging for **orders** and **errors**

---

## ⚙️ Requirements
- Python 3.9+
- Virtual environment recommended

Install dependencies:
```bash
pip install -r requirements.txt

🔑 SETUP:

Clone this repo:

git clone <your-repo-url>
cd trading_bot


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows


Configure environment variables:
Create a .env file (based on .env.example):

BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

▶️ USAGE

Run the bot via app.py with command-line arguments:

1. Place a Market Order
python app.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.002

2. Place a Limit Order
python app.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.002 --price 60000

3. Cancel an Order
python app.py --symbol BTCUSDT --cancel 123456789

4. Get Open Orders
python app.py --symbol BTCUSDT --open-orders

📂 Project Structure
trading_bot/
│── app.py              # CLI entry point
│── binance_client.py   # Trading bot logic
│── logger.py           # Logging setup
│── logs/
│    ├── orders.log     # Successful order logs
│    └── errors.log     # Error logs
│── requirements.txt    # Dependencies
│── .env.example        # Example environment variables

📜 Logs

logs/orders.log → Successful actions

logs/errors.log → API errors or exceptions

Example:
2025-09-03 19:25:14,882 - INFO - SUCCESS: LIMIT BUY 0.002 BTCUSDT @ 59050 (orderId=5637004759)
2025-09-03 19:25:16,441 - ERROR - FAILED: LIMIT BUY 0.001 BTCUSDT @ 59050 → {"code": -4164, "msg": "Order's notional must be no smaller than 100"}
