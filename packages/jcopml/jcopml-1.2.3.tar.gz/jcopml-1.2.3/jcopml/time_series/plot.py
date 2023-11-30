import pandas as pd
import matplotlib.pyplot as plt
from .metric import _get_scorer


def plot_ets_fitted(model, y_train, scoring="rmse", figsize=(15, 3)):
    """
    Visualize fitted statsmodels.tsa model


    == Example usage ==
    plot_fitted(model, y_train, scoring="rmse")


    == Arguments ==
    y_train: pandas Series
        time series data

    model: statsmodels.tsa model
        fitted statsmodels.tsa model

    scoring: str
        If None, mean squared error would be used. Here are list of supported scorer:
        - mse   Mean Squared Error
        - mae   Mean Absolute Error
        - mape  Mean Absolute Percentage Error
        - msle  Mean Squared Log Error
        - rmse  Root Mean Squared Error
    """
    result = y_train.to_frame(name="series").copy()
    result["fitted"] = model.fittedvalues
    scoring, scorer = _get_scorer(scoring)
    score = scorer(result.series, result.fitted)

    plt.figure(figsize=figsize)
    plt.plot(result.series, "b-", label="train")
    plt.plot(result.fitted, "r--", label="fitted")
    plt.title(f"{scoring.upper()} = {score:.3f}")
    plt.legend(loc="upper left");
    return result, score
    

def plot_ets_forecast(model, y_train, y_test, n_prior=0, scoring="rmse", figsize=(15, 3)):
    train_result = y_train.to_frame(name="series").copy()
    train_result["fitted"] = model.fittedvalues
    
    test_result = model.forecast(len(y_test) + n_prior).to_frame(name="fitted").copy()
    test_result["series"] = y_test
    
    scoring, scorer = _get_scorer(scoring)
    train_score = scorer(train_result.series, train_result.fitted)    
    test_score = scorer(test_result.dropna().series, test_result.dropna().fitted)

    plt.figure(figsize=figsize)
    plt.plot(train_result.series, "b-", label="train")
    plt.plot(train_result.fitted, "r--", label="fitted")
    plt.plot(test_result.series, "k-", label="test")
    plt.plot(test_result.fitted, "m--", label="forecast")
    plt.title(f"Train {scoring.upper()} = {train_score:.3f} | Test {scoring.upper()} = {test_score:.3f}")
    plt.legend(loc="upper left");

    result = pd.concat([train_result, test_result])
    score = {"train": train_score, "test": test_score}
    return result, score
