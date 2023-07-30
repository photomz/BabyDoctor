import os
import shutil

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, BitsAndBytesConfig
import torch
from llava.model import *
from llava.constants import DEFAULT_IMAGE_PATCH_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from peft import PeftModel

def load_pretrained_model(model_path, model_base, model_name, load_8bit=False, load_4bit=False, device_map="auto"):
		kwargs = {"device_map": device_map}

		if load_8bit:
				kwargs['load_in_8bit'] = True
		elif load_4bit:
				kwargs['load_in_4bit'] = True
		else:
				kwargs['torch_dtype'] = torch.float16

		print("\n\nLOAD ME DADDY\n\n\n")

		lora_cfg_pretrained = AutoConfig.from_pretrained(model_base or model_path)
		tokenizer = AutoTokenizer.from_pretrained(model_base, use_fast=False)
		print('Loading LLaVA from base model...')
		model = LlavaLlamaForCausalLM.from_pretrained(model_base, low_cpu_mem_usage=True, config=lora_cfg_pretrained, **kwargs)
		token_num, tokem_dim = model.lm_head.out_features, model.lm_head.in_features
		if model.lm_head.weight.shape[0] != token_num:
				model.lm_head.weight = torch.nn.Parameter(torch.empty(token_num, tokem_dim, device=model.device, dtype=model.dtype))
				model.model.embed_tokens.weight = torch.nn.Parameter(torch.empty(token_num, tokem_dim, device=model.device, dtype=model.dtype))

		print('Loading additional LLaVA weights...')
		
		print('Loading LoRA weights...')
		model = PeftModel.from_pretrained(model, model_path)
		print('Merging LoRA weights...')
		model = model.merge_and_unload()
		print('Model is loaded...')

		image_processor = None

		mm_use_im_start_end = getattr(model.config, "mm_use_im_start_end", False)
		mm_use_im_patch_token = getattr(model.config, "mm_use_im_patch_token", True)
		if mm_use_im_patch_token:
				tokenizer.add_tokens([DEFAULT_IMAGE_PATCH_TOKEN], special_tokens=True)
		if mm_use_im_start_end:
				tokenizer.add_tokens([DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN], special_tokens=True)
		model.resize_token_embeddings(len(tokenizer))

		vision_tower = model.get_vision_tower()
		if not vision_tower.is_loaded:
				vision_tower.load_model()
		vision_tower.to(device='cuda', dtype=torch.float16)
		image_processor = vision_tower.image_processor

		if hasattr(model.config, "max_sequence_length"):
				context_len = model.config.max_sequence_length
		else:
				context_len = 2048

		return tokenizer, model, image_processor, context_len
