import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from sklearn.datasets import make_blobs
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from kale.pipeline.multi_domain_adapter import CoIRLS


@api_view(['GET'])
def test_view(request):
    return Response({"message": "Django & React Integration Test"})


@api_view(['POST'])
def run_example(request):
    # Set the seed for reproducibility
    np.random.seed(29118)

    # Get parameters from frontend
    lambda_value = float(request.data.get('lambda_value', 1.0))
    alpha_value = float(request.data.get('alpha_value', 1.0))  # Define alpha_value

    
    # Get the uploaded files
    source_file = request.FILES.get('source_data')
    target_file = request.FILES.get('target_data')


    if not source_file or not target_file:
        return Response({"error": "Source and target data files are required"}, status=400)

    # Read the CSV files into pandas dataframes
    source_data = pd.read_csv(source_file)
    target_data = pd.read_csv(target_file)
    n_samples = len(source_data)


    # Split the data into features (all columns except 'label') and labels (the 'label' column)
    xs = source_data.drop(columns=["label"]).values
    ys = source_data["label"].values

    xt = target_data.drop(columns=["label"]).values
    yt = target_data["label"].values


    # Train Ridge Classifier
    clf = RidgeClassifier(alpha=alpha_value)
    clf.fit(xs, ys)
    yt_pred = clf.predict(xt)
    accuracy_before = accuracy_score(yt, yt_pred)

    # Domain adaptation with CoIRLS
    clf_ = CoIRLS(lambda_=lambda_value)
    covariates = np.zeros(n_samples * 2)
    covariates[:n_samples] = 1
    enc = OneHotEncoder(handle_unknown="ignore")
    covariates_mat = enc.fit_transform(covariates.reshape(-1, 1)).toarray()

    x = np.concatenate((xs, xt))
    clf_.fit(x, ys, covariates_mat)
    yt_pred_ = clf_.predict(xt)
    accuracy_after = accuracy_score(yt, yt_pred_)



    # Send results as JSON response
    response_data = {
        "accuracy_before": accuracy_before,
        "accuracy_after": accuracy_after,
        "graph_data": {
            "source": {"x": xs[:, 0].tolist(), "y": xs[:, 1].tolist(), "labels": ys.tolist()},
            "target": {"x": xt[:, 0].tolist(), "y": xt[:, 1].tolist(), "labels": yt.tolist()},
        }
    }

    return Response(response_data)
