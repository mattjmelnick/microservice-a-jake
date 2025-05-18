# Microservice A Implementation

This microservice calculates 3 different profit and loss scenarios for a stock based on:

* Current Price
* Historical Date
* Potential PnL

The main program communicates with the microservice through the ZeroMQ messaging library. The microservice uses the YFinance Python API library to request and receive stock information.

---
## Requesting Data

The user will be prompted for a keyword to request profit and loss information. These keywords are self-identifying:

* "current"
* "historical"
* "potential"

Once the program has received the keyword, the user will be prompted to enter values for the request JSON object.

The main program then sends the request JSON object through the ZeroMQ socket to the microservice.

Example request for "current" profit and loss information based on the current stock price:

    # after prompting for PnL scenario and getting user input

    request = {"type": "current",       # string
               "ticker": "aapl",        # string
               "shares": 10,            # int
               "cost_basis": 123.45}    # float

    socket.send_string(json.dumps(req))

The microservice assumes the request values are in the correct format and have the correct type.
___

## Receiving Data

Once the microservice receives and uses the request data to call the YFinance API, it will calculate the profit/loss for the given scenario based on the requested stock price. The microservice will then create a response JSON object with the resulting calculations and send it back to the main program.

    # right below the request in the main program    

    response = socket.recv_string()
    response_data = json.loads(response)

    # the result object from the microservice file

    # result = {"gain_loss": 878.1,
    #           "percent_change": 71.13} 

    if req["type"] == "current":
      print(f"Gain/Loss: ${response_data["gain_loss"]}")
      print(f"Percent Change: {response_data["percent_change"]}%")

    # output

    # Gain/Loss: $878.1
    # Percent Change: 71.13%

___

## UML Diagram

![UML Diagram] (/uml-diagram.png)