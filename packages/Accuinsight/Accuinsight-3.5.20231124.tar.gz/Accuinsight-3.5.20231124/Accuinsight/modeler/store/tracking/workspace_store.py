import logging

from Accuinsight.modeler.utils.rest_utils_runsandbox import http_request, verify_rest_response
from Accuinsight.modeler.utils.os_getenv import get_os_env
from Accuinsight.modeler.core.LcConst import LcConst


class RestStore:
    def __init__(self, host_creds):
        if host_creds is None:
            raise Exception("host_creds cannot be None")

        self._host_creds = host_creds

    @property
    def host_creds(self):
        return self._host_creds

    @staticmethod
    def set_endpoint_uri(endpoint, mode, param):
        if mode == "alarm":
            return endpoint + '/alarm'
        elif mode == "run":
            return endpoint + '/afterRun'
        elif mode == "model_evaluation":
            return endpoint + '/experiment/{experimentId}/run'
        elif mode == "packageList":
            return endpoint + '/package/change?packageType=' + param
        else:
            return endpoint

    def call_endpoint(self, param, mode):
        env_value = get_os_env()

        endpoint = self.set_endpoint_uri('/project/{project}/workspace/{workspaceId}', mode, param)
        endpoint = endpoint.replace('{project}', str(env_value[LcConst.ENV_PROJECT_ID]))
        endpoint = endpoint.replace('{workspaceId}', str(env_value[LcConst.ENV_WORKSPACE_ID]))
        if '{experimentId}' in endpoint:
            endpoint = endpoint.replace('{experimentId}', str(env_value[LcConst.ENV_EXPERIMENT_ID]))

        try:
            if mode == "packageList":
                response = http_request(host_creds=self.host_creds, endpoint=endpoint, method='GET')
            else:
                response = http_request(host_creds=self.host_creds, endpoint=endpoint, method='POST', data=param)

            response = verify_rest_response(response, endpoint).text

        except Exception as e:
            logging.error("Modeler API server connection failed", e)
            response = None

        return response
