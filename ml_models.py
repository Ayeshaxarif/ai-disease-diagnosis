import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

data = {
    "fever": [1,1,1,0,1,0,0,1,1,0,1,1,0,0,1],
    "cough": [1,1,0,0,1,0,0,0,1,0,1,0,1,0,0],
    "fatigue": [1,0,1,0,0,1,0,1,0,1,0,1,0,1,1],
    "thirst": [0,0,0,1,0,1,0,0,0,0,0,0,0,0,0],
    "chills": [0,1,0,0,0,0,1,1,0,0,1,0,0,0,0],
    "stomach_pain": [0,0,1,0,0,0,0,0,0,1,0,0,1,0,0],
    "shortness_of_breath": [0,0,0,0,1,0,0,0,1,0,0,0,0,1,0],
    "headache": [0,1,1,0,0,0,0,1,0,0,1,0,0,1,0],
    "disease": ["flu","malaria","typhoid","diabetes","covid",
                "diabetes","malaria","flu","covid","typhoid",
                "dengue","anemia","gastroenteritis","migraine","tuberculosis"]
}

df = pd.DataFrame(data)
X = df.drop("disease", axis=1)
y = df["disease"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
knn_acc = accuracy_score(y_test, knn.predict(X_test))

svm = SVC(kernel="rbf", probability=True)
svm.fit(X_train, y_train)
svm_acc = accuracy_score(y_test, svm.predict(X_test))

nn = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=1000, random_state=42)
nn.fit(X_train, y_train)
nn_acc = accuracy_score(y_test, nn.predict(X_test))

def predict_all(symptoms_dict):
    vals = [list(symptoms_dict.values())]
    return {
        "KNN": knn.predict(vals)[0],
        "SVM": svm.predict(vals)[0],
        "Neural Network": nn.predict(vals)[0],
    }

def get_confusion_matrix(model="knn"):
    m = {"knn": knn, "svm": svm, "nn": nn}[model]
    y_pred = m.predict(X_test)
    cm = confusion_matrix(y_test, y_pred, labels=m.classes_)
    return pd.DataFrame(cm, index=m.classes_, columns=m.classes_)

def get_model_accuracy():
    return {
        "KNN": round(knn_acc * 100, 1),
        "SVM": round(svm_acc * 100, 1),
        "Neural Network": round(nn_acc * 100, 1)
    }

print(f"KNN Accuracy: {knn_acc:.0%}")
print(f"SVM Accuracy: {svm_acc:.0%}")
print(f"Neural Network Accuracy: {nn_acc:.0%}")
print("All ML Models Ready!")
