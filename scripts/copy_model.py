from pathlib import Path
import shutil

def copy_files(source_dir, destination_dir):
		source_path = Path(source_dir)
		destination_path = Path(destination_dir)

		# Create the destination directory if it doesn't exist
		destination_path.mkdir(parents=True, exist_ok=True)

		# Iterate over the files in the source directory
		for file_path in source_path.iterdir():
				destination_file = destination_path / file_path.name

				# Check if the destination file already exists
				if not destination_file.exists():
						# Copy the file from the source directory to the destination directory
						shutil.copy2(file_path, destination_file)
						print(f"Copied '{file_path.name}' to '{destination_file}'.")
				else:
						print(f"Skipped '{file_path.name}' as it already exists in '{destination_file.parent}'.")
				#break

# Replace the paths with your desired source and destination directories
source_directory = "git/LLaVA/checkpoints/llava-7b-pretrain/"
destination_directory = "git/roco-finetuned-llava/"

copy_files(source_directory, destination_directory)
