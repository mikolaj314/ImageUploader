import json

# Load the JSON data from default_configs.json
with open("default_configs.json", "r") as json_file:
    config_data = json.load(json_file)

# Extract the values
MIN_EXPIRY_LINK_TIME = config_data.get("MIN_EXPIRY_LINK_TIME")
MAX_EXPIRY_LINK_TIME = config_data.get("MAX_EXPIRY_LINK_TIME")
DEFAULT_EXPIRY_LINK_TIME = config_data.get("DEFAULT_EXPIRY_LINK_TIME")
MAX_UPLOAD_SIZE = config_data.get("MAX_UPLOAD_SIZE")
tiers_config = config_data.get("DEFAULT_TIERS_CONFIG", {})
