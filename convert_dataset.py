from datasets import load_dataset, Dataset, DatasetDict
from sklearn.model_selection import train_test_split


data = load_dataset("json", data_files="alpaca_data.json")


train_dataset, test_dataset = train_test_split(data['train'], test_size=0.2, random_state=42)

print(train_dataset['instruction'][0])
print(type(train_dataset))

dataset = DatasetDict({
    'train': Dataset.from_dict(
        train_dataset
    ),
    'validation': Dataset.from_dict(
        test_dataset
    ),
})

dataset.save_to_disk('alpaca_data.hf')