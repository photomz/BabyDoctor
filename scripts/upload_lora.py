"""
python ~/myllm/LLaVA/scripts/upload_lora.py \
--path llava-roco-8bit
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1].resolve()))


from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path


def merge_lora(args):
		tokenizer, model, image_processor, context_len = \
					load_pretrained_model(args.path, None, args.path, device_map='cpu')

		model.push_to_hub(args.path)
		tokenizer.push_to_hub(args.path)


if __name__ == "__main__":
		parser = argparse.ArgumentParser()
		parser.add_argument("--path", type=str, required=True)

		args = parser.parse_args()

		merge_lora(args)