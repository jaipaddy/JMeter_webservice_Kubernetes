# JMeter_webservice_Kubernetes
Run Distributed JMeter Docker container pods in a secure Kubernetes cluster via a webservice. Granting everyone ssh access to their containers is a security risk. Containers are meant to write logs to a central location/service accessible external to the running container. As a result, `docker exec` and `kubectl exec` is forbidden. The recommended way/workaround to executing a CLI is by exposing a simple webservice that can accept run time parameters to be passed on to the CLI.
The runtime test parameters may be passed via a simple Http REST client such as Postman - 
![Alt text](test.png?raw=true "CLI Test execution")

and here is the sample output -
![Alt text](results.png?raw=true "Sample output")

Note the last line providing the Google Cloud Storage location to access the JMeter report dashboard. To enable authentication, follow [Setting up authentication](https://cloud.google.com/storage/docs/reference/libraries?authuser=1#client-libraries-install-python) and populate the `creds.env` file with appropriate values for the service account key and storage bucket. 
