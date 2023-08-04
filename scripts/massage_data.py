import json
from pathlib import Path
from tqdm import tqdm

split = 'test'
version = 1

# Define the input and output file paths
base_dir = Path('git')
image_dir = base_dir / 'roco-dataset/data' / split / 'radiology/images'
input_path = base_dir / 'roco-dataset/data' / split / 'radiology/captions.txt'
output_path = base_dir / 'roco'/ f'roco-{split}-{version}.json'

# Process each line in the input file
with input_path.open('r') as input_file, output_path.open('w') as output_file:
		flag = False
		json_array = []
		for line in tqdm(input_file):
				words = line.split()

				# Reconstruct the line after processing
				id_word = words[0][5:] # Skip the first 5 characters
				image_word = words[0] + '.jpg' # Append .jpg

				output_word = line[len(words[0])+2:] # Skip the first word and the following 2 characters

				conversations = [
					{
						'from': 'human',
						'value': 'The following image is a radiology scan. Deeply analyze and diagnose this image.\n<image>'
					},
					{
						'from': 'gpt',
						'value': output_word.strip()
					}
				]

				# Create a JSON object and write it to the output file
				datapoint = {
						'id': id_word,
						'image': image_word,
						'conversations': conversations
				}
				if not flag:
					print(datapoint)
					flag = True

				if is_valid_image := (image_dir / image_word).exists():
						json_array.append(datapoint)
						
		json.dump(json_array, output_file, ensure_ascii=False, indent=2)

# original_output_path =  base_dir / 'roco-finetuning-2.json'

# from deepdiff import DeepDiff

# with output_path.open() as A_file,  original_output_path.open() as B_file:
# 	A = json.load(A_file)
# 	B = json.load(B_file)
# 	i=0
# 	for a,b in zip(A,B):
# 			if a != b:
# 				print(DeepDiff(a, b, ignore_order=True))
# 				i+=1
# 			if i > 10: pass