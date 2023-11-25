from . import make_component
from abstract_utilities import create_new_name
class GlobalWindowManager:
    def __init__(self):
        self.global_windows = {}
        self.current_window = None  # you can change this as per the window you're working with
        self.event = None
        self.values = None
        self.undesignated_value_keys = []
    def add_window(self,window_name=None,default_name=True,match_true=False,*args,**kwargs):
        window_name = create_new_name(name=window_name,names_list=list(self.global_windows.keys()),default=default_name,match_true=match_true)
        self.global_windows[window_name]=make_component('Window',*args,**kwargs)
        return window_name
    def close_window(self, window_name):
        if window_name in self.global_windows:
            self.global_windows[window_name].close()  # Assuming your window object has a close method
            del self.global_windows[window_name]
    def set_current_window(self, window_name):
            self.current_window = self.global_windows.get(window_name)

    def update_value(self, key, value=None, args=None):
        if self.current_window:
            if args:
                self.current_window[key].update(**args)
            elif value:
                self.current_window[key].update(value=value)
        else:
            print("No current window set!")

    def read_window(self):
        if self.current_window:
            self.event, self.values = self.current_window.read()
            return self.event, self.values
        else:
            print("No current window set!")
            return None, None

    def get_event(self):
        if not self.event:
            self.read_window()
        return self.event

    def get_values(self):
        if not self.values:
            self.read_window()
        return self.values

    def get_from_value(self, key, default=None, delim=None):
        self.get_values()
    def get_from_value(self,key,default=None,delim=None):
        self.get_values()
        if key not in self.values:
            print(f'{key} has no value')
            if key not in self.undesignated_value_keys:
                self.undesignated_value_keys.append(key)
                print('undesignated_value_keys: \n',self.undesignated_value_keys)
            return
        value = self.values[key]
        if delim != None:
            if value == delim:
                return default
        return value
