import csv
import os

SUMMARY_CSV = "portfolio_summary.csv"

# Pre-defined S&P 500 reference prices (serves as built-in fallback)
DEFAULT_MARKET_PRICES = {
    "AAPL": 182.50,
    "MSFT": 415.20,
    "GOOGL": 142.10,
    "AMZN": 158.40,
    "TSLA": 250.00,
    "NVDA": 890.30,
    "META": 490.15,
    "BRK.B": 410.00,
    "JNJ": 156.80,
    "JPM": 195.50
}

def load_market_dataset():
    """Loads ticker prices from any downloaded CSV dataset in the folder if present."""
    market_prices = DEFAULT_MARKET_PRICES.copy()
    
    # Automatically scan directory for the downloaded S&P 500 dataset
    dataset_file = None
    for fname in os.listdir("."):
        if fname.endswith(".csv") and fname != SUMMARY_CSV:
            dataset_file = fname
            break

    if dataset_file and os.path.exists(dataset_file):
        try:
            with open(dataset_file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row.get("Symbol") or row.get("Ticker") or row.get("symbol")
                    price = row.get("Price") or row.get("Current_Price") or row.get("price")
                    if symbol and price:
                        try:
                            market_prices[symbol.strip().upper()] = float(price)
                        except ValueError:
                            continue
        except Exception:
            pass
            
    return market_prices

def get_portfolio_input():
    """Takes user input for stock symbols, quantities, and buy prices into a dictionary."""
    portfolio = {}
    print("\n--- STOCK PORTFOLIO INPUT ---")
    print("(Enter your holdings. Press Enter with an empty ticker when finished.)")
    
    while True:
        ticker = input("\nEnter Stock Ticker (e.g., AAPL, NVDA, TSLA): ").strip().upper()
        if not ticker:
            if portfolio:
                break
            else:
                print("Please enter at least one holding before continuing.")
                continue

        try:
            shares = float(input(f"Enter share quantity for {ticker}: "))
            buy_price = float(input(f"Enter purchase price per share ($) for {ticker}: "))
            if shares <= 0 or buy_price <= 0:
                print("Quantity and price must be greater than 0.")
                continue
        except ValueError:
            print("Invalid numeric value entered. Please re-enter this stock.")
            continue

        portfolio[ticker] = {
            "shares": shares,
            "buy_price": buy_price
        }
        print(f"Recorded: {shares} shares of {ticker} at ${buy_price:.2f}")

    return portfolio

def calculate_and_export(portfolio, market_prices):
    """Calculates performance metrics, displays console output, and logs to CSV."""
    total_invested = 0.0
    total_current_value = 0.0
    summary_rows = []

    print("\n" + "=" * 90)
    print(f"{'TICKER':<10} {'SHARES':<10} {'BUY PRICE':<12} {'CURRENT':<12} {'CURR VAL':<14} {'P&L ($)':<14} {'GAIN/LOSS (%)'}")
    print("=" * 90)

    for ticker, data in portfolio.items():
        shares = data["shares"]
        buy_price = data["buy_price"]
        current_price = market_prices.get(ticker, buy_price)

        invested = shares * buy_price
        current_val = shares * current_price
        pnl = current_val - invested
        pct_gain_loss = (pnl / invested) * 100 if invested > 0 else 0.0

        total_invested += invested
        total_current_value += current_val

        summary_rows.append({
            "Ticker": ticker,
            "Shares": shares,
            "Buy_Price": f"{buy_price:.2f}",
            "Current_Price": f"{current_price:.2f}",
            "Invested_Capital": f"{invested:.2f}",
            "Current_Value": f"{current_val:.2f}",
            "Gain_Loss_Dollar": f"{pnl:.2f}",
            "Gain_Loss_Pct": f"{pct_gain_loss:.2f}%"
        })

        pnl_sign = "+" if pnl >= 0 else ""
        print(f"{ticker:<10} {shares:<10.2f} ${buy_price:<11.2f} ${current_price:<11.2f} ${current_val:<13.2f} {pnl_sign}${pnl:<13.2f} {pnl_sign}{pct_gain_loss:.2f}%")

    overall_pnl = total_current_value - total_invested
    overall_roi = (overall_pnl / total_invested) * 100 if total_invested > 0 else 0.0

    print("-" * 90)
    print(f"Total Invested Capital  : ${total_invested:,.2f}")
    print(f"Total Current Valuation : ${total_current_value:,.2f}")
    total_sign = "+" if overall_pnl >= 0 else ""
    print(f"Net Portfolio Return    : {total_sign}${overall_pnl:,.2f} ({total_sign}{overall_roi:.2f}%)")
    print("=" * 90)

    # Persist summary logs to external CSV file
    fieldnames = [
        "Ticker", "Shares", "Buy_Price", "Current_Price",
        "Invested_Capital", "Current_Value", "Gain_Loss_Dollar", "Gain_Loss_Pct"
    ]

    with open(SUMMARY_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\n[+] Output logged successfully to '{SUMMARY_CSV}'.")

def main():
    market_prices = load_market_dataset()
    portfolio = get_portfolio_input()
    calculate_and_export(portfolio, market_prices)

if __name__ == "__main__":
    main()