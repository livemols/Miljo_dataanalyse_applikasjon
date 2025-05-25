# This file make the class PredictiveAnalysis for predictive_analysis.ipynb

# This file has used ChatGPT (OpenAI) for troubleshooting and explanation of error codes.

import os
import sys 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, HuberRegressor, RANSACRegressor, TheilSenRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
import math
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error



# Read the right files from the right folders

base_dir = os.path.dirname(__file__)
data_path = os.path.abspath(os.path.join(base_dir, "..", "..", "data"))
original_file = "blindern_data_cleaning.csv"
original_path = os.path.join(data_path, original_file)
df = pd.read_csv(original_path, delimiter=";")



class PredictiveAnalysis:
    def __init__(self, df=None, X=None, y=None, X_train=None, X_test=None, y_train=None, y_test=None, linespace_values=None, col=None):
        self.df = df.copy() if df is not None else None
        self.X = X.copy() if X is not None else None
        self.y = y.copy() if y is not None else None
        self.X_train = X_train.copy() if X_train is not None else None
        self.X_test = X_test.copy() if X_test is not None else None
        self.y_train = y_train.copy() if y_train is not None else None
        self.y_test = y_test.copy() if y_test is not None else None
        self.linespace_values = linespace_values
        self.col = col

    def managing_categorial_data(self, df):

        # Sorting out the right columns
        df["Tid"] = pd.to_datetime(df["Tid"], format="%Y-%m-%d")
        df = df.drop(columns=[col for col in df.columns if df[col].nunique() == 1])
        df_modified = df.copy()

        # Convert 'Tid' to numeric

        df_modified["Tid_num"] = (df_modified["Tid"] - df_modified["Tid"].min()).dt.days
        df_modified["År"] = df_modified["Tid"].dt.year
        df_modified["Måned"] = df_modified["Tid"].dt.month
        df_modified = df_modified.drop(columns=['Tid'], errors='ignore')

        return df_modified
   
    def modells_prediction(self, X_train, y_train, linespace_values):

        X_train_values = X_train.values

        # List of modells
        models = {
            "Linear": LinearRegression(),
            "Huber": HuberRegressor(),
            "RANSAC": RANSACRegressor(random_state=42),
            "TheilSen": TheilSenRegressor(random_state=42),
            "Poly2": LinearRegression(),
            "Poly3": LinearRegression()
        }

        # Define the df for all of the modells
        fit_df = pd.DataFrame(index=linespace_values.flatten())

        # Linear modells
        for name in ["Linear", "Huber", "RANSAC", "TheilSen"]:
            model = models[name].fit(X_train_values, y_train)
            fit_df[name] = model.predict(linespace_values)

        # Polynomial 2. grad
        poly2 = PolynomialFeatures(degree=2)
        poly2_model = poly2.fit_transform(X_train_values)
        plot_poly2 = poly2.transform(linespace_values)
        models["Poly2"].fit(poly2_model, y_train)
        fit_df["Poly2"] = models["Poly2"].predict(plot_poly2)

        # Polynomial 3. grad
        poly3 = PolynomialFeatures(degree=3)
        poly3_model = poly3.fit_transform(X_train_values)
        plot_poly3 = poly3.transform(linespace_values)
        models["Poly3"].fit(poly3_model , y_train)
        fit_df["Poly3"] = models["Poly3"].predict(plot_poly3)

        return fit_df
    
    def plot_train_and_split(self, X_train, X_test, y, y_train, y_test):

        features = X_train.columns

        try:
            n_features = len(features)
            n_cols = 3
            n_rows = int(np.ceil(n_features / n_cols))

            # Checking for every day ('Tid_num'), every year ('År') and every month ('Måned')
            for col in y.columns:
                fig, axs = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
                axs = axs.flatten()  # axes need to be flatten

                for i, feature in enumerate(features):
                    ax = axs[i]
                    ax.scatter(X_train[feature], y_train[col], color="blue", label="Train", alpha=0.6)
                    ax.scatter(X_test[feature], y_test[col], color="red", label="Test", alpha=0.6)
                    ax.set_xlabel(feature)
                    ax.set_ylabel(col)
                    ax.legend()

                fig.suptitle(f'Scatterplots: {col} mot hver funksjon', fontsize=16)
                plt.tight_layout(rect=[0, 0, 1, 0.97])
                plt.show()
        except ValueError: 
            print('Ingen funksjoner å plotte!')

    def plot_polynomial_1to3(self, X_train, X_test, y_train, y_test):

        # Selected modells
        modell_definations = {
            "Linear": LinearRegression(),
            "Poly2": make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression()),
            "Poly3": make_pipeline(PolynomialFeatures(degree=3, include_bias=False), LinearRegression())
        }

        # Preparing a libary for all of the preditcions to every model
        predictions = {}

        for name, modell in modell_definations.items():
            modell.fit(X_train, y_train)
            y_pred = modell.predict(X_test)
            predictions[name] = y_pred

        # Columnnames
        feature_names = X_train.columns
        target_names = y_train.columns

        # Number of subplots
        num_targets = y_test.shape[1]
        num_cols = math.ceil(math.sqrt(num_targets))
        num_rows = math.ceil(num_targets / num_cols)

        # Plotting all of the modells in one loop
        for modelname, y_pred in predictions.items():
            fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(16, 10))
            axes = axes.flatten()
            
            for j in range(len(target_names)):
                ax = axes[j]
                ax.scatter(X_test.iloc[:, 0], y_test.iloc[:, j], label='Actual', alpha=0.5)
                ax.scatter(X_test.iloc[:, 0], y_pred[:, j], label='Predicted', alpha=0.6)

                ax.set_xlabel(f'{feature_names[0]}')
                ax.set_ylabel(f'{target_names[j]}')
                ax.set_title(f'{modelname} - {target_names[j]}')
                ax.legend()
            
            # Remove extra subplots
            for i in range(len(target_names), len(axes)):
                fig.delaxes(axes[i])
            
            fig.suptitle(f'Prediksjon med {modelname}', fontsize=16)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.show()

        return predictions

    def evaluation(self, predictions, y_train, y_test):

        target_names = y_train.columns

        # Results of evaluationvalues per modell
        evaluation = []

        for modelname, y_pred in predictions.items():
            # Sørg for 2D-format hvis bare én målvariabel
            if y_pred.ndim == 1:
                y_pred = y_pred.reshape(-1, 1)

            for i, target in enumerate(target_names):
                y_true = y_test.iloc[:, i]
                y_hat = y_pred[:, i]

                mae = mean_absolute_error(y_true, y_hat)
                mse = mean_squared_error(y_true, y_hat)
                r2 = r2_score(y_true, y_hat)

                evaluation.append({
                    'Modell': modelname,
                    'Målvariabel': target,
                    'MAE': mae,
                    'MSE': mse,
                    'R²': r2
                })

        # Converting 'evaluation' to a df
        eval_df = pd.DataFrame(evaluation)

        return eval_df

    def RandomForestRegressor_evaluation_egPlot(self, df, X_train, X_test, y_train, y_test, col):

        df_final = df.copy()
        results = []
        predictions = {}

        for target in y_train.columns:
            model = RandomForestRegressor()
            model.fit(X_train, y_train[target])

            y_pred = model.predict(X_test)
            predictions[target] = y_pred  # Saved for potenial use afterwards

            mae = mean_absolute_error(y_test[target], y_pred)
            mse = mean_squared_error(y_test[target], y_pred)
            r2 = r2_score(y_test[target], y_pred)

            results.append({
                "Målvariabel": target,
                "MAE": mae,
                "MSE": mse,
                "R²": r2
            })

            # Plotting for a col just to visualize and giving an example
            if target == col:
                # Adding 'Tid' if 'Tid' not in X_test
                tid_column = df_final.loc[X_test.index, 'Tid']
                
                # Make a DataFrame for both historic/empirically and predicted
                plot_df = pd.DataFrame({
                    'Tid': tid_column,
                    'Historisk': y_test[target].values,
                    'Predikert': y_pred
                })

                # Sort values after Tid
                plot_df = plot_df.sort_values(by='Tid')

                plt.figure(figsize=(10, 5))
                plt.plot(plot_df['Tid'], plot_df['Historisk'], label='Historisk')
                plt.plot(plot_df['Tid'], plot_df['Predikert'], label='Predikert', linestyle='--')
                plt.title(f'Historisk vs Predikert {col.lower()}')
                plt.xlabel('Tid')
                if 'temp' in col:
                    plt.ylabel('Temperatur (°C)')
                elif 'vind' in col:
                    plt.ylabel('Vind (m/s)')
                elif 'nedbør' in col.lower():
                    plt.ylabel('Nedbør (mm)')
                else:
                    plt.ylabel(col)
                plt.legend()
                plt.show()

        # Evaluation of the modell
        eval_df = pd.DataFrame(results)
    
        return eval_df
    
    def pred_amount_over_limits(self, X, y):
        # One model per one variable
        results = {}
        for col in y.columns:
            X_train, X_test, y_train, y_test = train_test_split(X, y[col], test_size=0.2, random_state=0)

            model = LinearRegression()
            model.fit(X_train, y_train)

            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)

            results[col] = {
                "model": model,
                "predictions": predictions,
                "mse": mse,
                "y_test": y_test,
                "coefficients": model.coef_
            }

            # Collecting all the tests and predictions into one dataframe for each of them
            y_tests_df = pd.DataFrame({col: results[col]["y_test"].values for col in results})
            y_preds_df = pd.DataFrame({col: results[col]["predictions"] for col in results})

        # Columnnames
        target_names = y_tests_df.columns
        feature_name = X_test.columns[0]  # 'Tid', antas bare én

        # Count of subplots
        num_targets = len(target_names)
        num_cols = math.ceil(math.sqrt(num_targets))
        num_rows = math.ceil(num_targets / num_cols)

        # Definate the figure
        fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(16, 10))

        # Ensure that the axes are flatten -onedimensional
        if isinstance(axes, np.ndarray):
            axes = axes.flatten()
        else:
            axes = [axes]

        # Plotting every weather variable
        for j, target in enumerate(target_names):
            ax = axes[j]
            ax.scatter(X_test[feature_name], y_tests_df[target], color='blue', label='Faktisk', alpha=0.5)
            ax.scatter(X_test[feature_name], y_preds_df[target], color='green', label='Predikert', alpha=0.6)
            # Plotting the regression line
            ax.plot(X_test[feature_name], y_preds_df[target], color='red', label='Regression Line', alpha=0.6)
            ax.grid(True)
            ax.set_xlabel('Tid')
             
            if isinstance(target, str) and 'temp' in target.lower():
                ax.set_ylabel('Temperatur (°C)')
            elif isinstance(target, str) and 'vind' in target.lower():
                ax.set_ylabel('Vind (m/s)')
            elif isinstance(target, str) and 'nedbør' in target.lower():
                ax.set_ylabel('Nedbør (mm)')
            else:
                ax.set_ylabel(target)

            ax.set_title(f'Trend for {target.lower()}')
            ax.legend()

        # Remove extra subplots
        for i in range(len(target_names), len(axes)):
            fig.delaxes(axes[i])

        fig.suptitle('Prediksjoner for værvariabler over tid', fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

        return results


















