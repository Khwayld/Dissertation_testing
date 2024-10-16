from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.datasets import make_blobs
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score
import numpy as np

@api_view(['GET'])
def test_view(request):
    return Response({"message": "Django & React Integration Test"})



@api_view(['GET'])
def kale_example_view(request):
    np.random.seed(42)
    # Generate toy data
    X, y = make_blobs(n_samples=200, centers=[[0, 0], [2, 2]], cluster_std=0.5)
    clf = RidgeClassifier()
    clf.fit(X, y)
    accuracy = accuracy_score(y, clf.predict(X))
    return Response({"accuracy": accuracy})
