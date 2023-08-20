import json

def txt_to_json(input_file_path, output_file_path):
    with open(input_file_path, 'r') as f:
        content = f.read()

    data = {
        "text_content": content
    }

    with open(output_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    input_file_path = "Rule1.txt"  # Replace with the path to your input text file
    output_file_path = "Rule1.json"  # Replace with the desired output JSON file path
    txt_to_json(input_file_path, output_file_path)