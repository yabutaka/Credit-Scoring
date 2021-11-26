dataset_name = "give_me_credit"

exec(open("src/scripts/train.py").read(),
    {'name': dataset_name})