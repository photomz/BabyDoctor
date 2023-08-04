import json, datasets
from pathlib import Path

base_dir = Path('git/roco')

splits = [
    {'name': 'train', 'stem': 'roco-train-1.json'},
    {'name': 'validation', 'stem': 'roco-validation-1.json'},
    {'name': 'test', 'stem': 'roco-test-1.json'}
]

for s in splits:
    dataset = datasets.load_dataset('json', data_files=str(base_dir / s['stem']))['train']
    dataset.push_to_hub('roco-instruct-65k', split=s['name'])