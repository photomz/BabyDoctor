from datasets import load_dataset
from pathlib import Path
import json

version = 1

def download_splits_as_json(dataset_name, output_folder):
    # Load the dataset
    dataset = load_dataset(dataset_name)

    # Create the output folder if it doesn't exist
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through each split and export as JSON
    for split_name in dataset.keys():
        split_path = output_path / f"roco-{split_name}-{version}.json"
        data = dataset[split_name].to_dict()

        # Extract the required columns and create an array of dictionaries
        examples = []
        for idx in range(len(data['conversations'])):
            example = {
                'conversations': data['conversations'][idx],
                'image': data['image'][idx],
                'id': data['id'][idx]
                # Add more columns here if needed
            }
            examples.append(example)

        # Convert data to JSON format and save to the output file
        with split_path.open('w', encoding='utf-8') as f:
            json.dump(examples, f, ensure_ascii=False)

        print(f"Exported {split_name} split to {split_path}")

if __name__ == "__main__":
    dataset_name = "photonmz/roco-instruct-65k"  # Replace with the name of the dataset from Hugging Face
    output_folder = "roco"  # Replace with the desired folder name to store the JSON files

    download_splits_as_json(dataset_name, output_folder)
