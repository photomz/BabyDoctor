import json
from typing import List, Dict
from pathlib import Path

def load_data_from_json(file_path: Path) -> List[Dict]:
    """Load data from a JSON file.
    
    Args:
        file_path (Path): The path to the JSON file.

    Returns:
        List[Dict]: The data loaded from the JSON file.
    """
    with file_path.open() as f:
        data = json.load(f)
    return data

def save_data_to_json(data: List[Dict], file_path: Path) -> None:
    """Save data to a JSON file.

    Args:
        data (List[Dict]): The data to be saved.
        file_path (Path): The path to the JSON file.
    """
    with file_path.open("w") as f:
        json.dump(data, f, indent=4)

def filter_missing_images(data: List[Dict], missing_images: List[str]) -> List[Dict]:
    """Filter out JSON objects that contain missing images.
    
    Args:
        data (List[Dict]): The list of JSON objects.
        missing_images (List[str]): The list of missing images.

    Returns:
        List[Dict]: The filtered list of JSON objects.
    """
    return [item for item in data if item["image"] not in missing_images]

def main():
    """The main function to load, filter, and save data."""
    # Define the file paths.
    input_file_path = Path("../git/roco-finetuning.json")
    output_file_path = Path("../git/roco-finetuning-2.json")

    # Load the data from the JSON file.
    data = load_data_from_json(input_file_path)

    # Assume the list of missing images already exists.
    missing_images = ["ROCO_07233.jpg",
										"ROCO_07738.jpg",
										"ROCO_07927.jpg",
										"ROCO_22299.jpg",
										"ROCO_24535.jpg",
										"ROCO_24849.jpg",
										"ROCO_25337.jpg",
										"ROCO_26232.jpg",
										"ROCO_26439.jpg",
										"ROCO_29364.jpg",
										"ROCO_35395.jpg",
										"ROCO_36338.jpg",
										"ROCO_37937.jpg",
										"ROCO_40763.jpg",
										"ROCO_47259.jpg",
										"ROCO_50469.jpg",
										"ROCO_50644.jpg",
										"ROCO_53013.jpg",
										"ROCO_57545.jpg",
										"ROCO_60391.jpg",
										"ROCO_61045.jpg",
										"ROCO_63050.jpg",
										"ROCO_63365.jpg",
										"ROCO_64107.jpg",
										"ROCO_67140.jpg",
										"ROCO_70505.jpg",
										"ROCO_77673.jpg",
										"ROCO_78946.jpg"]


    # Filter out JSON objects that contain missing images.
    filtered_data = filter_missing_images(data, missing_images)

    # Save the filtered data to a new JSON file.
    save_data_to_json(filtered_data, output_file_path)

if __name__ == "__main__":
    main()
