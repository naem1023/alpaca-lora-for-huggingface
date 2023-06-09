accelerate launch --config_file peft_config.yaml train.py \
    --model_name_or_path $model_path \
    --dataset_name alpaca_data.hf \
    --is_dataset_from_disk True \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --lora_r 4 \
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --bf16 True \
    --bf16_full_eval True \
    --do_train \
    --do_eval \
    --output_dir $output_dir \
    --overwrite_output_dir