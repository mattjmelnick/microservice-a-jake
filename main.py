import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def send_receive_request(req):
  print()
  print("Sending request...")
  print()
  socket.send_string(json.dumps(req))
  response = socket.recv_string()
  response_data = json.loads(response)

  if req["type"] == "current":
    print(f"Gain/Loss: ${response_data["gain_loss"]}")
    print(f"Percent Change: {response_data["percent_change"]}%")
  
  if req["type"] == "historical":
    print(f"Date: {response_data["date"]}")
    print(f"Gain/Loss: ${response_data["gain_loss"]}")
    print(f"Percent Change: {response_data["percent_change"]}%")

  if req["type"] == "potential":
    print(f"Potential Gain/Loss: ${response_data["gain_loss"]}")
    print(f"Potential Percent Change: {response_data["percent_change"]}%")

while True:
  user_input = input("Enter 'current', 'historical', or 'potential': ")
  try:
    user_input = user_input
    if user_input == "current" or user_input == "historical" or user_input == "potential":
      break
  except ValueError:
    print("Enter 'current', 'historical', or 'potential': ")

request = {}
if user_input == "current":
  request["type"] = "current"
  request["ticker"] = input("Enter ticker (no $): ")
  request["shares"] = int(input("Enter shares (integer): "))
  request["cost_basis"] = float(input("Enter cost basis (float): "))

if user_input == "historical":
  request["type"] = "historical"
  request["ticker"] = input("Enter ticker (no $): ")
  request["shares"] = int(input("Enter shares (integer): "))
  request["cost_basis"] = float(input("Enter cost basis (float): "))
  request["date"] = input("Enter date (format YYYY-MM-DD): ")

if user_input == "potential":
  request["type"] = "potential"
  request["ticker"] = input("Enter ticker (no $): ")
  request["shares"] = int(input("Enter shares (integer): "))
  request["cost_basis"] = float(input("Enter cost basis (float): "))
  request["potential_movement"] = float(input("Enter potential movement (percentage): "))

send_receive_request(request)