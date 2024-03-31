import jenkins
from retry import retry
import os
import json

class JenkinsJob:
    def __init__(self):
        self._jenkins_url = os.getenv('INPUT_JENKINS_URL')
        self._jenkins_user = os.getenv('INPUT_JENKINS_USER')
        self._jenkins_password = os.getenv('INPUT_JENKINS_TOKEN')
        self._job_name = os.getenv('INPUT_JOB_NAME')
        self._parameters = self._get_job_params_in_dict()
        self._wait_for_build_result = bool(os.getenv('INPUT_WAIT'))

        self._jenkins_connection = jenkins.Jenkins(url= self._jenkins_url,
                                                   username=self._jenkins_user,
                                                   password=self._jenkins_password)
    

    def _get_job_params_in_dict(self):
        if os.getenv('INPUT_JOB_PARAMETERS') and os.getenv('INPUT_JOB_PARAMETERS') != '' :
            return json.loads(os.getenv('INPUT_JOB_PARAMETERS'))
        else:
            return {}
        
    @retry(ValueError, delay=20)
    def _wait_for_build_number(self, queued_item_id):
        queue_item_data = self._jenkins_connection.get_queue_item(queued_item_id)
        if 'executable' in queue_item_data:
            return queue_item_data['executable']['number']
        raise ValueError('Not correct Build Number')

    @retry(ValueError, delay=20)
    def _wait_for_job_to_start(self, queued_item_id):
        if self._jenkins_connection.get_queue_item(queued_item_id)['why'] is None:
            return True
        raise ValueError('Not correct Build Queue status')

    @retry(ValueError, delay=60)
    def _get_build_result(self, build_number):
        build_info = self._jenkins_connection.get_build_info(name=self._job_name, number=build_number)
        if not build_info['building']:
            return build_info['result']
        else:
            raise ValueError('Not correct Build Info status')
        
    def _build_jenkins_job(self):
        try:    
            return self._jenkins_connection.build_job(name=self._job_name, parameters=self._parameters)
        except Exception as e:
            raise e

    def _set_output(self, staus_value):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'status={staus_value}', file=fh)
    
    def trigger_jenkins_job(self):
        try:
            queued_item_id = self._build_jenkins_job()
            build_number = self._wait_for_build_number(queued_item_id=queued_item_id)
            build_url = f'{self._jenkins_url}/job/{self._job_name}/{build_number}/'
            print(f'Jenkins job triggered: {build_url}')
            if self._wait_for_build_result:
                result = self._get_build_result(build_number=build_number)
                self._set_output(staus_value=result)
            else:
                self._set_output(staus_value='TRIGGERED')
        except Exception as e:
            print(str(e))
            self._set_output(staus_value='ERROR_OCCURRED')

def main():
    for name, value in os.environ.items():
        print("{0}: {1}".format(name, value))
    JenkinsJob().trigger_jenkins_job()

if __name__ == "__main__":
    main()