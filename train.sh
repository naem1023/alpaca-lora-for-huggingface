python train.py \
    --model_name_or_path decapoda-research/llama-7b-hf \
    --dataset_name alpaca_data.hf \
    --is_dataset_from_disk True \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --do_train \
    --do_eval \
    --output_dir test-clm