import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.scripts.model import Model
from sklearn.linear_model import LogisticRegression

#load dataset with either path or name
try:
    dataset_path
    model = Model(dataset_path = dataset_path)
except:
    try:
        dataset_name
    except:
        dataset_name = "give_me_credit"
        model = Model(dataset_name = dataset_name)

# Set the model
clf = LogisticRegression(random_state=0, penalty="none")
model.train(clf)
# Plot the performance
model.plot_clf()

logger.info("=================Training complete=================")




