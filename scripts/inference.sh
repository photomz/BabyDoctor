python -m llava.eval.run_llava \
	--model-path photonmz/llava-roco-8bit \
	--image-file ~/roco-dataset/data/train/radiology/images/ROCO_00002.jpg \
	--query 'The following image is a radiology scan. Deeply analyze and diagnose this image.'