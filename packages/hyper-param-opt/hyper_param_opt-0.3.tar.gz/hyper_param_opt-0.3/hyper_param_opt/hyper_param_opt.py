import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from default_params import DICT_DEFAULT_PARAMS

class GWOSearch:
    def __init__(self, model, x_train, y_train, x_test, y_test, dict_params=None, target="r2", int_population_size=5, int_num_iterations=5, flag_use_default=1):
        self.model = model
        str_model_nm = type(self.model).__name__
        self.model_name = str_model_nm
        print(self.model_name)
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        
        self.target = target
        self.int_population_size = int_population_size
        self.int_num_iterations = int_num_iterations
        
        self.flag_use_default = flag_use_default
        self.flag_skip = 0
        
        self.dict_best_hyperparameters = None
        self.best_model_ = None
        
        self.DICT_DEFAULT_PARAMS = DICT_DEFAULT_PARAMS

        self.dict_search_spaces = dict_params
        self.dict_param_types = {}
        
        if not self.dict_search_spaces:
            if self.flag_use_default:
                self.dict_search_spaces = self.DICT_DEFAULT_PARAMS.get(str_model_nm, {})
                if not self.dict_search_spaces:
                    self.flag_skip = 1
                    
                for key, value in self.dict_search_spaces.items():
                    self.dict_param_types[key] = value["dtype"]
                    self.dict_search_spaces[key] = value["values"]
            else:
                self.flag_skip = 1
        else:
            for key, value in self.dict_search_spaces.items():
                self.dict_param_types[key] = value["dtype"]
                self.dict_search_spaces[key] = value["values"]


    def orig_to_index(self, param_name, value):
        expected_dtype = self.dict_param_types[param_name]
        
        if expected_dtype in [int, float]:
            if not isinstance(value, expected_dtype):
                return expected_dtype(value)
            
            return value
        
        else:
            if value in self.dict_search_spaces[param_name]:
                return self.dict_search_spaces[param_name].index(value)
            else:
                raise ValueError(f"Value {value} not found in search space for parameter {param_name}.")

    
    def index_to_orig(self, param_name, index):
        param_values = self.dict_search_spaces[param_name]
        expected_dtype = self.dict_param_types[param_name]
    
        # For numerical types, find the nearest index in the search space
        if expected_dtype in [int, float]:
            if not isinstance(index, expected_dtype):
                return expected_dtype(index)
            
            return index
        
        # Ensure the index is an integer if it"s a float
        index = int(round(index)) if isinstance(index, float) else index
    
        # For bool or mixed (bool/str), ensure index is within valid range
        if index < 0:
            index = 0
        elif index >= len(param_values):
            index = len(param_values) - 1  
    
        return param_values[index]


    def create_model(self, params):
        self.model.set_params(**params)
        
        return self.model


    def clip_lst_population(self, lst_population):
        for i in range(lst_population.shape[0]):  
            for j, param_name in enumerate(self.dict_search_spaces.keys()): 
                param_type = self.dict_param_types[param_name]
                lst_population[i, j] = self.index_to_orig(param_name, lst_population[i, j])
                
                if param_type in [int, float]:
                    # For numerical types, clip the values to the min/max of the search space
                    min_val = np.min(self.dict_search_spaces[param_name])
                    max_val = np.max(self.dict_search_spaces[param_name])
                    lst_population[i, j] = np.clip(lst_population[i, j], min_val, max_val)
                else:
                    # For categorical types, ensure the value is within the search space
                    if lst_population[i, j] not in self.dict_search_spaces[param_name]:
                        # If the value is not in the search space, randomly select one from the search space
                        lst_population[i, j] = np.random.choice(self.dict_search_spaces[param_name])
                
        return lst_population


    def fitness_function(self, params):
        model = self.create_model(params)
        model.fit(self.x_train, self.y_train)
        predictions = model.predict(self.x_test)


       
        dict_target = {
                "mae": mean_absolute_error(self.y_test, predictions),
                "mape": mean_absolute_percentage_error(self.y_test, predictions) * 100,
                "rmse": np.sqrt(mean_squared_error(self.y_test, predictions)),
                "r2": -r2_score(self.y_test, predictions),
        }
            
        return dict_target.get(self.target)


    def evaluate_model(self):
        if self.dict_search_spaces:
            model = self.create_model(self.dict_best_hyperparameters)
        else:
            model = self.model
        
        model.fit(self.x_train, self.y_train)
        predictions = model.predict(self.x_test)
        

     
        mae = mean_absolute_error(self.y_test, predictions)
        mape = mean_absolute_percentage_error(self.y_test, predictions) * 100
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)
            
        return (mae, mape, rmse, r2)
    
    
    def best_model(self):
        if self.best_model_ is not None:
            return self.best_model_
        else:
            print("No best model found. Please run 'run()' first.")
            return self.model
    
        
    def best_param(self):
        if self.dict_best_hyperparameters is not None:
            return self.dict_best_hyperparameters
        else:
            print("No best model found. Please run 'run()' first.")
            return None
          
            
    def run(self):
        if self.flag_skip:
            print("[Info] Optimization skipped. Returning default model parameters.")
            self.evaluate_model()
        else:
            print("[Info] Optimization running. Please wait...")
            num_params = len(self.dict_search_spaces)
            lst_population = np.empty((self.int_population_size, num_params), dtype=object)
            
            for i in range(self.int_population_size):
                for j, param_name in enumerate(self.dict_search_spaces.keys()):
                    value = np.random.choice(self.dict_search_spaces[param_name])
                    
                    # Check for "True"/"False" strings and convert to boolean
                    if value == "True":
                        value = True
                    elif value == "False":
                        value = False
                    
                    lst_population[i, j] = value
                    
            best_score = float("inf")
            
            for iteration in range(self.int_num_iterations):
                print(f"This is {iteration+1} iteration")
    
                # Convert current lst_population to indices for calculation
                lst_population_indices = np.copy(lst_population)
                
                for i in range(self.int_population_size):
                    for j, param_name in enumerate(self.dict_search_spaces.keys()):
                        lst_population_indices[i, j] = self.orig_to_index(param_name, lst_population[i, j])
            
                fitness = [self.fitness_function({key: wolf[idx] for idx, key in enumerate(self.dict_search_spaces.keys())}) for wolf in lst_population]
                sorted_idx = np.argsort(fitness)
                
                alpha = lst_population_indices[sorted_idx[0]]
                beta = lst_population_indices[sorted_idx[1]]
                delta = lst_population_indices[sorted_idx[2]]
                
                a = 2 * (1 - (iteration / self.int_num_iterations))
                
                for i in range(self.int_population_size):
                    for j, param_name in enumerate(self.dict_search_spaces.keys()):
                        lst_population[i, j] = self.orig_to_index(param_name, lst_population[i, j])
                        
                        r1, r2 = np.random.random(), np.random.random()
                        A1, C1 = 2 * a * r1 - a, 2 * r2
                        r1, r2 = np.random.random(), np.random.random()
                        A2, C2 = 2 * a * r1 - a, 2 * r2
                        r1, r2 = np.random.random(), np.random.random()
                        A3, C3 = 2 * a * r1 - a, 2 * r2
                       
                        D_alpha = abs(C1 * alpha[j] - lst_population[i, j])
                        D_beta = abs(C2 * beta[j] - lst_population[i, j])
                        D_delta = abs(C3 * delta[j] - lst_population[i, j])
    
                        lst_population[i, j] = (alpha[j] - A1 * D_alpha + beta[j] - A2 * D_beta + delta[j] - A3 * D_delta) / 3
    
                # Clip the lst_population values based on the search space
                lst_population = self.clip_lst_population(lst_population)
               
                # Update the best hyperparameters if a better one is found
                if fitness[sorted_idx[0]] < best_score:
                    best_score = fitness[sorted_idx[0]]
                    best_hyperparameters_indices = {key: alpha[idx] for idx, key in enumerate(self.dict_search_spaces.keys())}
                    # Transform indices back to original values
                    self.dict_best_hyperparameters = {key: self.index_to_orig(key, value) for key, value in best_hyperparameters_indices.items()}
                    
                    # Save the best model
                    self.best_model_ = self.create_model(self.dict_best_hyperparameters)
                    #self.best_model_.fit(self.x_train, self.y_train.values.ravel())
                    self.best_model_.fit(self.x_train, self.y_train)


class AutoML:  
    def __init__(self, lst_model_info, x_train, y_train, x_test, y_test, target="r2", int_population_size=5, int_num_iterations=5, flag_use_default=1):
        self.lst_gwo_search_objects = []
        self.dict_model_to_gwo = {}
        self.lst_results = []
        self.target = target
        
        for dict_model_info in lst_model_info:
            gwo_search_obj = GWOSearch(
                model=dict_model_info["model"],
                x_train=x_train, 
                y_train=y_train, 
                x_test=x_test, 
                y_test=y_test, 
                dict_params=dict_model_info["dict_hyper_params"], 
                target=target, 
                int_population_size=int_population_size, 
                int_num_iterations=int_num_iterations,
                flag_use_default=flag_use_default
            )
            self.lst_gwo_search_objects.append(gwo_search_obj)
            self.dict_model_to_gwo[gwo_search_obj.model_name] = gwo_search_obj


    def run(self):
        for gwo_search_obj in self.lst_gwo_search_objects:
            gwo_search_obj.run()


    def evaluate_model(self):
        self.lst_results = []
        
        for gwo_search_obj in self.lst_gwo_search_objects:
            tup_target_value = gwo_search_obj.evaluate_model()  # (mae, mape, rmse, r2)
  
            result_dict = {
                    "model_name": gwo_search_obj.model_name,
                    "mae": tup_target_value[0],
                    "mape": tup_target_value[1],
                    "rmse": tup_target_value[2],
                    "r2": tup_target_value[3]
            }
                
            self.lst_results.append(result_dict)
        
        return self.lst_results


    def best_model(self):
        if not self.lst_results:
            self.evaluate_model()
        
        dict_best_result = max(self.lst_results, key=lambda x: x[self.target]) if self.target in ["r2"] else min(self.lst_results, key=lambda x: x[self.target])
        best_model_name = dict_best_result["model_name"]
        best_gwo_search_obj = self.dict_model_to_gwo[best_model_name]  
        print(f"Best model is : {best_gwo_search_obj.model_name}")
        
        return best_gwo_search_obj.best_model_


    def best_param(self):
        if not self.lst_results:
            self.evaluate_model()
        
        dict_best_result = max(self.lst_results, key=lambda x: x[self.target]) if self.target in ["r2"] else min(self.lst_results, key=lambda x: x[self.target])
        best_model_name = dict_best_result["model_name"]
        best_gwo_search_obj = self.dict_model_to_gwo[best_model_name]  
        
        return best_gwo_search_obj.dict_best_hyperparameters
