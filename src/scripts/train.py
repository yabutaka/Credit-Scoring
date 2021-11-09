from model import Model
from sklearn.linear_model import LogisticRegression

# Set the dataset name
name = "give_me_credit"

model = Model(name)
# Set the model
clf = LogisticRegression(random_state=0, penalty="none")
model.train(clf)
# Plot the performance
model.plot_clf()