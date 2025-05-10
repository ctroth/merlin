import os
import json

def write_to_check_results(data, filename ="check_results.json"):
    
    script_directory = os.path.dirname(__file__)
    merlin_root_directory = os.path.dirname(script_directory)

    full_path = os.path.join(merlin_root_directory, "check_results.json")

    # check if the file exists
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding = 'utf-8') as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)

    with open(full_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=2)

def main():
    write_to_check_results()

if __name__ == "__main__":
    main()