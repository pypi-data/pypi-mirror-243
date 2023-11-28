"""
this is SHGS python package(version2) - single hyperparameter grid search
we will set one hyperparameter to be the target hyperparameter;
we will give all hyperparameters a range space;
In each round:
    for target hyperparameter, all the values in the range space will be run and recorded;
    for other hyperparameters, we will only choose one value from the range space in each round;
to use this package, the user should follow these steps:
    1. choose one hyperparameter to be the target hyperparameter;
        GS_space(grid search space);
        give GS_space the target hyperparameter and its range space
    2. give range spaces for all hyperparameters(including the target hyperparameter);
        GS_space(random search space);
        give GS_space all hyperparameters and their range spaces
Compared to the first version, the aim of this version is store the test auc for all datasets
By using grid search, we could push one hyperparameter setting into it each time,
and then use the model to do the prediction on test dataset and record the auc value.
For recording the result, should change the output.py to store the the test auc value
"""
import sys
sys.path.append('../')
import random
import numpy as np
from sklearn.model_selection import GridSearchCV, StratifiedKFold
import keras.optimizers as opt
from sklearn.metrics import roc_curve, auc
from keras import regularizers
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
"""write table"""
import copy
class SHGS:
    def __init__(self,g_space, r_space,iter):
        self.g_space = g_space
        self.r_space = r_space
        self.iter = iter
        self.hyperparameter_settings = []
        self.get_hyperparameter_settings()
        #print(self.hyperparameter_settings)
    def create_a_network(self,number_of_hidden_layer,low, high):
        network = []
        for i in range(number_of_hidden_layer):
            network.append(random.randint(low, high))
        network.append(1)
        return tuple(network)
    def choose_background_hyperparameters_setting_for_one_iter(self):
        random_hyperparameters = list(self.r_space.keys())
        if "number_of_hidden_layer" in random_hyperparameters and "number_of_hidden_nodes" in random_hyperparameters:
            random_params = {}
            number_of_hidden_layer, number_of_hidden_nodes = random.sample(self.r_space['number_of_hidden_layer'],1)[0], self.r_space['number_of_hidden_nodes']
            random_params['mstruct'] = [self.create_a_network(number_of_hidden_layer, low=number_of_hidden_nodes[0], high=number_of_hidden_nodes[-1])]
            for k, v in self.r_space.items():
                if k =='number_of_hidden_layer' or k == 'number_of_hidden_nodes': continue
                random_params[k] = random.sample(list(self.r_space[k]), 1)
                if isinstance(random_params[k][0], np.float64):
                    random_params[k][0] = round(random_params[k][0],5)
            # for k, v in self.g_space.items(): #add parameters in grid search into random_params
            #     random_params[k] = v
            return random_params
        elif "number_of_hidden_nodes" in random_hyperparameters:
            random_params = {}
            #number_of_hidden_layer, number_of_hidden_nodes = self.g_space['number_of_hidden_layer'], self.r_space['number_of_hidden_nodes']
            #mstruct = []
            #for i in number_of_hidden_layer:
            #    mstruct.append(self.create_a_network(i,low=number_of_hidden_nodes[0], high=number_of_hidden_nodes[-1]))
            #random_params['mstruct'] = mstruct
            for k, v in self.r_space.items():
                if k =='number_of_hidden_layer' or k == 'number_of_hidden_nodes': continue
                random_params[k] = random.sample(list(self.r_space[k]), 1)
                if isinstance(random_params[k][0], np.float64):
                    random_params[k][0] = round(random_params[k][0],5)
            return random_params
        elif "number_of_hidden_layer" in random_hyperparameters:
            """
            eg. if the range of nodes number is 3000, number of layer is 3, there will be 3000*3000*3000 possibilites
            question: if we set 'number of nodes' to be the target feature, the number of nodes in which layer we should fix?
            """
            pass
    def get_hyperparameter_settings(self):
        random_hyperparameters = list(self.r_space.keys())
        if "number_of_hidden_layer" in random_hyperparameters and "number_of_hidden_nodes" in random_hyperparameters:
            for i in range(self.iter):
                for k, target_values in self.g_space.items(): #Only one k which is the target hyperparameter
                    hyperparameters = self.choose_background_hyperparameters_setting_for_one_iter()
                    for value in target_values:
                        hyperparameters[k] = [value]
                        hyperparameters_copy = copy.deepcopy(hyperparameters)
                        self.hyperparameter_settings.append(hyperparameters_copy)
        elif "number_of_hidden_nodes" in random_hyperparameters:
            for i in range(self.iter):
                number_of_hidden_layer_range = self.g_space['number_of_hidden_layer']
                hyperparameters = self.choose_background_hyperparameters_setting_for_one_iter()
                number_of_hidden_nodes = self.r_space['number_of_hidden_nodes']
                for number_of_hidden_layer in number_of_hidden_layer_range:
                    mstruct = [self.create_a_network(number_of_hidden_layer, low=number_of_hidden_nodes[0],high=number_of_hidden_nodes[-1])]
                    hyperparameters['mstruct'] = mstruct
                    hyperparameters_copy = copy.deepcopy(hyperparameters)
                    self.hyperparameter_settings.append(hyperparameters_copy)
        elif "number_of_hidden_layer" in random_hyperparameters:
            """
            eg. if the range of nodes number is 3000, number of layer is 3, there will be 3000*3000*3000 possibilites
            question: if we set 'number of nodes' to be the target feature, the number of nodes in which layer we should fix?
            """
            pass
    def create_model(self,mstruct, idim, drate, kinit, iacti, hacti, oacti, opti, lrate, momen, dec, ls, L1, L2, ltype):
        # create a model that KerasClassifier needs as an input for parameter build_fn
        model = Sequential()
        if ltype == 0:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti))
        elif ltype == 1:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti,
                            kernel_regularizer=regularizers.l1(L1)))
        elif ltype == 2:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti,
                            kernel_regularizer=regularizers.l2(L2)))
        elif ltype == 3:
            model.add(Dense(mstruct[0], input_dim=idim, kernel_initializer=kinit, activation=iacti,
                            kernel_regularizer=regularizers.l1_l2(l1=L1, l2=L2)))

        model.add(Dropout(drate))
        nlayers = len(mstruct)
        nhiddenlayers = nlayers - 2
        for i in range(nhiddenlayers):
            model.add(Dense(mstruct[i + 1], activation=hacti))
            model.add(Dropout(drate))
        model.add(Dense(mstruct[nlayers - 1], activation=oacti))
        # Using 'softmax' as the activation function for the output layer will return all 0.5s when class is binary

        for layer in model.layers:
            print(layer.weights)
        cur_opt = opti
        if opti == 'Adagrad':
            cur_opt = opt.Adagrad(lr=lrate, decay=dec)
        elif opti == 'SGD':
            cur_opt = opt.SGD(lr=lrate, momentum=momen, decay=dec)
        elif opti == 'adam':
            cur_opt = opt.Adam(lr=lrate,decay=dec)
        elif opti == 'Nadam':
            cur_opt = opt.Nadam(lr=lrate,decay=dec)
        elif opti == 'Adamax':
            cur_opt = opt.Adamax(lr=lrate,decay=dec)
        model.compile(optimizer=cur_opt, loss=ls, metrics="accuracy")
        return model

    def train_one_grid_search(self, index, X_train, Y_train, nsplits, scores, seed):
        cur_cv = StratifiedKFold(n_splits=nsplits, shuffle=True, random_state=seed)
        clf = KerasClassifier(build_fn=self.create_model)
        g_search = GridSearchCV(clf, param_grid=self.hyperparameter_settings[index], cv=cur_cv, refit='AUC',scoring=scores, return_train_score=True, n_jobs=10)
        gs = g_search.fit(X=X_train, y=Y_train)
        print('train successfully!!!')
        return gs
    # def train_and_write_in_grid_search(self,X_train, Y_train, X_test, Y_test, nsplits, scores, seed,result_path,table,experiment_des):
    #     for index in range(len(self.hyperparameter_settings)):
    #         print('********************',index,'******************')
    #         start_time = datetime.now()
    #         gs = self.train_one_grid_search(index,X_train, Y_train, nsplits, scores, seed)
    #         test_auc_grid = self.test(X_test,Y_test,gs)
    #         end_time = datetime.now()
    #         self.write_one_train_and_test_grid_search_result(result_path,table,experiment_des,start_time, end_time, seed, nsplits,gs,[test_auc_grid],index)
    def test(self, X_test, Y_test, gs):
        pred_grid = gs.predict_proba(X_test)[:, 1]
        pred_grid = pred_grid.reshape(-1)
        FP, TP, thresholds = roc_curve(Y_test.astype(float), pred_grid.astype(float))
        test_auc_grid = auc(FP, TP)
        #print('*****************test_auc_grid')
        #print(test_auc_grid)
        return test_auc_grid
    # def write_one_train_and_test_grid_search_result(self,result_path,table,experiment_des,start_time, end_time, seed, split,grid_result,testAUC_results,index):
    #     output.writetable(tablename=result_path,
    #                       tabletype=1,  # cross valication level 1 or two
    #                       table=table,
    #                       grid_result=grid_result,
    #                       experiment_iden="comparative",
    #                       experiment_description=experiment_des,
    #                       ml_classifier_name="deep learning keras",
    #                       # Has to enter "deep learning keras" because its error plot is different from other sk methods.
    #                       start_time=start_time,
    #                       end_time=end_time,
    #                       seed=seed,
    #                       split=split,
    #                       cpu_state=cpuinformation.record_cpu_information(),
    #                       testAUC_results=testAUC_results,
    #                       plot_roc=False,
    #                       plot_learning_curve=False,
    #                       plot_feature_importance=False,  # can work now
    #                       validation_array=None,
    #                       combined_validation_auc=None,
    #                       ifAppearRocParameter=False,
    #                       ifStoreROCData=False,
    #                       ifStoreErrorData=False,
    #                       id = index,
    #                       )