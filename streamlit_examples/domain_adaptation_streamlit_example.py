import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.datasets import make_blobs
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from kale.interpret.visualize import distplot_1d
from kale.pipeline.multi_domain_adapter import CoIRLS
import streamlit as st


# CONSTANTS
N_SAMPLES = 200


def generate_toy_data():
    np.random.seed(29118)
    # Generate toy data
    xs, ys = make_blobs(N_SAMPLES, centers=[[0, 0], [0, 2]], cluster_std=[0.3, 0.35])
    xt, yt = make_blobs(N_SAMPLES, centers=[[2, -2], [2, 0.2]], cluster_std=[0.35, 0.4])

    return xs, ys, xt, yt

def generate_ridge_data(xs, ys, xt, yt):
    clf = RidgeClassifier(alpha=1.0)
    clf.fit(xs, ys)

    yt_pred = clf.predict(xt)
    accuracy = accuracy_score(yt, yt_pred)

    ys_score = clf.decision_function(xs)
    yt_score = clf.decision_function(xt)

    return accuracy, ys_score, yt_score

def generate_domain_data():
    pass



def main():
    xs, ys, xt, yt = generate_toy_data() 
    
    # convert to streamlit counterpart
    # colors = ["c", "m"]
    # x_all = [xs, xt]
    # y_all = [ys, yt]
    # labels = ["source", "Target"]
    # plt.figure(figsize=(8, 5))
    # for i in range(2):
    #     idx_pos = np.where(y_all[i] == 1)
    #     idx_neg = np.where(y_all[i] == 0)
    #     plt.scatter(
    #         x_all[i][idx_pos, 0],
    #         x_all[i][idx_pos, 1],
    #         c=colors[i],
    #         marker="o",
    #         alpha=0.4,
    #         label=labels[i] + " positive",
    #     )
    #     plt.scatter(
    #         x_all[i][idx_neg, 0],
    #         x_all[i][idx_neg, 1],
    #         c=colors[i],
    #         marker="x",
    #         alpha=0.4,
    #         label=labels[i] + " negative",
    #     )
    # plt.legend()
    # plt.title("Source domain and target domain blobs data", fontsize=14, fontweight="bold")
    # plt.show()


    acc, ys_score, yt_score = generate_ridge_data(xs, ys, xt, yt)
    accuracy_score_txt = "Accuracy on target domain: {:.2f}".format(acc)
    print(accuracy_score_txt)
    

    # convert to streamlit counterpart
    title = "Ridge classifier decision score distribution"
    title_kwargs = {"fontsize": 14, "fontweight": "bold"}
    hist_kwargs = {"kde": True, "alpha": 0.7}
    plt_labels = ["Source", "Target"]
    
    distplot_1d(
        [ys_score, yt_score],
        labels=plt_labels,
        xlabel="Decision Scores",
        title=title,
        title_kwargs=title_kwargs,
        hist_kwargs=hist_kwargs,
    ).show()

    # domain adaptation
    clf_ = CoIRLS(lambda_=1)
    # encoding one-hot domain covariate matrix
    covariates = np.zeros(N_SAMPLES * 2)
    covariates[:N_SAMPLES] = 1
    enc = OneHotEncoder(handle_unknown="ignore")
    covariates_mat = enc.fit_transform(covariates.reshape(-1, 1)).toarray()

    x = np.concatenate((xs, xt))
    clf_.fit(x, ys, covariates_mat)
    yt_pred_ = clf_.predict(xt)
    print("Accuracy on target domain: {:.2f}".format(accuracy_score(yt, yt_pred_)))

    ys_score_ = clf_.decision_function(xs).detach().numpy().reshape(-1)
    yt_score_ = clf_.decision_function(xt).detach().numpy().reshape(-1)
    title = "Domain adaptation classifier decision score distribution"

    
    distplot_1d(
        [ys_score_, yt_score_],
        labels=plt_labels,
        xlabel="Decision Scores",
        title=title,
        title_kwargs=title_kwargs,
        hist_kwargs=hist_kwargs,
    ).show()


if __name__ == "__main__":
    main()
    input()