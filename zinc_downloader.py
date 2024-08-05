import requests
from colorama import Fore, Style
from tqdm import tqdm
import os

def download_zinc_data(zinc_id, file_format, zinc_version):
    base_url = f"https://zinc{zinc_version}.docking.org/substances/{zinc_id}.{file_format}"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def main():
    zinc_version = input("Choose between 15 & 20 (15 for zinc15.docking.org, 20 for zinc20.docking.org): ")
    file_format = input("Choose file format (SDF, SMI, CSV, XML, JSON): ").lower()
    list_file = input("Enter your Zinc ID list file (default is list.txt): ") or 'list.txt'
    merge_files = input("Do you want to merge all downloaded molecules to a final_dataset file at the end? (yes/no): ").lower()

    if not os.path.exists(list_file):
        print(Fore.RED + f"File {list_file} does not exist." + Style.RESET_ALL)
        return

    with open(list_file, 'r') as f:
        zinc_ids = f.read().splitlines()

    os.makedirs('dataset', exist_ok=True)
    dataset_folder = 'dataset'
    merged_content = []

    for zinc_id in tqdm(zinc_ids, desc="Downloading datasets"):
        content = download_zinc_data(zinc_id, file_format, zinc_version)
        if content:
            file_path = os.path.join(dataset_folder, f"{zinc_id}.{file_format}")
            with open(file_path, 'wb') as f:
                f.write(content)
            if merge_files == 'yes':
                merged_content.append(content.decode('utf-8'))

    if merge_files == 'yes':
        merged_folder = 'merged_dataset'
        os.makedirs(merged_folder, exist_ok=True)
        merged_file_path = os.path.join(merged_folder, f"final_dataset.{file_format}")
        with open(merged_file_path, 'w') as f:
            f.write('\n'.join(merged_content))
        print(Fore.GREEN + f"Merged dataset saved to {merged_file_path}" + Style.RESET_ALL)

    print(Fore.GREEN + "Download completed." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
