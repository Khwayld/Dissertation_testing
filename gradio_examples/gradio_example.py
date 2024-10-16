import io
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import gradio as gr
from sklearn.datasets import make_blobs
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

from kale.interpret.visualize import distplot_1d
from kale.pipeline.multi_domain_adapter import CoIRLS


def run_example(n_samples=200, lambda_value=1.0, alpha_value=1.0):
    np.random.seed(29118)
    # Generate toy data
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
    plt.close(fig1)  # Close the figure to prevent it from displaying in non-Gradio environments

    # Train RidgeClassifier
    clf = RidgeClassifier(alpha=alpha_value)
    clf.fit(xs, ys)
    yt_pred = clf.predict(xt)
    accuracy1 = accuracy_score(yt, yt_pred)

    # Visualize decision scores before adaptation
    ys_score = clf.decision_function(xs)
    yt_score = clf.decision_function(xt)
    title = "Ridge Classifier Decision Score Distribution"
    title_kwargs = {"fontsize": 14, "fontweight": "bold"}
    hist_kwargs = {"kde": True, "alpha": 0.7}
    plt_labels = ["Source", "Target"]
    fig2 = distplot_1d(
        [ys_score, yt_score],
        labels=plt_labels,
        xlabel="Decision Scores",
        title=title,
        title_kwargs=title_kwargs,
        hist_kwargs=hist_kwargs,
    )
    plt.close(fig2)

    # Domain adaptation using CoIRLS
    clf_ = CoIRLS(lambda_=lambda_value)
    # Encoding one-hot domain covariate matrix
    covariates = np.zeros(n_samples * 2)
    covariates[:n_samples] = 1
    enc = OneHotEncoder(handle_unknown="ignore")
    covariates_mat = enc.fit_transform(covariates.reshape(-1, 1)).toarray()

    x = np.concatenate((xs, xt))
    y = np.concatenate((ys, np.zeros_like(yt)))  # Assuming zero labels for unlabeled target data
    clf_.fit(x, y, covariates_mat)
    yt_pred_ = clf_.predict(xt)
    accuracy2 = accuracy_score(yt, yt_pred_)

    # Visualize decision scores after adaptation
    ys_score_ = clf_.decision_function(xs).detach().numpy().reshape(-1)
    yt_score_ = clf_.decision_function(xt).detach().numpy().reshape(-1)
    title = "Adapted Classifier Decision Score Distribution"
    fig3 = distplot_1d(
        [ys_score_, yt_score_],
        labels=plt_labels,
        xlabel="Decision Scores",
        title=title,
        title_kwargs=title_kwargs,
        hist_kwargs=hist_kwargs,
    )
    plt.close(fig3)

    # Return figures and accuracy scores
    return (
        fig1,
        f"Accuracy on target domain: {accuracy1:.2f}",
        fig2,
        f"Accuracy after adaptation: {accuracy2:.2f}",
        fig3,
    )


iface = gr.Interface(
    fn=run_example,
    inputs=[
        gr.Number(value=200, label="Number of Samples"),
        gr.Number(value=1.0, label="Lambda Value"),
        gr.Number(value=1.0, label="Alpha Value"),
    ],
    outputs=[
        gr.Plot(label="Data Plot"),
        gr.Textbox(label="Accuracy on Target Domain"),
        gr.Plot(label="Decision Scores Before Adaptation"),
        gr.Textbox(label="Accuracy After Adaptation"),
        gr.Plot(label="Decision Scores After Adaptation"),
    ],
    title="Domain Adaptation Example with Gradio",
    description="Interactively adjust parameters and visualize the effects on domain adaptation.",
)

iface.launch()