import os
import subprocess
import sys
import json

def get_llamacpp_path():
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings.get('llamacpp_path')

def menu_selection():
    menu_options = ["Q2_K", "Q3_K_M", "Q4_K_M", "Q5_K_M", "Q6_K"]
    for i, option in enumerate(menu_options):
        print(f"{i + 1}. {option}")
    choice = int(input("Select an option (1-5): "))
    return menu_options[choice - 1]

def main(folder_path):
    llamacpp_path = get_llamacpp_path()
    model_name = os.path.basename(folder_path)
    gguf_file_path = os.path.join(folder_path, f"{model_name}.GGUF")
    quantization_option = menu_selection()

    if not os.path.exists(gguf_file_path):
        convert_command = f"python {llamacpp_path}/convert.py \"{folder_path}\" --outfile \"{gguf_file_path}\" --outtype f16"
        print("Running convert command:", convert_command)
        subprocess.run(convert_command, shell=True)
    else:
        print(f"The .GGUF file for {model_name} already exists. Skipping conversion.")

    if os.path.exists(gguf_file_path):
        quantize_command = [os.path.join(llamacpp_path, "quantize"), gguf_file_path, f"{folder_path}/{model_name}-{quantization_option}.gguf", quantization_option]
        print("Running quantize command...")
        subprocess.run(quantize_command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_folder>")
    else:
        main(sys.argv[1])
