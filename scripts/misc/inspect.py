base = 'roco-dataset/data/test/radiology/'

captions = {}

with open(base + '/captions.txt', 'r') as f:
    for line in f:
        x, y = line.split('\t')
        y = y.strip()
        captions[x + '.jpg'] = y

import argparse
import torch
import os, json, gzip

from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.conversation import conv_templates, SeparatorStyle
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria

from PIL import Image

import requests
from PIL import Image
from io import BytesIO

disable_torch_init()

def load_image(image_file):
    if image_file.startswith('http') or image_file.startswith('https'):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_file).convert('RGB')
    return image

model_path = 'photonmz/llava-roco-8bit'
model_name = get_model_name_from_path(model_path)
tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, None, model_name)
if "v1" in model_name.lower():
    conv_mode = "llava_v1"
elif "mpt" in model_name.lower():
    conv_mode = "mpt"
else:
    conv_mode = "llava_v0"

def run_model(pic):
    qs = 'The following image is a radiology scan. Deeply analyze and diagnose this image.'
    if model.config.mm_use_im_start_end:
        qs = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + qs
    else:
        qs = DEFAULT_IMAGE_TOKEN + '\n' + qs

    conv = conv_templates[conv_mode].copy()
    conv.append_message(conv.roles[0], qs)
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()

    image = load_image(base + f'/images/{pic}')
    image_tensor = image_processor.preprocess(image, return_tensors='pt')['pixel_values'].half().cuda()

    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()

    stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
    keywords = [stop_str]
    stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            do_sample=False, # i.e. temp=0
            temperature=0,
            max_new_tokens=1024,
            use_cache=True,
            stopping_criteria=[stopping_criteria])

    input_token_len = input_ids.shape[1]
    n_diff_input_output = (input_ids != output_ids[:, :input_token_len]).sum().item()
    if n_diff_input_output > 0:
        print(f'[Warning] {n_diff_input_output} output_ids are not the same as the input_ids')
    outputs = tokenizer.batch_decode(output_ids[:, input_token_len:], skip_special_tokens=True)[0]
    outputs = outputs.strip()
    if outputs.endswith(stop_str):
        outputs = outputs[:-len(stop_str)]
    outputs = outputs.strip()
    return outputs


def distance(outputted, real):
    c1 = len(gzip.compress(outputted.encode()))
    c2 = len(gzip.compress(real.encode()))
    c12 = len(gzip.compress((outputted + '\n' + real).encode()))
    ncd = (c12 - min(c1, c2))/ max(c1, c2)
    return ncd

outfile = open('inspected.json', 'w')
outfile.write('[')

arr = []
marr = None
i = 0
imgs = sorted(os.listdir('roco-dataset/data/test/radiology/images'))
for pic in imgs[:500]:
    i += 1
    if i % 10 == 0:
        print('i = ', i)
    out = run_model(pic)
    dist = distance(out, captions[pic])
    tup = (dist, pic, out)
    outfile.write(f'{tup},')
    arr.append(tup) 
    if marr is None or marr[0] >= dist:
        marr = tup
        print('marr updated to', marr)
        print(f'(real was "{captions[pic]}")')

arr.sort(key=lambda k: k[0])

print('final writtern to inspected.json')
