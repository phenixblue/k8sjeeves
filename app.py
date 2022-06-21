from ntpath import join
from pprint import pprint
from flask import Flask
from flask import send_file
from flask import jsonify, request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World!'


@app.route('/execute_k8s_task', methods=['POST'])
def execute_k8s_task():

    k8s_action = request.form.get("Field_k8s_action_Value")
    k8s_resource = request.form.get("Field_k8s_resource_Value")
    k8s_namespace = request.form.get("Field_k8s_namespace_Value")

    message = None

    if k8s_namespace is None:
        print("Namespace was not passed, using \"default\"")
        k8s_namespace = "default"

    if k8s_action is None or k8s_resource is None:
        message = "Sorry, I didn't quite catch that. Can you repeat?"

    if message is None:
        if k8s_action == "list":
            if k8s_resource == "pod":
                message = {}
                pod_list = listPods(k8s_namespace)
                message = "The following pods were found: " + ", ".join(pod_list)
            elif k8s_resource == "deployment":
                message = {}
                deployment_list = listDeployments(k8s_namespace)
                message = "The following deployments were found: " + ", ".join(deployment_list)
            else:
                message = f"The resource {k8s_resource} isn't one of \"pod\" or \"deployment\". Please try again."
        #elif k8s_action == "get":
        #    if k8s_resource == "pod":
        #        message = "get pod"
        #    elif k8s_resource == "deployment":
        #        message = "get deploys"
        #    else: 
        #        message = f"The resource {k8s_resource} isn't one of \"pod\" or \"deployment\". Please try again."
        #elif k8s_action == "restart":
        #    message = "restart"
        #elif k8s_action == "delete":
        #    message = "delete"
        else:
            message = f"The action {k8s_action} was not recognized. Please try again"

        return jsonify(actions=[{"say": message}, {"listen": True}])
 
@app.route('/test', methods=['POST'])
def test_route():
    message = {}
    pod_list = listPods("kube-system")
    print(dir(pod_list))
    pods = ", ".join(pod_list)
    message = f"The following pods were found: , {pods}"
    return jsonify(actions=[{"say": message}, {"listen": True}])

def listDeployments(k8s_namespace):

    message = []

    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
        except config.ConfigException:
            raise Exception("Could not configure kubernetes python client")

    v1 = client.AppsV1Api()

    deployment_list = None

    try:
        deployment_list = v1.list_namespaced_deployment(namespace=k8s_namespace)
    except ApiException as exception:

        if exception.reason == "Not Found":
            message = "No deployments were found."
            return message
        else:
            message = exception
            return message
 
    for deploy in deployment_list.items:
        message.append(deploy.metadata.name)

    return message

def listPods(k8s_namespace):

    message = []

    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
        except config.ConfigException:
            raise Exception("Could not configure kubernetes python client")

    v1 = client.CoreV1Api()

    pod_list = None

    try:
        pod_list = v1.list_namespaced_pod(namespace=k8s_namespace)
    except ApiException as exception:

        if exception.reason == "Not Found":
            message = "No pods were found."
            return message
        else:
            message = exception
            return message
 
    for pod in pod_list.items:
        message.append(pod.metadata.name)

    return message
