import os
thisFile = os.path.realpath(__file__)
packageFolder = os.path.dirname(thisFile)
package = os.path.basename(packageFolder)
if os.getcwd() != packageFolder:
    os.chdir(packageFolder)
configFile = os.path.join(packageFolder, "config.py")
if not os.path.isfile(configFile):
    open(configFile, "a", encoding="utf-8").close()
from autoassistant import config
from autoassistant.health_check import HealthCheck
if not config.openaiApiKey:
    HealthCheck.changeAPIkey()
    HealthCheck.saveConfig()
    print("Updated!")
HealthCheck.checkCompletion()

import autogen, os, json, traceback, geocoder, platform, socket, getpass, datetime, pendulum, netifaces, requests
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit import prompt
#from prompt_toolkit.styles import Style
#from prompt_toolkit import PromptSession
#from prompt_toolkit.history import FileHistory


class AutoGenAssistant:

    def __init__(self):
        #config_list = autogen.get_config_list(
        #    [config.openaiApiKey], # assume openaiApiKey is in place in config.py
        #    api_type="openai",
        #    api_version=None,
        #)
        oai_config_list = []
        for model in ("gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"):
            oai_config_list.append({"model": model, "api_key": config.openaiApiKey})
        os.environ["OAI_CONFIG_LIST"] = json.dumps(oai_config_list)

    def getResponse(self, message, auto=False):

        message = f"""Current device information is given below:
{self.getDeviceInfo()}

Below is my message:
{message}"""

        config_list = autogen.config_list_from_json(
            env_or_file="OAI_CONFIG_LIST",  # or OAI_CONFIG_LIST.json if file extension is added
            filter_dict={
                "model": {
                    config.chatGPTApiModel,
                }
            }
        )

        assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config={
                #"cache_seed": 42,  # seed for caching and reproducibility
                "config_list": config_list,  # a list of OpenAI API configurations
                "temperature": config.chatGPTApiTemperature,  # temperature for sampling
                "timeout": 300,
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )
        # create a UserProxyAgent instance named "user_proxy"
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER" if auto else "ALWAYS",
            max_consecutive_auto_reply=config.max_consecutive_auto_reply,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": os.path.join(config.letMeDoItAIFolder, "coding") if hasattr(config, "letMeDoItAIFolder") else "coding",
                "use_docker": False,  # set to True or image name like "python:3" to use docker
            },
        )
        # the assistant receives a message from the user_proxy, which contains the task description
        user_proxy.initiate_chat(
            assistant,
            message=message,
        )

    def get_wan_ip(self):
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']

    def get_local_ip(self):
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                for address in addresses[netifaces.AF_INET]:
                    ip = address['addr']
                    if ip != '127.0.0.1':
                        return ip

    def getDayOfWeek(self):
        now = pendulum.now() 
        return now.format('dddd')

    def getDeviceInfo(self):
        g = geocoder.ip('me')
        if hasattr(config, "thisPlatform"):
            thisPlatform = config.thisPlatform
        else:
            thisPlatform = platform.system()
            if thisPlatform == "Darwin":
                thisPlatform = "macOS"
        wan_ip = self.get_wan_ip()
        local_ip = self.get_local_ip()
        dayOfWeek = self.getDayOfWeek()
        return f"""Operating system: {thisPlatform}
Version: {platform.version()}
Machine: {platform.machine()}
Architecture: {platform.architecture()[0]}
Processor: {platform.processor()}
Hostname: {socket.gethostname()}
Username: {getpass.getuser()}
Python version: {platform.python_version()}
Python implementation: {platform.python_implementation()}
Current directory: {os.getcwd()}
Current time: {str(datetime.datetime.now())}
Current day of the week: {dayOfWeek}
Wan ip: {wan_ip}
Local ip: {local_ip}
Latitude & longitude: {g.latlng}
Country: {g.country}
State: {g.state}
City: {g.city}"""

    def print(self, message):
        #print(message)
        print_formatted_text(HTML(message))

    def run(self):
        auto = False
        self.print("Do you want auto-reply (y/yes/N/NO)?")
        userInput = prompt(default="NO")
        if userInput.strip().lower() in ("y", "yes"):
            auto = True
            self.print("Enter maximum consecutive auto-reply below:")
            max_consecutive_auto_reply = prompt(default=str(config.max_consecutive_auto_reply),)
            try:
                if max_consecutive_auto_reply and int(max_consecutive_auto_reply) > 1:
                    config.max_consecutive_auto_reply = int(max_consecutive_auto_reply)
            except:
                print("Invalid entry!")

        self.print("AutoGen Assistant launched!")
        self.print("[press 'ctrl+q' to exit]")
        while True:
            self.print("New chat started!")
            self.print("Enter your message below:")
            self.print("(To quit, enter '.exit')")
            message = prompt()
            if message == config.exit_entry:
                break
            try:
                self.getResponse(message, auto)
            except:
                self.print(traceback.format_exc())
                break
        self.print("\n\nAutoGen Assistant closed!")

def main():
    AutoGenAssistant().run()

if __name__ == '__main__':
    main()