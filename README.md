#  😊 Alpaca-lora for huggingface implementation using Deepspeed and FullyShardedDataParallel 😊

## Features
- Multi-GPU training using DeepSpeed and Fully sharded Data Parallel with Accelerate
- Training LLaMA using huggingface, lora, peft
- Using clm training examples from huggingface example
    - https://github.com/huggingface/transformers/tree/main/examples/pytorch/language-modeling
- You can use alpaca_data.hf which is converted for using Huggingface Datasets
    - Split train and validation for clm training

The codes are still updated, so maybe there're can be some unexpected error.
I used base code from https://github.com/tloen/alpaca-lora. Thanks a lot!!