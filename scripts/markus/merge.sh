cd ~
python LLaVA/scripts/merge_lora_weights.py --model-path ~/git/lora-roco-llava/checkpoint-2600/ --model-base ~/git/LLaVA/checkpoints/llava-7b-pretrain/ --save-model-path llava-roco-8bit