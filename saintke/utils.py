import yfinance as yf

def fetch_stock_data(symbol, period='1d', interval='1m'):
    """
    Fetch real-time stock data for a given symbol from Yahoo Finance.
    :param symbol: Stock symnbol,
    :param period: Period of data,
    :param interval: Interval of data,
    :return: pandas DataFrame with stock data.
    """
    stock = yf.Ticker(symbol)
    data = stock.history(period=period, interval=interval)
    return data

def calculate_reward(predicted_price, actual_price, action_taken):
    """
    Calculates the reward based on the action taken and the actual price change
    :param predicted_price: Price predicted by the model.
    :param actual_price: Actual price of the stock at prediction time
    :param action_taken: Action chosen by the agent("BUY","SELL","HOLD").
    :return: A numerical reward based on the success of the action.
    """
    #Define a basic reward structure
    price_change = actual_price - predicted_price

    if action_taken == "BUY":
        if price_change > 0:
            return price_change # Reward based on the profit made
        else:
            return price_change #penalize for loss
        
    elif action_taken == "SELL":
        if price_change < 0:
            return abs(price_change) # Reward for selling before a drop
        else:
            return -price_change #penalize for missing gains
    
    elif action_taken == "HOLD":
        return 0 # Neutral reward for holding
    return 0 # Default if action is neutral