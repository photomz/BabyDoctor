import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1].resolve()))


from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path


def merge_lora(args):
    model_name = args.model_path # get_model_name_from_path(args.model_path)
    print(model_name)
    tokenizer, model, image_processor, context_len = load_pretrained_model(args.model_path, args.model_base, model_name, device_map='cpu')

    model.save_pretrained(args.save_model_path)
    tokenizer.save_pretrained(args.save_model_path)

    if args.push_to_hub:
        model.push_to_hub(args.save_model_path)
        tokenizer.push_to_hub(args.save_model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--model-base", type=str, required=True)
    parser.add_argument("--save-model-path", type=str, required=True)
    parser.add_argument("--push-to-hub", type=bool, required=False, default=True)

    args = parser.parse_args()

    merge_lora(args)
