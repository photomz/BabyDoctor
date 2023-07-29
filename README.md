# BabyDoctor

This repository contains an implementation of BabyDoctor.

## Reproduce the result

0. Get a system with at least 16 vCPUs, 32GB RAM, and a NVIDIA GPU of >12GB VRAM.
1. Install CUDA.
    * For Ubuntu, that amounts to following [the official NVIDIA setup instructions](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu).
2. Install Conda.
3. Run `mkdir -p ~/git; cd ~/git`.
4. Clone this repository into `~/git/LLaVA`.
5. Run `conda env create -f LLaVA/llmenv.yaml`. This will take a while.
6. Run `conda activate llmforbio`. From this step onward, execute all commands under this environment.
7. Run `MAX_JOBS=8 python3 -m pip install flash-attn`.
8. Download the dataset: `git clone https://github.com/razorx89/roco-dataset; cd roco-dataset; python3 scripts/fetch.py; popd`.
9. Get usable training data: `python3 LLaVA/scripts/markus/massage_data.py`.
10. Do the actual finetuning: `mv LLaVA/finetune.sh .; bash finetune.sh`. This took 8 hours on the A10.
