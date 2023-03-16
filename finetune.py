import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import torch
import torch.nn as nn
from datasets import load_dataset
import transformers
from transformers import AutoTokenizer, AutoConfig, LLaMAForCausalLM, LLaMATokenizer
from peft import prepare_model_for_int8_training, LoraConfig, get_peft_model


# optimized for RTX 4090. for larger GPUs, increase some of these?
MICRO_BATCH_SIZE = 6  # this could actually be 5 but i like powers of 2
BATCH_SIZE = 128
GRADIENT_ACCUMULATION_STEPS = BATCH_SIZE // MICRO_BATCH_SIZE
EPOCHS = 3  # we don't need 3 tbh
LEARNING_RATE = 2e-5  # from the original paper
CUTOFF_LEN = 256  # 256 accounts for about 96% of the data
LORA_R = 4
LORA_ALPHA = 16
LORA_DROPOUT = 0.05

model_path = os.environ["model_path"]
output_dir = os.environ["output_dir"]
model = LLaMAForCausalLM.from_pretrained(
    model_path,
)
tokenizer = LLaMATokenizer.from_pretrained(
    model_path, add_eos_token=True
)

# model = prepare_model_for_int8_training(model)

config = LoraConfig(
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=LORA_DROPOUT,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, config)
tokenizer.pad_token_id = 0  # unk. we want this to be different from the eos token
data = load_dataset("json", data_files="alpaca_data.json")


def generate_prompt(data_point):
    # sorry about the formatting disaster gotta move fast
    if data_point["input"]:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{data_point["instruction"]}

### Input:
{data_point["input"]}

### Response:
{data_point["output"]}"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{data_point["instruction"]}

### Response:
{data_point["output"]}"""


data = data.shuffle().map(
    lambda data_point: tokenizer(
        generate_prompt(data_point),
        truncation=True,
        max_length=CUTOFF_LEN,
        padding="max_length",
    )
)

trainer = transformers.Trainer(
    model=model,
    train_dataset=data["train"],
    args=transformers.TrainingArguments(
        per_device_train_batch_size=MICRO_BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        warmup_steps=100,
        num_train_epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        bf16=True,
        logging_steps=1,
        output_dir=output_dir,
        save_total_limit=4,
    ),
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False),
)
model.config.use_cache = False
trainer.train(resume_from_checkpoint=False)

model.save_pretrained(output_dir)
model.save_model()
