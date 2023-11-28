import inspect
import json
import math
from collections import OrderedDict
import warnings
import logging
from joblib import dump
from sklearn import pipeline

from Accuinsight.modeler.core import func, path, get
from Accuinsight.modeler.core.func import get_time
from Accuinsight.modeler.core.get_for_visual import roc_pr_curve, get_true_y, get_visual_info_regressor
from Accuinsight.modeler.core.sklearnModelType import REGRESSION, CLASSIFICATION
from Accuinsight.modeler.core.LcConst.LcConst import ALL_MODEL_PARAMS, SELECTED_PARAMS, SELECTED_METRICS, VALUE_ERROR, \
    LOGGING_TIME, LOGGING_RUN_ID, FITTED_MODEL, USER_ID, RUN_OBJ_NAME, RUN_MODEL_JSON_PATH, RUN_MODEL_VISUAL_JSON_PATH, \
    RUN_MODEL_SHAP_JSON_PATH, RUN_MODEL_JOBLIB_PATH, RUN_ID
from Accuinsight.modeler.core.Run.RunInfo.RunInfo import set_current_runs, clear_runs, \
    set_git_meta, set_python_dependencies, set_run_name, set_model_json_path, set_visual_json_path, set_model_file_path, \
    set_prefix_path, set_best_model_joblib_path, _set_result_path, set_shap_json_path, set_best_model_json_path
from Accuinsight.modeler.core.LcConst import LcConst
from Accuinsight.modeler.utils.os_getenv import get_current_notebook, get_os_env
from Accuinsight.modeler.clients.modeler_api import LifecycleRestApi

from Accuinsight.modeler.core.feature_contribution import shap_value
from Accuinsight.modeler.core import metricsLightgbm
from Accuinsight.Lifecycle.common import Common
from Accuinsight.modeler.utils.file_path import get_file_path


logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

warnings.filterwarnings("ignore")


class accuinsight(Common):
    def __init__(self):
        global feature_name, alarm_api, message_param, user_id, \
            notebook_info, run_meta, run_nick_name, mail_alarm, mail_info
        super().__init__()

        feature_name = None
        user_id = None
        message_param = ''

        # alarm = self.workspace_alarm
        alarm_api = self.workspace_alarm_api
        notebook_info = self.notebook_info
        run_nick_name = self.default_run_nick_name
        mail_alarm = self.mail_alarm
        mail_info = self.mail_info

        run_meta = None

    def get_file(self, storage_json_file_name=None):
        global save_path, StorageInfo, target_name
        save_path, StorageInfo, target_name = super().get_file(storage_json_file_name)

    def set_features(self, feature_names):
        global feature_name
        feature_name = super().set_features(feature_names)

    def set_slack(self, hook_url=None):
        alarm_api.notifiers['slack'] = hook_url

    def unset_slack(self):
        if 'slack' in alarm_api.notifiers.keys():
            del alarm_api.notifiers['slack']

    # def set_mail(self, address=None):
    #     alarm.notifiers['mail'] = address
    #
    # def unset_mail(self):
    #     if 'mail' in alarm.notifiers.keys():
    #         del alarm.notifiers['mail']

    def unset_message(self):
        global message_param
        message_param = ''

    def set_user_id(self, uid):
        global user_id
        user_id = uid

    def unset_user_id(self):
        global user_id
        user_id = None

    def set_current_notebook(self):
        global notebook_info
        notebook_info = get_current_notebook()

    @staticmethod
    def get_current_run_meta():
        global run_meta
        return run_meta

    def get_current_run_id(self):
        try:
            return self.get_current_run_meta()[RUN_OBJ_NAME]
        except TypeError or KeyError:
            return None

    class add_experiment(object):
        def __init__(self, model_name, *args, model_monitor=False, runtime=False, f1_average_in='weighted', recall_average_in='weighted'):
            self.shap_on = model_monitor
            self.runtime = runtime
            logging.info('Using add_experiment(model_monitor={})'.format(model_monitor))
            if f1_average_in not in ['micro', 'macro', 'weighted']:
                raise ValueError("f1_average_in set micro|macro|weighted")
            if recall_average_in not in ['micro', 'macro', 'weighted']:
                raise ValueError("recall_average_in set micro|macro|weighted")

            if type(model_name) == pipeline.Pipeline:
                self.model_name = model_name.steps[-1][1]
            else:
                self.model_name = model_name

            _caller_globals = inspect.stack()[1][0].f_globals
            self.var_model_file_path, self.sources, self.dependencies = get_file_path(_caller_globals)

            if self.var_model_file_path is not None:
                print("filename: ", self.var_model_file_path)
            else:
                ValueError("filename을 찾을 수 없습니다.")

            self.fitted_model = get.model_type(self.model_name)          # fitted model type
            self.json_path = OrderedDict()                               # path
            self.selected_params = []                                    # log params
            self.selected_metrics = OrderedDict()                        # log metrics
            self.summary_info = OrderedDict()                            # final results
            self.error_log = []                                          # error log
            self.vis_info = None                                         # visualization info - classifier
            self.dict_path = path.get_file_path(self.model_name)

            set_current_runs(get.model_type(self.model_name))
            _set_result_path(self.dict_path)

            # data for visualization function
            if len(args) == 3:
                self.xval = args[1]
                self.yval = args[2]
                self.summary_info['run_nick_name'] = args[0]

            elif len(args) == 5:
                self.xtrain = args[1]
                self.ytrain = args[2]
                self.xval = args[3]
                self.yval = args[4]
                self.summary_info['run_nick_name'] = args[0]

            # 사용자가 run_nick_name 파라미터 입력 안했을 경우
            # ex1) with accu.add_experiment(model, X_train_scaled, y_train_num, X_test_scaled, y_test_num, model_monitor=True, runtime=True) as exp:
            # ex2) with accu.add_experiment(model, X_test_scaled, y_test_num, model_monitor=True, runtime=True) as exp:
            elif len(args) == 2:
                self.xval = args[0]
                self.yval = args[1]
                self.summary_info['run_nick_name'] = run_nick_name

            elif len(args) == 4:
                self.xtrain = args[0]
                self.ytrain = args[1]
                self.xval = args[2]
                self.yval = args[3]
                self.summary_info['run_nick_name'] = run_nick_name

            else:
                raise ValueError('Check the arguments of function - add_experiment(model_name, run_nick_name, X_val, y_val) or add_experiment(model_name, run_nick_name, X_train, y_train, X_val, y_val)',
                                 '\n and No assign run_nick_name, set default run_nick_name as File name.')

            # 사용자가 run_nick_name 파라미터를 지정했는데 '' 일 경우
            if args[0] == '':
                self.summary_info['run_nick_name'] = run_nick_name

            # sklearn/xgboost/lightgbm
            get_from_model = get.from_model(self.model_name)
            self.all_model_params = get_from_model.all_params()

            if 'metric' not in self.all_model_params.keys():
                self.all_model_params['metric'] = ''

            self.model_param_keys = get_from_model.param_keys()
            
            # classifier
            if any(i in self.fitted_model for i in CLASSIFICATION):
                self.vis_info = roc_pr_curve(self.xval, self.yval, model=self.model_name ,f1_average=f1_average_in, recall_average=recall_average_in)

            # regressor
            elif any(i in self.fitted_model for i in REGRESSION):
                self.ypred = get_visual_info_regressor(self.xval, model=self.model_name)
            
            # if user uses lightgbm package, verify the model for classification or regression.
            if self.fitted_model == 'lightgbm':
                print('lightgbm.')
                # classifier
                if self.all_model_params['metric'] in metricsLightgbm.CLASSIFICATION:
                    self.vis_info = roc_pr_curve(self.xval, self.yval, model=self.model_name, f1_average=f1_average_in, recall_average=recall_average_in)
                
                # regressor
                elif self.all_model_params['metric'] in metricsLightgbm.REGRESSION:
                    self.ypred = get_visual_info_regressor(self.xval, model=self.model_name)
                
                # None
                elif self.all_model_params['metric'] in metricsLightgbm.no_metrics:
                    raise ValueError('Please set any metric parameter in the lightGBM.')
            
            set_model_file_path(self.var_model_file_path)

            if hasattr(self, 'mainfile'):
                set_git_meta(fileinfo=self.mainfile)
            if hasattr(self, 'dependencies'):
                set_python_dependencies(py_depenpency=self.dependencies)

        def __enter__(self):
            self.start_time = get_time.now()
            self.summary_info[LOGGING_TIME] = get_time.logging_time()
            self.summary_info[LOGGING_RUN_ID] = func.get_run_id()
            self.summary_info[FITTED_MODEL] = self.fitted_model

            if user_id is not None:
                self.summary_info[USER_ID] = user_id

            set_prefix_path(self.dict_path[LcConst.RUN_PREFIX_PATH])
            set_run_name(self.fitted_model, self.summary_info[LOGGING_RUN_ID], self.summary_info['run_nick_name'])

            return self

        def __exit__(self, a, b, c):
            self.summary_info[ALL_MODEL_PARAMS] = self.all_model_params
            for key in self.summary_info[ALL_MODEL_PARAMS]:
                if isinstance(self.summary_info[ALL_MODEL_PARAMS][key], float) and math.isnan(self.summary_info[ALL_MODEL_PARAMS][key]):
                    self.summary_info[ALL_MODEL_PARAMS][key] = None
            self.summary_info[SELECTED_PARAMS] = self.selected_params
            self.summary_info[SELECTED_METRICS] = self.selected_metrics
            self.summary_info[VALUE_ERROR] = self.error_log

            # model_monitor = True
            self.run_id = self.summary_info[LOGGING_RUN_ID]
            
            if self.shap_on:
                if not feature_name:
                    try:
                        if self.data is not None:
                            self.feature_name = get.feature_name(save_path, StorageInfo, target_name, data=self.data)
                            self.data = None
                        else:
                            self.feature_name = get.feature_name(save_path, StorageInfo, target_name)
                    except:
                        self.feature_name = None
                else:
                    self.feature_name = feature_name

                self.run_id = self.fitted_model + '-' + self.run_id
                
                # when user uses lightGBM fitted by lightGBM datasets, convert data type to lightGBM dataset.
                if self.fitted_model == 'lightgbm':
                    self.xtrain = lgb.Dataset(self.xtrain, label=self.ytrain, silent=True)
                        
                self.shap_value = shap_value(self.model_name, self.xtrain, self.feature_name)
                
                # path for shap.json
                shap_json_full_path = self.dict_path[RUN_MODEL_SHAP_JSON_PATH]
                set_shap_json_path(self.dict_path['shap_json'])
                
                with open(shap_json_full_path, 'w', encoding='utf-8') as save_file:
                    json.dump(self.shap_value, save_file, indent='\t')
                
            # visualization
            if any(i in self.fitted_model for i in CLASSIFICATION) or self.all_model_params['metric'] in metricsLightgbm.CLASSIFICATION:

                # path for visual.json
                visual_json_full_path = self.dict_path[RUN_MODEL_VISUAL_JSON_PATH]
                set_visual_json_path(self.dict_path['visual_json'])

                with open(visual_json_full_path, 'w', encoding='utf-8') as save_file1:
                    json.dump(self.vis_info, save_file1, indent="\t")

            elif any(i in self.fitted_model for i in REGRESSION) or self.all_model_params['metric'] in metricsLightgbm.REGRESSION:
                temp_yval = get_true_y(self.yval)
                if len(temp_yval) <= 5000:
                    self.summary_info['True_y'] = temp_yval
                    self.summary_info['Predicted_y'] = get_visual_info_regressor(self.xval, model=self.model_name)
                else:
                    self.summary_info['True_y'] = None
                    self.summary_info['Predicted_y'] = None

            self.summary_info[VALUE_ERROR] = self.error_log

            if not self.summary_info[VALUE_ERROR]:
                # path for model_info.json
                model_json_full_path = self.dict_path[RUN_MODEL_JSON_PATH]
                set_model_json_path(self.dict_path['model_json'])

                with open(model_json_full_path, 'w', encoding='utf-8') as save_file2:
                    json.dump(self.summary_info, save_file2, indent="\t")
                    
            else:
                pass

            # model save
            save_model_path = self.dict_path[RUN_MODEL_JOBLIB_PATH] + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.joblib'
            path_for_setting_model_json = self.dict_path['save_model_dir'] + '/' + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.json'
            path_for_setting_model_joblib = self.dict_path['save_model_dir'] + '/' + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.joblib'

            # /best_model/ directory 저장하고 나중에 불러와서 run_info에 set할때 run/ 붙임.
            browser_common_path = self.dict_path['save_model_dir'] + '/' + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID]
            browser_model_json_path = browser_common_path + '.json'
            browser_model_joblib_path = browser_common_path + '.joblib'

            # best model save as JSON
            summary_info_json_for_evl = self.summary_info.copy()
            summary_info_json_for_evl[ALL_MODEL_PARAMS] = self.summary_info[ALL_MODEL_PARAMS]
            summary_info_json_for_evl[SELECTED_PARAMS] = self.summary_info[SELECTED_PARAMS]
            summary_info_json_for_evl[RUN_ID] = self.summary_info[LOGGING_RUN_ID]
            summary_info_json_for_evl['path'] = self.var_model_file_path
            summary_info_json_for_evl[FITTED_MODEL] = self.summary_info[FITTED_MODEL]
            summary_info_json_for_evl['model_dependencies'] = self.dependencies
            summary_info_json_for_evl['best_model_joblib'] = browser_model_joblib_path
            summary_info_json_for_evl['best_model_json'] = browser_model_json_path
            save_model_json_path = self.dict_path[RUN_MODEL_JOBLIB_PATH] + self.summary_info[FITTED_MODEL] + '-' + self.summary_info[LOGGING_RUN_ID] +'.json'
            with open(save_model_json_path, 'w', encoding='utf-8') as json_file:
                json.dump(summary_info_json_for_evl, json_file, indent="\t")

            set_best_model_json_path(path_for_setting_model_json)
            set_best_model_joblib_path(path_for_setting_model_joblib)

            dump(self.model_name, save_model_path)

            start_time = int(self.start_time.timestamp()*1000)
            end_time = int(get_time.now().timestamp()*1000)
            delta_ts = end_time - start_time

            global run_meta
            run_meta = clear_runs(start_time, end_time, delta_ts)

            accuinsight._send_message(metric=None,
                                      current_value=None,
                                      message=message_param,
                                      thresholds=None,
                                      alarm_object=None, #modeler alarm api deprecated
                                      alarm_api=alarm_api)

            env_value = get_os_env('ENV')
            modeler_rest = LifecycleRestApi(env_value[LcConst.BACK_END_API_URL],
                                            env_value[LcConst.BACK_END_API_PORT],
                                            env_value[LcConst.BACK_END_API_URI])
            modeler_rest.lc_create_run(run_meta)
            if self.runtime:
                accuinsight.set_runtime_model('sklearn')

        def log_params(self, param=None):
            # sklearn/xgboost/lightgbm
            if param:
                if param in self.model_param_keys:
                    return self.selected_params.append(param)

                else:
                    self.error_log.append(True)
                    raise ValueError('"' + param + '"' + ' does not exist in the model.')

        def log_metrics(self, metric_name, defined_metric):
            self.selected_metrics[metric_name] = defined_metric

        def log_tag(self, description):
            self.summary_info['tag'] = description
