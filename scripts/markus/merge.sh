cd ~/LLaVA/scripts
python merge_lora_weights.py --model-path ~/git/lora-roco-llava/checkpoint-2300/ --model-base ~/git/LLaVA/checkpoints/llava-7b-pretrain/ --save-model-path ~/merged-llava