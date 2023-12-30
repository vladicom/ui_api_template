import configparser

global_config = configparser.ConfigParser()
global_config.sections()
global_config.read('test_config.ini')

class ConfigProvider:

    def __init__(self) -> None:
        self.config = global_config

    def get(self, section: str, prop: str):
        return self.config[section].get(prop)
    
    def getint(self, section: str, prop: str):
        return self.config[section].get(int(prop))
    
    def ui_url(self):
        return self.config["ui"].get("base_url")
    
    def api_url(self):
        return self.config['api'].get("base_url")