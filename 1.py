import os
MODEL_PATH = "models"
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)
# Save model
pickle.dump(text_clf, open(os.path.join(MODEL_PATH, "svm_model.pkl"), 'wb'))

# SVM Accuracy
model = pickle.load(open(os.path.join(MODEL_PATH,"svm.pkl"), 'rb'))
y_pred = model.predict(X_test)
print('SVM, Accuracy =', np.mean(y_pred == y_test))