import io
import base64
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render
from sklearn.datasets import make_blobs
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from kale.pipeline.multi_domain_adapter import CoIRLS
from kale.interpret.visualize import distplot_1d

from .forms import ExampleForm

def run_example(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Get input values from form
            n_samples = form.cleaned_data['n_samples']
            lambda_value = form.cleaned_data['lambda_value']
            alpha_value = form.cleaned_data['alpha_value']
            
            # Generate toy data
            np.random.seed(29118)
            xs, ys = make_blobs(n_samples, centers=[[0, 0], [0, 2]], cluster_std=[0.3, 0.35])
            xt, yt = make_blobs(n_samples, centers=[[2, -2], [2, 0.2]], cluster_std=[0.35, 0.4])
            
            # Visualize toy data
            colors = ["c", "m"]
            x_all = [xs, xt]
            y_all = [ys, yt]
            labels = ["Source", "Target"]
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            for i in range(2):
                idx_pos = np.where(y_all[i] == 1)
                idx_neg = np.where(y_all[i] == 0)
                ax1.scatter(
                    x_all[i][idx_pos, 0],
                    x_all[i][idx_pos, 1],
                    c=colors[i],
                    marker="o",
                    alpha=0.4,
                    label=labels[i] + " positive",
                )
                ax1.scatter(
                    x_all[i][idx_neg, 0],
                    x_all[i][idx_neg, 1],
                    c=colors[i],
                    marker="x",
                    alpha=0.4,
                    label=labels[i] + " negative",
                )
            ax1.legend()
            ax1.set_title("Source and Target Domain Data", fontsize=14, fontweight="bold")

            # Save the figure to a buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            data_plot = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig1)

            # Train RidgeClassifier
            clf = RidgeClassifier(alpha=alpha_value)
            clf.fit(xs, ys)
            yt_pred = clf.predict(xt)
            accuracy1 = accuracy_score(yt, yt_pred)

            # Domain adaptation using CoIRLS
            clf_ = CoIRLS(lambda_=lambda_value)
            covariates = np.zeros(n_samples * 2)
            covariates[:n_samples] = 1
            enc = OneHotEncoder(handle_unknown="ignore")
            covariates_mat = enc.fit_transform(covariates.reshape(-1, 1)).toarray()
            x = np.concatenate((xs, xt))
            y = np.concatenate((ys, np.zeros_like(yt)))  # Assuming zero labels for unlabeled target data
            clf_.fit(x, y, covariates_mat)
            yt_pred_ = clf_.predict(xt)
            accuracy2 = accuracy_score(yt, yt_pred_)

            context = {
                'form': form,
                'data_plot': data_plot,
                'accuracy1': f"Accuracy on target domain: {accuracy1:.2f}",
                'accuracy2': f"Accuracy after adaptation: {accuracy2:.2f}",
            }

            return render(request, 'myapp/result.html', context)
    else:
        form = ExampleForm()

    return render(request, 'myapp/example_form.html', {'form': form})


def homepage(request):
    return render(request, 'myapp/homepage.html')  # Ensure this path matches the templates directory

