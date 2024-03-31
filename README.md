## Jenkins client
Use this package to trigger jobs remotely from GitHub action.


#### Required to use the client

- Jenkins server url
- Username and password (or API key) for the Jenkins server


### GitHub Action usage
You can use this package as a GitHub Action to trigger a job remotely and optionally wait for the job's result.
The action parameters are the following:

| Parameter                          | Required  | Description                                                                  |
|------------------------------------|-----------|------------------------------------------------------------------------------|
| `job_name`                 | Yes | The name of the job to trigger                                               |
| `job_parameters`           | No | A dictionary of parameters to pass to the job                                |
| `jenkins_url`                 | Yes | The url of the jenkins server                                                |
| `jenkins_user`                     | Yes | The username for the jenkins server                                          |
| `jenkins_password`                 | Yes | The password/token for the jenkins server                                    |
| `wait` | No | If set to true, the action will wait for the job to finish _(default: False)_ |

**Note**
`jenkins_job_parameters` and `wait` should be quoted as in the example below.

#### Example of usage:
```yaml
jobs:
  start-jenkins-job:
    runs-on: ubuntu-latest
    steps:
      - name: Start Jenkins job
        uses: NathanelLevi/Jenkins_job_runner@main
        with:
          job_name: 'some_job_name'
          job_parameters: '{"APP_ENV_NAME": "staging"}'
          jenkins_url: 'https://my-jenkins-instance.com/'
          jenkins_user: ${{ secrets.JENKINS_USER }}
          jenkins_password: ${{ secrets.JENKINS_PASSWORD }}
          wait: 'True'

      - name: Print the status
        run: echo "${{ steps.run_job.outputs.job-status }}"
```

###### Contact QA team in order to add more actions to the package.
