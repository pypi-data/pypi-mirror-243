import json
from Accuinsight.modeler.core.LcConst.LcConst import RUN_BASE_PATH, RUN_PREFIX_PATH, ALL_MODEL_PARAMS, \
    SELECTED_METRICS, SELECTED_PARAMS, RUN_OBJ_MODEL_JSON_PATH
from Accuinsight.modeler.protos.life_cycle_pb2 import LcParam, LcMetric
from Accuinsight.modeler.core.Run.ParseRun import Parse_Helper

def _makeLcParam(selected_params, all_model_params):
    grpc_params = []

    for param_key in selected_params:

        param = LcParam(
            key=param_key,
            value=str(all_model_params[param_key])
        )
        grpc_params.append(param)
    return grpc_params


def _append_metrics(metrics, **kwargs):
    values = []
    timestamp = []
    steps = []
    count = 0
    data = kwargs['data']
    key = kwargs['key']

    for v in data:
        values.append(str(v))
        timestamp.append(str(count))
        steps.append(str(count))
        count += 1
    metrics.append({'key': key,
                    'values': values,
                    'timestamp': timestamp,
                    'steps': steps})
    return metrics


def _parse_true_predict(metric_data, metrics):
    true_y = []
    predicted_y = []
    true_y_values = metric_data['True_y']
    predicted_y_values = metric_data['Predicted_y']

    # check if nested list
    is_nested_true = any(isinstance(elem, list) for elem in true_y_values)
    is_nested_predicted = any(isinstance(elem, list) for elem in predicted_y_values)

    if is_nested_true:
        for elem in true_y_values:
            true_y.append(elem[0])
    else:
        true_y = true_y_values

    if is_nested_predicted:
        for elem in predicted_y_values:
            predicted_y.append(elem[0])
    else:
        predicted_y = predicted_y_values

    metrics = _append_metrics(metrics, data=true_y, key='true_y')
    metrics = _append_metrics(metrics, data=predicted_y, key='predicted_y')
    return metrics


# parse parameters
def parse_run_parameters(json_data):
    # read ~/runs/results-XGBClassifier/model-info-json/*.json
    # return parameters

    param_data = json_data
    selected_params = param_data[SELECTED_PARAMS]
    all_model_params = param_data[ALL_MODEL_PARAMS]

    grpc_params = _makeLcParam(selected_params=selected_params, all_model_params=all_model_params)

    return grpc_params


# parse metrics
def _parse_selected_metrics(json_data):
    # read ~/runs/results-XGBClassifier/model-info-json/*.json
    # get "selected_metrics" field
    # return metrics

    metric_data = json_data

    grpc_metrics = []
    if SELECTED_METRICS not in metric_data:
        return grpc_metrics

    # selected_metrics
    selected_metrics = metric_data[SELECTED_METRICS]
    metric_keys = selected_metrics.keys()

    result_dict = {'metrics': []}

    count = 0
    timestamp = []
    steps = []
    values = []
    for key in metric_keys:
        values.append(str(selected_metrics[key]))
        timestamp.append(str(count))
        steps.append(key)
        count += 1

    result_dict['metrics'].append({
                                   'values': values,
                                   'timestamp': timestamp,
                                   'steps': steps})

    metrics = result_dict['metrics']

    for item in metrics:
        metric = LcMetric(
                key=SELECTED_METRICS,
                values=item['values'],
                timestamp=item['timestamp'],
                steps=item['steps']
            )
        grpc_metrics.append(metric)

    return grpc_metrics


def parse_run_metrics(json_data):
    # read ~/runs/results-XGBClassifier/model-info-json/*.json
    # get "selected_metrics" field
    # return metrics

    metrics = []
    metrics = _parse_true_predict(json_data, metrics)

    grpc_metrics = []

    for item in metrics:
        metric = LcMetric(
                key=item['key'],
                values=item['values'],
                timestamp=item['timestamp'],
                steps=item['steps']
            )
        grpc_metrics.append(metric)

    selected_metrics = _parse_selected_metrics(json_data=json_data)
    grpc_metrics = grpc_metrics + selected_metrics

    return grpc_metrics


# parse metrics
def _append_visual_data(visual_data, key):
    result_dict = {'metrics': []}

    count = 0
    timestamp = []
    steps = []
    values = []

    for k, v in visual_data.items():
        timestamp.append(str(count))
        count += 1

        steps.append(k)
        values.append(v)

    result_dict['metrics'].append({'key': key,
                                   'values': values,
                                   'timestamp': timestamp,
                                   'steps': steps})
    return result_dict


def _make_steps(steps_value):
    steps_list = []
    for value in steps_value:
        steps_list.append(str(value))
    return steps_list


def parse_run_result(run_info_json):
    result_dict = {'metrics': '', 'params': ''}

    grpc_params = parse_run_parameters(json_data=run_info_json)
    grpc_metrics = parse_run_metrics(json_data=run_info_json)

    result_dict['params'] = grpc_params
    result_dict['metrics'] = grpc_metrics

    return result_dict