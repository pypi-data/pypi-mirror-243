import numpy as np

DICT_DEFAULT_PARAMS = {
    "XGBRegressor": {
        "n_estimators": {"values": np.arange(50, 501), "dtype": int},
        "learning_rate": {"values": np.linspace(0.001, 0.9, 50), "dtype": float},
        "max_depth": {"values": np.arange(3, 11), "dtype": int},
        "gamma": {"values": np.linspace(0, 0.5, 50), "dtype": float},
        "min_child_weight": {"values": np.arange(1, 11), "dtype": int},
        "subsample": {"values": np.linspace(0.5, 1.0, 6), "dtype": float},
        "colsample_bytree": {"values": np.linspace(0.5, 1.0, 6), "dtype": float},
        "reg_alpha": {"values": np.linspace(0, 1, 100), "dtype": float}
    },
    "GradientBoostingRegressor": {
        "n_estimators": {"values": np.arange(50, 501), "dtype": int},
        "learning_rate": {"values": np.linspace(0.001, 0.9, 50), "dtype": float},
        "max_depth": {"values": np.arange(3, 11), "dtype": int},
        "subsample": {"values": np.linspace(0.5, 1.0, 6), "dtype": float},
        "min_samples_split": {"values": np.arange(2, 11), "dtype": int},
        "min_samples_leaf": {"values": np.arange(1, 11), "dtype": int}
    },
    "RandomForestRegressor": {
        "n_estimators": {"values": np.arange(50, 501), "dtype": int},
        "max_depth": {"values": np.arange(3, 11), "dtype": int},
        "min_samples_split": {"values": np.arange(2, 11), "dtype": int},
        "min_samples_leaf": {"values": np.arange(1, 11), "dtype": int}
    },
    "Ridge": {
        "alpha": {"values": np.linspace(0.01, 10, 100), "dtype": float}
    },
    "Lasso": {
        'alpha': {'values': np.linspace(0.0001, 1, 100), 'dtype': float},
        'max_iter': {'values': np.arange(100, 2001, 100), 'dtype': int},
        'tol': {'values': np.linspace(0.0001, 0.01, 100), 'dtype': float},
        'selection': {'values': ['cyclic', 'random'], 'dtype': str}
    }
}