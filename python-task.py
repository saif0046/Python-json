import json


# Function to load JSON data from a file
def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Function to manipulate the JSON data
def manipulate_data_from_json(json_data):
    # Access the assignment results
    assignment_results = json_data.get("assignment_results", [])

    # Ensure there's data to process
    if not assignment_results:
        return None, None, None, None

    # Extract the shown_price dictionary and taxes from the first assignment result
    result = assignment_results[0]
    shown_price = result.get("shown_price", {})
    net_price = result.get("net_price", {})
    taxes_str = result.get("ext_data", {}).get("taxes", "{}")
    taxes = json.loads(taxes_str) if taxes_str else {}

    # 1. Find the cheapest price and corresponding room
    cheapest_price = None
    cheapest_room = None
    for room, price in shown_price.items():
        price = float(price)  # Convert string price to float for comparison
        if cheapest_price is None or price < cheapest_price:
            cheapest_price = price
            cheapest_room = room

    # Get the number of guests
    number_of_guests = result.get("number_of_guests", 0)

    # 2. Calculate the total price (Net price + Taxes) for all rooms
    total_prices = {}
    tax_total = sum(float(value) for value in taxes.values())  # Sum all taxes
    for room, net in net_price.items():
        total_prices[room] = float(net) + tax_total

    # Return results
    return cheapest_price, cheapest_room, number_of_guests, total_prices


# Load the JSON data from a local file
file_path = 'C:\\Users\\HP\\Downloads\\Python-task.json'  # Replace with your actual file path
json_data = load_json_from_file(file_path)

# Process the JSON data
result = manipulate_data_from_json(json_data)

# Use the returned results
if result:
    cheapest_price, cheapest_room, number_of_guests, total_prices = result

    # Output in the required order
    outputs = []
    # 1. Cheapest price
    outputs.append(f"The cheapest price is {cheapest_price:.2f} USD.") # .2f means to round up to two decimal places

    # 2. Room type and number of guests for the cheapest price
    outputs.append(f"The cheapest room is '{cheapest_room}' for {number_of_guests} guest(s), priced at {cheapest_price:.2f} USD")

    # 3. Total price (Net price + Taxes) for all rooms
    outputs.append("Total price (Net + Taxes) for all rooms:")
    for room, total in total_prices.items():
        outputs.append(f"  - Room Type: {room}, Total Price: {total:.2f} USD")

    # Join and print the final output, uncomment the below code to check the output in the terminal
    # print("\n".join(outputs))
