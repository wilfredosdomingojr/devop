from netmiko import ConnectHandler
import yaml

# Load configuration from YAML file
with open("test1.yml", "r") as file:
    config = yaml.safe_load(file)

# Extract router details
router = config['router']

# Establish connection to the router
connection = ConnectHandler(
    host=router['host'],
    username=router['username'],
    password=router['password'],
    device_type=router['device_type']
)

# Build configuration commands
commands = [
    f"interface GigabitEthernet0/0",
    f"ip address {router['management_ip']} 255.255.255.0",
    "no shutdown"
]

for i, ip in enumerate(router['loopbacks'], start=1):
    commands.append(f"interface Loopback{i}")
    commands.append(f"ip address {ip} 255.255.255.255")

# Send commands to the router and display the output
output = connection.send_config_set(commands)
print("Configuration Output:\n")
print(output)

# Save configuration
save_output = connection.save_config()
print("\nConfiguration Saved.")

# Disconnect
connection.disconnect()