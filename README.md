#  😊 Alpaca-lora for huggingface implementation using Deepspeed and FullyShardedDataParallel 😊

## Features
- Multi-GPU training using DeepSpeed and Fully sharded Data Parallel with Accelerate
- Training LLaMA using huggingface, lora, peft
- Using clm training examples from huggingface example
    - https://github.com/huggingface/transformers/tree/main/examples/pytorch/language-modeling
- You can use alpaca_data.hf which is converted for using Huggingface Datasets
    - Split train and validation for clm training

## Dependency
```sh
pip install -r requirements.txt
```

## Train
```sh
# Use PEFT, LORA
accelerate launch --config_file peft_config.yaml finetune.py

# Use Huggingface Arguments for controll all situations during training.
# You can use train.sh.
# Stil updating...
python train.py \
    --model_name_or_path decapoda-research/llama-7b-hf \
    --dataset_name alpaca_data.hf \
    --is_dataset_from_disk True \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --do_train \
    --do_eval \
    --output_dir test-clm
```
The codes are still updated, so maybe there're can be some unexpected error.
I used base code from https://github.com/tloen/alpaca-lora. Thanks a lot!!