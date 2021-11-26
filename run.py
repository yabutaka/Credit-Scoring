test_dataset_path = "src/data/screening/screening_data.csv"

exec(open("src/scripts/train.py").read(),
    {'dataset_path': test_dataset_path})
