from hashlib import sha256
import base64
from Crypto import Random
from Crypto.Cipher import AES
import json
import platform
import yaml
from yaml.loader import SafeLoader


class Snappyflow:
    def __init__(self):
        self.project_name = None
        self.app_name = None
        self.profile_data = None
        path = ''
        os_type = platform.system().lower()
        if os_type == 'windows' or os_type == 'win32':
            path = 'C:\\Program Files (x86)\\Sfagent\\config.yaml'
        else:
            path = '/opt/sfagent/config.yaml'
        # with open(path) as file:
        try:
            yaml_file = open(path)
            data = yaml.load(yaml_file, Loader=SafeLoader)
            # self.profile_key = 
            self.project_name = data['tags']['projectName']
            self.app_name = data['tags']['appName']
            self.profile_data = self._get_profile_data(data['key'])
        except Exception as ex:
            print('Can not read from config.yaml\nCall init method with parameters to initialize.')

    def init(self, profile_key, project_name, app_name):
        self.profile_data = self._get_profile_data(profile_key)
        self.project_name = project_name
        self.app_name = app_name

    def _get_profile_data(self, profile_key):

        unpad = lambda s : s[0:-ord(s[-1:])]
        CP_ENCRYPTED_KEY = "U25hcHB5RmxvdzEyMzQ1Ng=="
        key = base64.b64decode(CP_ENCRYPTED_KEY)
        
        enc = base64.b64decode(profile_key)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv )
        message = unpad(cipher.decrypt( enc[16:] )).decode('utf-8')
        return json.loads(message)

    def get_trace_config(self):
        """ Returns Snappyflow trace config

        Args:
            profile_key ([string]): [Snappyflow Profile Key]
            project_name ([string]): [Project name]
            app_name ([string]): [App name]

        Raises:
            ValueError: [If profile key is invalid]

        Returns:
            [dict]: [trace config]
        """    

        
        try:
            data = self.profile_data
            global_labels = "_tag_projectName={},_tag_appName={},_tag_profileId={}".format(
                self.project_name, self.app_name, data['profile_id'])
            trace_data = {
                'SFTRACE_SERVER_URL': data['trace_server_url'],
                'SFTRACE_SPAN_FRAMES_MIN_DURATION': "1ms",
                'SFTRACE_STACK_TRACE_LIMIT': 2,
                'SFTRACE_CAPTURE_SPAN_STACK_TRACES': False,
                'SFTRACE_VERIFY_SERVER_CERT': False,
                'SFTRACE_GLOBAL_LABELS': global_labels
            }
            return trace_data
        except Exception as e:
            # print("ex", e)
            raise ValueError("\nPlease check config.yaml file is present. Or \nInit method is called with appropriate values.")

def get_data_from_request(elasticapm, request):
    """ Returns request information for APM

    Args:
        request (obj): Contains http request information from User
    
    Returns:
        [dict] : ["headers", "method", "socket", "url"]

    """
    httprequest = request.httprequest
    data = {
        "headers": dict(**httprequest.headers),
        "method": httprequest.method,
        "socket": {
            "remote_address": httprequest.remote_addr,
            "encrypted": httprequest.scheme == "https",
        },
        "url": elasticapm.utils.get_url_dict(httprequest.url),
    }
    # remove Cookie header since the same data is in request["cookies"] as well
    data["headers"].pop("Cookie", None)
    return data

def begin_transaction(elasticapm, client, request):
    """ Begins Transaction for APM Tracing

    Args:
        elasticapm : Elastic APM package to set user context
        clinet : elastic APM client (To Begin transaction)
        request (obj): Contains http request information from User
    Returns:
        nil

    """
    client.begin_transaction(transaction_type="request")
    elasticapm.set_user_context(user_id=request.session.uid)

def end_transaction(elasticapm, client, request, response):
    """ Ends Transaction for APM Tracing

    Args:
        elasticapm : Elastic APM package to set user context
        clinet : elastic APM client (To End transaction)
        request (obj): Contains http request information from User
        response (obj): Contains http response information from User
    Returns:
        nil

    """
    path_info = request.httprequest.environ.get("PATH_INFO")
    name = path_info
    for key in ["model", "method", "signal"]:
        val = request.params.get(key)
        if val and val not in name:
            name += " {}: {}".format(key, val)
    elasticapm.set_context(lambda: get_data_from_request(elasticapm, request), "request")
    try:
        code = response.status_code
    except Exception:
        try:
            code = response.code
        except Exception:
            code = 100
    elasticapm.set_context(lambda: {"status_code" : code}, "response")
    if code and code >= 200 and code <=399:
        status = "success"
    else:
        status = "failed"
    client.end_transaction(name, status)