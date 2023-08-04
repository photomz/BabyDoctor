from llava.model.builder import load_pretrained_model

tokenizer, model, image_processor, context_len = \
				load_pretrained_model('kaelee/llava-llama-2-7b-chat-finetuning', None, \
				'llava-llama-2-7b-chat-finetuning', load_8bit=True)

model.push_to_hub("llava-llama-2-7b-chat-8bit")