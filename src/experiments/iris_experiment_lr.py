
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from mlflow import log_metric, log_param
from mlflow.sklearn import log_model
import mlflow

url= "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/639388c2cbc2120a14dcf466e85730eb8be498bb/iris.csv"
df = pd.read_csv(url)
df.sample(2)

le = preprocessing.LabelEncoder()
df['species'] = le.fit_transform(df['species'])


y = df['species']
x = df[['sepal_length']]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=2)


MAX_ITER = 2

mlflow.set_tracking_uri("http://52.56.126.161:5000/")

try:
    mlflow.create_experiment("iris_lr")
except:
    print('The experiment may already exist.')

mlflow.set_experiment("iris_lr")

with mlflow.start_run(nested=True):

    log_param("MAX_ITER", MAX_ITER)
    
    clf = LogisticRegression(max_iter=MAX_ITER)
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    acc = accuracy_score(y_test, y_pred)

    log_metric("Accuracy", acc)
    log_model(clf, "Model")

print(classification_report(y_test, y_pred, target_names=le.classes_))
