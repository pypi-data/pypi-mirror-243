import sys

import numpy as np
import pandas as pd

from .metrics_bci import MetricsBCI


class InputTreatment:
    def __init__(self, data, variables, model_label):
        self.variables = variables
        self.model_label = model_label
        self.univariate_table, self.selected_vars = self.univ_predict(
            data, self.variables, self.model_label
        )

    def filt_corr(self, df_in, corr_threshold=0.7, method="pearson", family=False):
        pred_var = self.univariate_table
        if family:
            pred_var["Group"] = "SinGrupo"

        selected_variables = []
        for group in pred_var["Group"].unique():
            variables = pred_var[pred_var["Group"] == group]["Feature"]
            selected_variables.append(self._identify_correlated(df_in[variables], 0.9))
        seleccionadas = self._flatten(selected_variables)

        print(f"\nVariables candidatas iniciales: {len(self.selected_vars)}")
        print(f"\nSeleccionadas por correlación familiar: {len(seleccionadas)}")
        return seleccionadas

    @staticmethod
    def univ_predict(df_in, variables, model_label):
        data_model = df_in.copy()
        pred_var = []
        total_variables = len(variables)

        for it, f in enumerate(variables):
            sys.stdout.write(f"\rProcesando [{it+1}/{total_variables}]" + "\r")
            metricas = MetricsBCI.evaluate(
                data_model[model_label], data_model[f].astype(float)
            )
            grupo_var = f.split("_")[0]
            pred_var.append([f, grupo_var, metricas[0], metricas[1], metricas[2]])

        pred_var = pd.DataFrame(
            pred_var, columns=["Feature", "Group", "ROC", "KS", "DIV"]
        )

        # En base a criterios de KS y ROC se selecciona las Variables que sobrepasen
        # un valor al ser consideradas predictivas.
        print(
            f"Variables candidatas iniciales: {len(variables)}",
        )
        pred_var_filtered = pred_var.loc[
            (pred_var["KS"] > 0.01) & (pred_var["ROC"] > 0.501), :
        ]
        seleccionadas = list(pred_var_filtered["Feature"].values)
        print(f"\nSeleccionadas por univariado: {len(seleccionadas)}")

        return pred_var_filtered, seleccionadas

    @staticmethod
    def filldata(df_in, num_value=-999999, cat_value="unk"):
        data = df_in.copy()
        for col in data.columns:
            try:
                data[col] = data[col].fillna(num_value)
            except:
                data[col] = data[col].cat.add_categories(cat_value)
                data[col] = data[col].fillna(cat_value, inplace=True)

        return data

    @staticmethod
    def _flatten(list_):
        return [item for sublist in list_ for item in sublist]

    @staticmethod
    def _identify_correlated(df, threshold):
        """
        A function to identify highly correlated features.
        """
        # Compute correlation matrix with absolute values
        matrix = df.corr(method="spearman").abs()

        # Create a boolean mask
        mask = np.triu(np.ones_like(matrix, dtype=bool))

        # Subset the matrix
        reduced_matrix = matrix.mask(mask)

        # Find cols that meet the threshold
        to_drop = [
            c for c in reduced_matrix.columns if not any(reduced_matrix[c] > threshold)
        ]

        return to_drop
