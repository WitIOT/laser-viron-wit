import socket
import threading
import logging
import random  # Import random module for generating random numbers

# Initial QSDELAY value
qsdelay_value = 220  # Default value set to 220 microseconds
status = "Prepare"  # Default status

# Network settings
network_settings = {
    "GWIPADDR": "192.168.1.1",
    "IDHCP": 0,
    "IPADDR": "192.168.1.100",
    "IPORT": 23,
    "MACID": "00:11:22:33:44:55",
    "NETMASK": "255.255.255.0",
    "SETPASS": "default"
}

# Setup logging
logging.basicConfig(filename='telnet_server.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_client(client_socket):
    global qsdelay_value  # Declare qsdelay_value as global
    global status
    
    try:
        welcome_message = (
            "Welcome to the simulated Telnet server.\n"
        )
        client_socket.send(welcome_message.encode())
        logging.info("Sent welcome message to client")

        buffer = ""

        while True:
            data = client_socket.recv(1024).decode()
            buffer += data  # Collect incoming data

            if '\n' in buffer or '\r' in buffer:  # Process only when Enter is pressed
                command = buffer.strip()  # Strip any leading/trailing whitespace
                buffer = ""  # Clear the buffer for the next command
                
                # Remove the leading '$' from the command if it exists
                if command.startswith("$"):
                    command = command[1:]

                # Log the command received
                logging.info(f"Received command: {command}")

                # Process the command
                if command == "HELP":
                    response = (
                        "Available commands: help, status, standby, fire, stop, echo, uvill, frecall, dtrig, qstrig, "
                        "qson, dfreq, qsdivby, qsdelay, qspre, burst, bstof, bston, term, dpw, dcurr, oven1, oven2, "
                        "capv, shot, ushot, ltempf, dtempf, ltvers, lcvres, model, serial, gwipaddr, idhcp, ipaddr, "
                        "iport, login, logout, macid, netmask, netsave, npara, setpass\n"
                    )
                elif command.startswith("STATUS ?"):
                    response = f"{status}\n"
                elif command == "STANDBY":
                    status = "Standby Now"
                    response = f"{status}\n"
                elif command == "FIRE":
                    status = "Laser Fire !"
                    response = f"{status}\n"
                elif command == "STOP":
                    status = "Laser Stop !"
                    response = f"{status}\n"
                elif command.startswith("QSDELAY ?"):
                    response = f"{qsdelay_value}\n"
                elif command.startswith("QSDELAY "):
                    try:
                        new_value = int(command.split()[1])
                        qsdelay_value = new_value
                        response = f"{qsdelay_value}\n"
                    except ValueError:
                        response = "Invalid QSDELAY value. Please enter an integer.\n"
                elif command.startswith("LTEMF ?"):
                    # Generate a random temperature between 15 and 30
                    random_temperature = random.randint(15, 30)
                    response = f"{random_temperature}\n"
                elif command.startswith("GWIPADDR ?"):
                    response = f"GWIPADDR is currently set to {network_settings['GWIPADDR']}.\n"
                elif command.startswith("GWIPADDR "):
                    network_settings["GWIPADDR"] = command.split()[1]
                    response = f"GWIPADDR set to {network_settings['GWIPADDR']}.\n"
                elif command.startswith("IDHCP ?"):
                    response = f"IDHCP is currently set to {network_settings['IDHCP']}.\n"
                elif command.startswith("IDHCP "):
                    network_settings["IDHCP"] = int(command.split()[1])
                    response = f"IDHCP set to {network_settings['IDHCP']}.\n"
                elif command.startswith("IPADDR ?"):
                    response = f"IPADDR is currently set to {network_settings['IPADDR']}.\n"
                elif command.startswith("IPADDR "):
                    network_settings["IPADDR"] = command.split()[1]
                    response = f"IPADDR set to {network_settings['IPADDR']}.\n"
                elif command.startswith("IPORT ?"):
                    response = f"IPORT is currently set to {network_settings['IPORT']}.\n"
                elif command.startswith("IPORT "):
                    network_settings["IPORT"] = int(command.split()[1])
                    response = f"IPORT set to {network_settings['IPORT']}.\n"
                elif command == "LOGIN":
                    response = "Login successful.\n"
                elif command == "LOGOUT":
                    response = "Session closed.\n"
                    client_socket.send(response.encode())
                    logging.info("Client logged out, session closed.")
                    break
                elif command == "MACID ?":
                    response = f"MACID is {network_settings['MACID']}.\n"
                elif command.startswith("NETMASK ?"):
                    response = f"NETMASK is currently set to {network_settings['NETMASK']}.\n"
                elif command.startswith("NETMASK "):
                    network_settings["NETMASK"] = command.split()[1]
                    response = f"NETMASK set to {network_settings['NETMASK']}.\n"
                elif command == "NETSAVE":
                    response = "Network settings saved.\n"
                elif command == "NPARA ?":
                    response = (
                        f"GWIPADDR={network_settings['GWIPADDR']}, IDHCP={network_settings['IDHCP']}, "
                        f"IPADDR={network_settings['IPADDR']}, IPORT={network_settings['IPORT']}, "
                        f"MACID={network_settings['MACID']}, NETMASK={network_settings['NETMASK']}.\n"
                    )
                elif command.startswith("SETPASS "):
                    network_settings["SETPASS"] = command.split()[1]
                    response = "Password updated successfully.\n"
                else:
                    response = "Unknown command. Type 'help' for a list of commands.\n"

                logging.info(f"Sending response: {response.strip()}")
                client_socket.send(response.encode())

    except (ConnectionResetError, BrokenPipeError):
        logging.error("Client disconnected abruptly.")
    finally:
        client_socket.close()
        logging.info("Connection closed with client.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 23))
    server.listen(5)
    logging.info("Server started on port 23")

    while True:
        client_socket, addr = server.accept()
        logging.info(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
