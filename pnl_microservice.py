import zmq
import time
import json
import datetime
import yfinance as yf

def check_valid_date(date_str):
  try:
    datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return True
  except ValueError:
    return False

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

result = {}

while True:
    req = socket.recv_string()
    data = json.loads(req)
    
    if data["type"] == "current":
      stock = yf.download(data["ticker"], period="1d")
      stock_price = stock["Close"].iloc[-1].item()
      rounded_price = round(stock_price, 2)

      holding = data["cost_basis"] * data["shares"] 
      current_value = data["shares"] * rounded_price

      result = {"gain_loss": 0,
                "percent_change": 0} 

      gain_loss = current_value - holding
      result["gain_loss"] = round(gain_loss, 2)
      result["percent_change"] = round(((current_value - holding) / holding) * 100, 2)
    
    if data["type"] == "historical":
      stock = yf.Ticker(data["ticker"])

      if not check_valid_date(data["date"]):
        print("Incorrect date format, format is in YYYY-MM-DD")
        break

      next_date = (datetime.datetime.strptime(data["date"], "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
      stock_date_data = stock.history(period="1d", start=data["date"], end=next_date)

      if not stock_date_data.empty:
        stock_price = stock_date_data["Close"].iloc[-1].item()
        rounded_price = round(stock_price, 2)
      else:
        print("Date Invalid")
        break

      holding = data["cost_basis"] * data["shares"] 
      historical_value = data["shares"] * rounded_price
      gain_loss = historical_value - holding

      result = {"date": data["date"],
                "gain_loss": 0,
                "percent_change": 0} 

      result["gain_loss"] = round(gain_loss, 2)
      result["percent_change"] = round(((historical_value - holding) / holding) * 100, 2)
    
    if data["type"] == "potential":
      stock = yf.download(data["ticker"], period="1d")
      stock_price = stock["Close"].iloc[-1].item()
      rounded_price = round(stock_price, 2)

      holding = data["cost_basis"] * data["shares"] 
      new_price = rounded_price * (1 + (data["potential_movement"] / 100))
      potential_holding = new_price * data["shares"]

      result = {"gain_loss": 0,
                "percent_change": 0}

      result["gain_loss"] = round(potential_holding - holding, 2)
      result["percent_change"] = round(((potential_holding - holding) / holding) * 100, 2)
      
    socket.send_string(json.dumps(result))
    time.sleep(1)
