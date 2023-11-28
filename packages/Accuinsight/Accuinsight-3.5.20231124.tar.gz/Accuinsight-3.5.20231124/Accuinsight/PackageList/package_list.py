import json
from Accuinsight.modeler.utils.os_getenv import get_os_env
from Accuinsight.modeler.clients.modeler_api_common import WorkspaceRestApi
from Accuinsight.modeler.core.LcConst import LcConst
from collections import OrderedDict


class PackageList:
    def __init__(self):
        self.packageList = OrderedDict()

    def call_api(self, param):
        env_value = get_os_env('ENV')
        modeler_rest = WorkspaceRestApi(env_value[LcConst.BACK_END_API_URL],
                                        env_value[LcConst.BACK_END_API_PORT],
                                        env_value[LcConst.BACK_END_API_URI])

        return modeler_rest.call_rest_api(param, 'packageList')

    def process_response(self, response):
        # JSON 파싱 및 데이터 처리
        try:
            parsed = json.loads(response)
            # print(json.dumps(parsed, indent=4, sort_keys=True)) # 응답 확인

            for item in parsed['data']['list']:
                self.packageList[item['name']] = item['version']
        except json.JSONDecodeError:
            print("JSON 파싱 오류가 발생했습니다.")

    def getCustomPackageList(self, packageType="pip"):
        # 유효한 packageType 검사
        if packageType not in ['all', 'pip', 'conda']:
            raise ValueError("packageType은 'all', 'pip', 'conda' 중 하나여야 합니다.")

        if packageType == 'all':
            # pip 패키지 리스트 처리
            self.packageList = OrderedDict()  # 패키지 리스트 초기화
            response = self.call_api('pip')
            self.process_response(response)
            print("\nAdded/Modified Pip Packages\n")
            for package, version in self.packageList.items():
                print(f'{package}=={version}')
            print("============================================================")
            # conda 패키지 리스트 처리
            self.packageList = OrderedDict()  # 패키지 리스트 초기화
            response = self.call_api('conda')
            self.process_response(response)
            print("\nAdded/Modified Conda Packages\n")
            for package, version in self.packageList.items():
                print(f'{package}=={version}')
        else:
            # 특정 타입의 패키지 리스트 처리
            self.packageList = OrderedDict()  # 패키지 리스트 초기화
            response = self.call_api(packageType)
            self.process_response(response)
            print("\nAdded/Modified " + packageType + " Packages\n\n")
            for package, version in self.packageList.items():
                print(f'{package}=={version}')

        # 안내는 ai runtime 통해서 모델 서빙 하려면 경로의 파일 넣어야함
        print('''
        \n============================================================
airuntime을 통한 모델 배포를 위해 아래 경로에 requirements 파일 추가\n
@주의: pytorch, sklearn, tensorflow 모델에 따라 파일 위치가 다릅니다.

<경로> 
/airuntime/{pytorch|sklearn|tensorflow}/requirements.txt --> 해당 파일(없으면 생성)에 아래 형태로 파일 작성
 
패키지==버전
패키지==버전
패키지==버전
...
...
...
패키지==버전
''')


        # print('''\n============================================================
        # 배포를 위한 requirements 파일 수정\n
        # <pip packages>
        # /airuntime/{pytorch|sklearn|tensorflow}/requirements.txt
        # 해당경로의 파일 수정\n
        # <conda packages>
        # /airuntime/{pytorch|sklearn|tensorflow}/requirements_conda.txt
        # 해당경로의 파일 수정\n
        # ''')