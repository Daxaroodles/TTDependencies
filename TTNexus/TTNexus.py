import argparse
import os
import yaml
import json
import datetime

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def delete_file(file_path):
    """Deletes a file and provides feedback."""
    
    try:
        os.remove(file_path)
        print(f"{GREEN}[Success]{RESET} File '{file_path}' has been deleted.")
    except FileNotFoundError:
        print(f"{RED}[NexusFatality]{RESET} File '{file_path}' not found.")
    except PermissionError:
        print(f"{RED}[NexusFatality]{RESET} Permission denied to delete '{file_path}'.")
    except Exception as e:
        print(f"{RED}[NexusFatality]{RESET} Error: {e}")

def fetch_everestyaml(celeste_path, modname):
    """Fetches the everest.yaml inside your mod, translates it to JSON, and saves it."""
    
    if not os.path.exists(celeste_path):
        print(f"{RED}[NexusFatality]{RESET} invalidModException: Celeste directory does not exist.")
        log("NexusFatality: Celeste directory does not exist.")
        return

    mods_path = os.path.join(celeste_path, "Mods")
    if not os.path.isdir(mods_path):
        print(f"{RED}[NexusFatality]{RESET} invalidModException: Mods directory does not exist.")
        log("NexusFatality: Mods directory does not exist.")
        return

    mod_path = os.path.join(mods_path, modname)
    if not os.path.isdir(mod_path):
        print(f"{RED}[NexusFatality]{RESET} invalidModException: Mod folder '{modname}' does not exist.")
        log("NexusFatality: Mod folder '{modname}' does not exist.")
        return

    yaml_path = os.path.join(mod_path, "everest.yaml")

    if not os.path.isfile(yaml_path):
        print(f"{RED}[NexusFatality]{RESET} invalidYamlException: everest.yaml does not exist.")
        log("NexusFatality: everest.yaml does not exist.")
        return

    print(f"{GREEN}[Success]{RESET} Yaml found for mod '{modname}':")
    print(f"- {yaml_path}")

    json_path = os.path.join(mod_path, "everest.TTNexus.temp")
    delete_file(json_path)  

    try:
        with open(yaml_path, "r") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
    except Exception as e:
        print(f"{RED}[NexusFatality]{RESET} Error reading YAML file: {e}")
        log("NexusFatality: Error reading YAML file.")
        return

    try:
        with open(json_path, "w") as json_file:
            json.dump(yaml_data, json_file, indent=4)
        print(f"{GREEN}[Success]{RESET} everest.TTNexus.temp saved to '{json_path}'")
    except Exception as e:
        print(f"{RED}[NexusFatality]{RESET} Error saving everest.TTNexus.temp: {e}")
        log("NexusFatality: Error saving everest.TTNexus.temp.")

def merge_everestjson(celeste_path, modname):
    """Converts the everest.TTNexus.temp JSON file back into YAML."""
    
    mods_path = os.path.join(celeste_path, "Mods")
    if not os.path.isdir(mods_path):
        print(f"{RED}[NexusFatality]{RESET} invalidModException: Mods directory does not exist.")
        log("NexusFatality: Mods directory does not exist.")
        return

    mod_path = os.path.join(mods_path, modname)
    if not os.path.isdir(mod_path):
        print(f"{RED}[NexusFatality]{RESET} invalidModException: Mod folder '{modname}' does not exist.")
        log("NexusFatality: Mod folder '{modname}' does not exist.")
        return

    json_path = os.path.join(mod_path, "everest.TTNexus.temp")

    if not os.path.isfile(json_path):
        print(f"{RED}[NexusFatality]{RESET} invalidJsonException: everest.TTNexus.temp does not exist.")
        log("NexusFatality: everest.TTNexus.temp does not exist.")
        return

    print(f"{GREEN}[Success]{RESET} JSON found for mod '{modname}':")
    print(f"- {json_path}")

    try:
        with open(json_path, "r") as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        print(f"{RED}[NexusFatality]{RESET} Error reading JSON file: {e}")
        log("NexusFatality: Error reading JSON file.")
        return

    yaml_path = os.path.join(mod_path, "everest.yaml")
    try:
        with open(yaml_path, "w") as yaml_file:
            yaml.safe_dump(json_data, yaml_file, default_flow_style=False)
        print(f"{GREEN}[Success]{RESET} everest.yaml saved to '{yaml_path}'")
    except Exception as e:
        print(f"{RED}[NexusFatality]{RESET} Error saving YAML: {e}")
        log("NexusFatality: Error saving YAML.")

    if os.path.exists(json_path):
        os.remove(json_path)
        print(f"{GREEN}[Success]{RESET} {json_path} has been deleted successfully.")
    else:
        print(f"{RED}[NexusFatality]{RESET} The file {json_path} does not exist.")
        log("NexusFatality: The file {json_path} does not exist.")

def main():
    parser = argparse.ArgumentParser(description="Allows for communication between the Tea Tree editor/GameMaker and Celeste/Everest resources. For technical support, please contact me on Discord (@daxaroodles). Alternatively, you can join my Discord Server and ping me in the TTNexus channel. https://discord.gg/6vbhdzmGq7")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    
    parser_fetch_everestyaml = subparsers.add_parser("fetch_everestyaml", help="Fetches the everest.yaml inside your mod and translates it to JSON so GameMaker can read it.")
    parser_fetch_everestyaml.add_argument("celeste_path", type=str, help="Path to your Celeste directory.")
    parser_fetch_everestyaml.add_argument("modname", type=str, help="Name of the mod.")
    parser_fetch_everestyaml.set_defaults(func=lambda args: fetch_everestyaml(args.celeste_path, args.modname))

    parser_merge_everestjson = subparsers.add_parser("merge_everestjson", help="Converts the everest.TTNexus.temp JSON file back into YAML.")
    parser_merge_everestjson.add_argument("celeste_path", type=str, help="Path to your Celeste directory.")
    parser_merge_everestjson.add_argument("modname", type=str, help="Name of the mod.")
    parser_merge_everestjson.set_defaults(func=lambda args: merge_everestjson(args.celeste_path, args.modname))

    args = parser.parse_args()
    args.func(args)

def log(message):
    log_dir = os.path.join(os.path.expanduser("~"), "ttnexuslogs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file_path = os.path.join(log_dir, "error_log.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    print(f"[Error Log] Message logged to {log_file_path}")
    

parent_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(parent_dir, 'ttnexus_config.json')

data = {
    "version": "0.0.1",
    "branch": "main",
}
with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"{YELLOW}[CONFIG]{RESET} TTNexus version written to {json_file_path}")

if __name__ == "__main__":
    main()
