test_dataset_path = ...

exec(open("src/scripts/train.py").read(),
    {'dataset_path': test_dataset_path})
