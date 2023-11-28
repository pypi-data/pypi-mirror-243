import json
from collections.abc import Mapping
from Accuinsight.modeler.core.LcConst.LcConst import RUN_RESULT_PATH, RUN_MODEL_VISUAL_JSON_PATH, RUN_OBJ_IS_EVALUATION, \
                                                    RUN_MODEL_EVL_JSON_PATH


# parse metrics
def _append_visual_data(visual_data, key):
    result_dict = {'metrics': []}

    count = 0
    timestamp = []
    steps = []
    values = []

    for k, v in visual_data.items():
        if isinstance(v, Mapping):
            v_keys = v.keys()

            # set values
            v_values = []
            v_values[0:0] = list(v.values())
            values.append(v_values)

            # set timestamp
            # timestamp.append(str(count))
            # count += 1

            # set steps
            for v_key in v_keys:
                steps.append('_'.join([k, v_key]))
        else:
            timestamp.append(str(count))
            count += 1

            steps.append(k)

            values.append(v)

    result_dict['metrics'].append({'key': key,
                                   'values': values,
                                   'timestamp': timestamp,
                                   'steps': steps})
    return result_dict


def _parse_visual_data(visual_data):
    result_dict = {'metrics': []}

    # get keys of visual_data
    keys_visual = visual_data.keys()
    # dict_keys(['fpr', 'tpr', 'roc_auc', 'recall', 'precision', 'average_precision', 'confusion_matrix'])

    for key in keys_visual:
        if isinstance(visual_data[key], Mapping):
            visual_result = _append_visual_data(visual_data[key], key)
            result_dict['metrics'].append(visual_result['metrics'][0])
        else:
            timestamp = list(range(0, len(visual_data[key])))
            steps = list(range(0, len(visual_data[key])))
            result_dict['metrics'].append({'key': key,
                                           'values': visual_data[key],
                                           'timestamp': timestamp,
                                           'steps': steps})

    return result_dict


def _make_visual_values(visual_value, key):
    result = {'listValue': [], 'value': []}

    is_list_nested = any(isinstance(i, list) for i in visual_value)

    if is_list_nested:
        listINlist = []
        for item in visual_value:
            listINlist.append({'values' : item})
        ListOfListOfValues = {
            'values' : listINlist
        }
        result['listValue'].append(ListOfListOfValues)
    else:
        to_string_values = []
        for v in visual_value:
            to_string_values.append(str(v))
        ListOfValues = {
            'values' : to_string_values
        }
        result['value'].append(ListOfValues)

    return result


def _make_steps(steps_value):
    steps_list = []
    for value in steps_value:
        steps_list.append(str(value))
    return steps_list


def parse_run_visual(run_mata):
    # parse 'for-visual-json/keras-visual-n.json'
    run_result_path = run_mata[RUN_RESULT_PATH]
    if run_mata[RUN_OBJ_IS_EVALUATION]=='true':
        visual_path = run_result_path[RUN_MODEL_EVL_JSON_PATH]
        print("Set evaluation path.", visual_path)
    else:
        visual_path = run_result_path[RUN_MODEL_VISUAL_JSON_PATH]

    with open(visual_path) as visual_file:
        visual_data = json.load(visual_file)

    result_dict = {'metrics': []}

    grpc_metrics = []

    # visual metrics
    visual_result = _parse_visual_data(visual_data)

    for item in visual_result['metrics']:
        result_dict['metrics'].append(item)

    metrics = result_dict['metrics']

    # count = 0
    nested_values_lists = []
    values_lists = []

    for item in metrics:
        count = 0
        timestamps = []
        timestamp_count = len(item['steps'])
        for v in range(0, timestamp_count):
            timestamps.append(str(count))
            count += 1
        nested_values = _make_visual_values(item['values'], key=item['key'])['listValue']
        values = _make_visual_values(item['values'], key=item['key'])['value']

        visual = {
            'key': item['key'],
            'listValues': nested_values,
            'values': values,
            'timestamp': timestamps,
            'steps': _make_steps(item['steps'])
        }
        if not visual['listValues']:
            del visual['listValues']
        else:
            del visual['values']
        grpc_metrics.append(visual)

    return grpc_metrics
