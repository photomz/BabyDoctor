python ~/myllm/LLaVA/scripts/merge_lora_weights.py \
	--model-path ~/roco-llava-finetuned/ \
	--model-base kaelee/llava-llama-2-7b-chat-finetuning \
	--save-model-path llava-roco-8bit