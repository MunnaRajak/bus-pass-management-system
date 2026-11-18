"""
Bus Pass Management System
Language  : Python 3
Concepts  : Lists, Dictionaries, Functions, File Handling
"""

# Import the 'os' module, which lets us check whether a file exists on disk
import os

# Name of the file where all bus passes are saved
DATA_FILE = "buspass.txt"
# Discount given to students (25% off the fee)
STUDENT_DISCOUNT = 0.25
# The first pass issued gets the number 101, so its ID is BP101
FIRST_PASS_NUMBER = 101
# The only categories a passenger can belong to
VALID_CATEGORIES = ["General", "Student"]

# A dictionary that stores each pass type with its validity in days and its fee in rupees
PASS_TYPES = {
    # Monthly pass is valid for 30 days and costs Rs. 500
    "Monthly":   {"days": 30,  "fee": 500},
    # Quarterly pass is valid for 90 days and costs Rs. 1350
    "Quarterly": {"days": 90,  "fee": 1350},
    # Yearly pass is valid for 365 days and costs Rs. 4800
    "Yearly":    {"days": 365, "fee": 4800},
}


# ---------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------

# This function formats the fee amount to display as a string with two decimal places if necessary
def format_fee(amount):
    # Check if the amount is a whole number (for example 3600.0 equals int 3600)
    if amount == int(amount):
        # Convert the whole number to a string without decimal places, so 3600.0 becomes "3600"
        return str(int(amount))
    # Otherwise show exactly two decimal places, so 1012.5 becomes "1012.50"
    return f"{amount:.2f}"


# This function cleans up the route the user typed so it is always stored as "Route <number>"
def normalize_route(text):
    # Remove any extra spaces at the start and end of the text the user typed
    text = text.strip()
    # If the user typed only digits like "5", add the word "Route " in front of it
    if text.isdigit():
        return "Route " + text
    # If the user typed something starting with "route" (in any case), rebuild it as "Route <number>"
    if text.lower().startswith("route"):
        # Take everything after the first 5 characters ("route"), remove spaces, and add it after "Route "
        return "Route " + text[5:].strip()
    # For any other text, return it unchanged
    return text


# This function works out the fee for a pass based on its type and the passenger's category
def calculate_fee(pass_type, category):
    # Read the base fee of this pass type from the PASS_TYPES dictionary
    fee = PASS_TYPES[pass_type]["fee"]
    # If the passenger is a student, reduce the fee by the discount
    if category == "Student":
        # Multiply the fee by (1 - 0.25) = 0.75 to get 75% of the original price
        fee = fee * (1 - STUDENT_DISCOUNT)
    # Send the final fee back to the caller
    return fee


# This function creates the next pass ID, such as BP101, BP102 and so on
def next_pass_id(passes):
    # If no passes exist yet, the first ID is BP101
    if not passes:
        return f"BP{FIRST_PASS_NUMBER}"
    # Look at every pass ID, remove the first two letters ("BP"), convert the rest to a number, and take the largest
    last_number = max(int(p["id"][2:]) for p in passes)
    # Add 1 to the largest number to get the next free ID
    return f"BP{last_number + 1}"


# This function searches the list of passes and returns the one with the matching ID
def find_pass(passes, pass_id):
    # Go through every pass dictionary in the list one by one
    for p in passes:
        # Compare the IDs in uppercase so that "bp101" and "BP101" match
        if p["id"].upper() == pass_id.upper():
            # Return the matching pass dictionary immediately
            return p
    # If the loop finishes without a match, return None (meaning "not found")
    return None


# This function builds the one-line text that describes a pass, used by search and view-all
def format_pass_line(p):
    # Join the ID, name, route, type and fee with " | " between them and return the resulting text
    return (f"{p['id']} | {p['name']} | {p['route']} | {p['type']} | "
            f"Fee: Rs. {format_fee(p['fee'])}")


# ---------------------------------------------------------------
# File handling
# ---------------------------------------------------------------

# This function reads buspass.txt and converts every line into a pass dictionary
def load_passes():
    # Start with an empty list that will hold all the passes
    passes = []
    # If the file does not exist yet (first time running the program), return the empty list
    if not os.path.exists(DATA_FILE):
        return passes

    # Open the file in read mode ("r"); the 'with' block closes it automatically at the end
    with open(DATA_FILE, "r") as f:
        # Read the file one line at a time
        for line in f:
            # Remove spaces and the newline character at the end of the line
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            # Split the line at every "|" and remove extra spaces around each piece
            parts = [part.strip() for part in line.split("|")]
            # If the line has fewer than 5 pieces it is broken, so skip it
            if len(parts) < 5:
                continue

            # Give names to the first five pieces: ID, name, route, pass type and fee text
            pass_id, name, route, pass_type, fee_text = parts[:5]
            # If a category is written in the file use it, otherwise assume "General"
            category = parts[5] if len(parts) >= 6 else "General"
            # If the number of days is written in the file use it, otherwise look it up from the pass type
            if len(parts) >= 7:
                # Convert the days text to an integer number
                days = int(parts[6])
            else:
                # Get the days for this pass type from PASS_TYPES (0 if the type is unknown)
                days = PASS_TYPES.get(pass_type, {}).get("days", 0)
            # Remove "Rs." and any commas from the fee text, then convert it to a decimal number
            fee = float(fee_text.replace("Rs.", "").replace(",", "").strip())

            # Build a dictionary for this pass and add it to the list
            passes.append({
                "id": pass_id,        # pass ID, for example BP101
                "name": name,         # passenger name
                "route": route,       # route, for example Route 5
                "type": pass_type,    # Monthly, Quarterly or Yearly
                "category": category, # General or Student
                "fee": fee,           # fee paid, as a number
                "days": days,         # number of days the pass is valid
            })
    # Return the full list of passes to the caller
    return passes


# This function saves every pass in the list back into buspass.txt
def save_passes(passes):
    # Open the file in write mode ("w"), which erases the old contents and writes fresh ones
    with open(DATA_FILE, "w") as f:
        # Go through each pass dictionary in the list
        for p in passes:
            # Write one line in the format: ID | Name | Route | Type | Rs. Fee | Category | Days
            f.write(f"{p['id']} | {p['name']} | {p['route']} | {p['type']} | "
                    f"Rs. {format_fee(p['fee'])} | {p['category']} | {p['days']}\n")


# ---------------------------------------------------------------
# Main features
# ---------------------------------------------------------------

# This function asks the user for details and issues a new bus pass
def issue_pass(passes):
    # Print a heading for this section
    print("\n--- Issue New Pass ---")
    # Ask for the passenger's name and remove extra spaces
    name = input("Enter passenger name: ").strip()
    # If the name is empty, show an error and stop without issuing a pass
    if not name:
        print("Name cannot be empty. Pass not issued.")
        return

    # Ask for the route and remove extra spaces
    route_input = input("Enter route (e.g. Route 5 or 5): ").strip()
    # If the route is empty, show an error and stop
    if not route_input:
        print("Route cannot be empty. Pass not issued.")
        return
    # Convert the route into the standard "Route <number>" format
    route = normalize_route(route_input)

    # Ask for the pass type, remove spaces, and capitalise the first letter (so "monthly" becomes "Monthly")
    pass_type = input("Enter pass type (Monthly/Quarterly/Yearly): ").strip().title()
    # If the type is not one of the keys in PASS_TYPES, show an error and stop
    if pass_type not in PASS_TYPES:
        print("Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued.")
        return

    # Ask for the category and capitalise it so "student" becomes "Student"
    category = input("Enter category (General/Student): ").strip().title()
    # If the category is not in the list of valid categories, show an error and stop
    if category not in VALID_CATEGORIES:
        print("Invalid category. Choose General or Student. Pass not issued.")
        return

    # Create a dictionary that holds all details of the new pass
    new_pass = {
        "id": next_pass_id(passes),                    # generate the next free ID
        "name": name,                                  # the passenger's name
        "route": route,                                # the cleaned-up route
        "type": pass_type,                             # the pass type
        "category": category,                          # the passenger's category
        "fee": calculate_fee(pass_type, category),     # the fee after any discount
        "days": PASS_TYPES[pass_type]["days"],         # validity taken from the pass type
    }
    # Add the new pass to the end of the list
    passes.append(new_pass)
    # Save the updated list to the file so the pass is not lost
    save_passes(passes)

    # Show a confirmation message with the ID, details, fee and validity
    print(f"Pass issued. ID: {new_pass['id']} | {name} | {route} | {pass_type} | "
          f"Fee: Rs. {format_fee(new_pass['fee'])} | Valid: {new_pass['days']} days")


# This function renews an existing pass found by its ID
def renew_pass(passes):
    # Print a heading for this section
    print("\n--- Renew Pass ---")
    # Ask for the ID of the pass to renew and remove extra spaces
    pass_id = input("Enter pass ID to renew: ").strip()
    # Search the list for a pass with this ID
    p = find_pass(passes, pass_id)
    # If no pass was found, show an error and stop
    if p is None:
        print(f"No pass found with ID {pass_id.upper()}.")
        return

    # Renewal keeps the same type and category, so recalculate the fee for them
    p["fee"] = calculate_fee(p["type"], p["category"])
    # Reset the validity period to the full number of days for this pass type
    p["days"] = PASS_TYPES[p["type"]]["days"]
    # Save the updated list to the file
    save_passes(passes)

    # Show a confirmation message with the renewed details
    print(f"Pass renewed. ID: {p['id']} | {p['name']} | {p['route']} | {p['type']} | "
          f"Fee: Rs. {format_fee(p['fee'])} | Valid: {p['days']} days")


# This function finds a pass by its ID and displays it
def search_pass(passes):
    # Print a heading for this section
    print("\n--- Search Pass ---")
    # Ask for the pass ID and remove extra spaces
    pass_id = input("Enter pass ID: ").strip()
    # Look for the pass in the list
    p = find_pass(passes, pass_id)
    # If it was not found, show an error message
    if p is None:
        print(f"No pass found with ID {pass_id.upper()}.")
    # Otherwise print the pass details on one line
    else:
        print(format_pass_line(p))


# This function displays every pass in the list
def view_all_passes(passes):
    # Print a heading for this section
    print("\n--- All Passes ---")
    # If the list is empty, tell the user and stop
    if not passes:
        print("No passes issued yet.")
        return
    # Go through every pass and print it on its own line
    for p in passes:
        print(format_pass_line(p))


# This function prints the main menu options
def show_menu():
    # Print a title line for the menu
    print("\n===== BUS PASS MANAGEMENT SYSTEM =====")
    # Print each menu option
    print("1. Issue new pass")
    print("2. Renew pass")
    print("3. Search pass by ID")
    print("4. View all passes")
    print("5. Exit")


# This is the main function that runs the program
def main():
    # Load all existing passes from the file once, when the program starts
    passes = load_passes()

    # Keep repeating the menu until the user chooses Exit
    while True:
        # Show the menu options
        show_menu()
        # Read the user's choice and remove extra spaces
        choice = input("Choose an option (1-5): ").strip()

        # If the user chose 1, call the function that issues a new pass
        if choice == "1":
            issue_pass(passes)
        # If the user chose 2, call the function that renews a pass
        elif choice == "2":
            renew_pass(passes)
        # If the user chose 3, call the function that searches for a pass
        elif choice == "3":
            search_pass(passes)
        # If the user chose 4, call the function that shows all passes
        elif choice == "4":
            view_all_passes(passes)
        # If the user chose 5, print a goodbye message and leave the loop to end the program
        elif choice == "5":
            print("Thank you for using the Bus Pass Management System.")
            break
        # For any other input, show an error and show the menu again
        else:
            print("Invalid option. Please choose 1 to 5.")


# Start the program only when this file is run directly (not when it is imported elsewhere)
if __name__ == "__main__":
    # Call the main function to start the program
    main()