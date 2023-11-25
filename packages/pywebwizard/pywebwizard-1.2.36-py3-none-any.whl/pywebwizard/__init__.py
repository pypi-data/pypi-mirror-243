from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as _ec
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from copy import deepcopy
import requests
import time
import yaml
import json
import os
import re

from .utils.exceptions import *
from .utils.config import INTERFACES, INTERFACES_WITH_INDEX, BROWSER_OPTIONS, DEFAULT_TIMEOUT, KEYBOARD
from .utils.functions import required_fields, is_valid_url
from .utils.logger import logging


class SeleniumManagerBase:
    """
    Base class for Selenium management. It initializes the driver, handles configuration,
    and defines basic actions like clicking or filling fields.
    """

    def __init__(self, selenium_config_file: str, headers: dict = None, destruct_on_finish: bool = True, external_functions_mapping: dict = None):
        """
        Initializes the SeleniumManagerBase instance.

        :param selenium_config_file: Path to the configuration file or URL.
        :param headers: Optional headers for web requests.
        """
        self.driver = None
        self.screenshots_dir = ""
        self.env_var_separator_start = "{{"
        self.env_var_separator_end = "}}"
        self.actions_map = {}
        self.headers = headers
        self.actions, self.config, self.environment = self.load_config(selenium_config_file)
        self.destruct_on_finish = self.config.get('destroy', destruct_on_finish) is True
        self.external_functions_mapping = external_functions_mapping
        self.prepare_screenshots_dir()
        if not self.config:
            logging.error("[CONFIG] Config not found")
            raise ConfigFileError("Config not found")
        self._driver_setup()
        if not self.driver:
            logging.error("[CONFIG] Browser not found")
            raise BrowserError("Browser not found")

    def run_actions(self):
        """
        Starts the automated browser actions based on the loaded configuration.
        """
        if not self._is_driver_alive():
            self._driver_setup()
        logging.info(f"[START] Actions to do: {len(self.actions)}")
        _actions_done = 0
        try:
            for _action in self.actions:
                _result = self._execute_action(_action)
                yield dict(action=_action, result=_result)
                _actions_done += 1
        except Exception:
            logging.info(f"[END] Actions done: {_actions_done}/{len(self.actions)}")
            raise
        finally:
            if self.destruct_on_finish:
                self.driver.close()
                self.driver.quit()
            logging.info(f"[END] Actions done: {len(self.actions)}")

    def prepare_screenshots_dir(self):
        self.screenshots_dir = self.config.get('screenshots')
        if self.screenshots_dir and not os.path.isdir(self.screenshots_dir):
            os.mkdir(self.screenshots_dir)

    def prepare_action(self, action: dict):
        return {self._get_env(_key): self._get_env(_value) for _key, _value in action.items()}

    def load_config(self, selenium_config_file: str) -> tuple:
        """
        Loads the configuration from a file or URL.

        :param selenium_config_file: Path to the configuration file or URL.
        :return: Tuple containing actions and configuration dictionary.
        """
        if is_valid_url(selenium_config_file):
            return self._load_url_config(selenium_config_file)

        if not os.path.isfile(selenium_config_file):
            logging.error(f"[CONFIG] File not found {selenium_config_file}")
            raise FileNotFoundError(f"File not found {selenium_config_file}")

        with open(selenium_config_file, 'r') as config:
            try:
                _data = yaml.safe_load(config)
                return _data.get('start', []), _data.get('config', {}), _data.get('environment', {})
            except Exception as e:
                logging.error(f"[CONFIG] Error loading config: {str(e)}")
                raise ConfigFormatError(f"Error loading config: {str(e)}")

    def _replace_env(self, search_value):
        pattern = r"\{\{\s*(\w+)\s*\}\}"

        def replace_local_env(match):
            word = match.group(1)
            return self.environment.get(word, self.env_var_separator_start + word + self.env_var_separator_end)

        def replace_system_env(match):
            word = match.group(1)
            return os.getenv(word, self.env_var_separator_start + word + self.env_var_separator_end)

        result_with_local_replacement = re.sub(pattern, replace_local_env, search_value)
        return re.sub(pattern, replace_system_env, result_with_local_replacement)

    def _get_env(self, value):
        if isinstance(value, dict):
            return {self._get_env(key): self._get_env(value) for key, value in value.items()}
        if isinstance(value, list):
            return [self._get_env(element) for element in value]
        if isinstance(value, tuple):
            return (self._get_env(element) for element in value)
        if isinstance(value, str):
            return self._replace_env(value)
        return value

    def _driver_setup(self):
        """
        Sets up the browser driver based on the configuration settings.
        """
        if self.config.get('browser') not in BROWSER_OPTIONS:
            raise BrowserError("Browser not supported")

        _browser_options = BROWSER_OPTIONS.get(self.config.get('browser', {}))
        _webdriver = _browser_options.get('webdriver')
        _options = _browser_options.get('options')
        _exec_path = _browser_options.get('exec_path')
        _capabilities = _browser_options.get('capabilities')
        _remote = self.config.get('remote')

        if not _webdriver:
            raise BrowserError(f"Web Driver not found (allowed: {', '.join(BROWSER_OPTIONS.keys())})")

        _browser_opt = _options()

        if self.config.get("hidden"):
            _browser_opt.add_argument("--headless")
        if _exec_path and os.path.isfile(_exec_path):
            _browser_opt.binary_location = _exec_path
        if _proxy := _browser_options.get('proxy', {}):
            _profile = None
            if _webdriver == webdriver.Firefox:
                if service_path := _browser_options.get("service_path"):
                    os.popen(service_path)
                _profile = webdriver.FirefoxProfile()
                _profile.set_preference("places.history.enabled", False)
                _profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
                _profile.set_preference("privacy.clearOnShutdown.passwords", True)
                _profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
                _profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
                _profile.set_preference("signon.rememberSignons", False)
                _profile.set_preference("network.cookie.lifetimePolicy", 2)
                _profile.set_preference("network.dns.disablePrefetch", True)
                _profile.set_preference("network.http.sendRefererHeader", 0)
                _profile.set_preference('network.proxy.type', _proxy.get("type"))
                _profile.set_preference('network.proxy.socks', _proxy.get("socks"))
                _profile.set_preference('network.proxy.socks_port', _proxy.get("port"))
                _profile.set_preference("network.proxy.socks_version", 5)
                _profile.set_preference("network.proxy.socks_remote_dns", True)
                _profile.set_preference("javascript.enabled", False)
                _profile.set_preference("permissions.default.image", 2)
                _profile.update_preferences()
                self.driver = _webdriver(firefox_profile=_profile, options=_browser_opt)
            else:
                self.driver = _webdriver(options=_browser_opt)
        else:
            self.driver = _webdriver(options=_browser_opt)
        logging.info(f"[DRIVER] {'Remote ' if _remote else ''}Started")

    def _execute_action(self, action: dict):
        """
        Executes a single action.

        :param action: Action dictionary.
        """
        action = self.prepare_action(action)
        _action_name = action.get('action')
        if _action_name not in self.actions_map:
            raise ActionError(f"'{_action_name}' action not supported")
        try:
            return self.actions_map.get(_action_name)(action)
        except Exception:
            if action.get('optional', False):
                logging.info(f"[{_action_name.upper()}] Optional action could not be runned... Ignoring")
            else:
                raise

    def _execute_js(self, *args, **kwargs):
        """
        Executes a JavaScript script in the context of the current session.

        :param args: Script and its arguments.
        :param kwargs: Optional keyword arguments for script execution.
        """
        self.driver.execute_script(*args, **kwargs)

    def _get_elements(self, interface: str, query: str, timeout: int = DEFAULT_TIMEOUT):
        """
        Retrieves web elements based on the specified search criteria.

        :param interface: Type of search (e.g., by ID, class, etc.).
        :param query: Search query or locator.
        :param timeout: Maximum time to wait for elements to appear.
        :return: Web elements.
        """
        _search = 'presence_of_element_located' \
            if interface not in [INTERFACES.get(_c) for _c in INTERFACES_WITH_INDEX] \
            else 'presence_of_all_elements_located'
        if interface.lower() == "string":
            query = f"//*[contains(text(), '{query}')]"
        return WebDriverWait(self.driver, timeout).until(
            getattr(_ec, _search)((interface, query))
        )

    def _wait(self, interface: str, query: str, index: int = None, timeout: int = DEFAULT_TIMEOUT):
        """
        Waits for web elements to become available.

        :param interface: Type of search (e.g., by ID, class, etc.).
        :param query: Search query or locator.
        :param index: Index of the element to wait for (if expecting a list).
        :param timeout: Maximum time to wait for elements.
        :return: Single web element or list of web elements.
        """
        _interface = self._is_valid_interface(interface)
        _elements = self._get_elements(_interface, query, timeout)
        if isinstance(_elements, list):
            if not index:
                index = 1
            if len(_elements) > index - 1:
                return _elements[index - 1]
            return _elements[0]
        return _elements

    def _loop_file(self, action: dict):
        """
        Process a local file specified in the action dictionary. This method checks the file's existence and format,
        reads its JSON content, and initiates appropriate actions based on its content.

        :param action: Dictionary containing details about the action to be performed.
                       It must include a 'source' key with the path to the file.
        :raises FileNotFoundError: If the file specified in the action's 'source' does not exist.
        :raises ValueError: If the file provided is not in JSON format.
        """
        action = self.prepare_action(action)
        _do_source = action.get('source')
        _raw = action.get('raw')
        try:
            _raw = eval(_raw)
        except:
            pass
        if not _raw and not os.path.isfile(_do_source):
            raise FileNotFoundError(f"File not found {_do_source}")
        if not _raw and not _do_source.endswith('.json'):
            raise ValueError(f"File format not found. Should be JSON format. ({_do_source})")
        if _raw:
            _file_values = _raw
        else:
            _file_values = json.load(open(_do_source, 'r', encoding='utf-8'))
        self._do_file_actions(action, _file_values)

    def _loop_web_file(self, action: dict):
        """
        Retrieve and process a file from the web specified in the action dictionary. This method attempts to download the
        file, expecting a JSON response, and initiates appropriate actions based on its content.

        :param action: Dictionary containing details about the action to be performed.
                       It must include a 'source' key with the URL to the file.
        :raises requests.RequestException: If there is a network problem, like a DNS failure, refused connection, etc.
        :raises ValueError: If the response from the 'source' does not contain valid JSON.
        """
        try:
            action = self.prepare_action(action)
            response = requests.get(action.get('source'))
            if response.ok or response.is_redirect:
                try:
                    self._do_file_actions(action, response.json())
                except ValueError as e:
                    logging.error("[LOOP] The response of the source does not contain JSON type data")
        except requests.RequestException as e:
            logging.error(f"[LOOP] Something went wrong retrieving data from {action.get('source')}: {str(e)}")
        except Exception as e:
            logging.error(f"[LOOP] Something went wrong: {str(e)}")

    def _do_file_actions(self, action: dict, file_data: dict):
        """
        Execute the commands specified in the 'do' section of the action dictionary, applying them to the provided file_data.

        :param action: Dictionary containing details about the actions to be performed.
        :param file_data: Dictionary parsed from a JSON file, containing data the actions will be applied to.
        """
        action = self.prepare_action(action)
        for _file_action in file_data:
            for _action in deepcopy(action.get('do', [])):
                for _action_key, _action_value in _action.items():
                    if isinstance(_action_value, str) and _action_value.startswith('do__'):
                        _key = _action_value.removeprefix('do__')
                        if _get_value := _file_action.get(_key):
                            _action[_action_key] = _get_value
                self._execute_action(_action)

    def send_keys_to_element(self, element, keys: list):
        """
        Helper method to send keys to the element. If no element is specified, it sends keys to the body or active element.

        :param element: The web element to send keys to, could be None for sending keys to the active element.
        :param keys: The key action to send.
        """
        if element:
            element.send_keys(*keys)
        else:
            try:
                active_element = self.driver.switch_to.active_element
                active_element.send_keys(*keys)
            except WebDriverException as e:
                logging.error(f"[KEYBOARD] An error occurred while sending keys to the active element: {str(e)}")
                raise

    def _is_driver_alive(self):
        try:
            _ = self.driver.title
            logging.info("[DRIVER] Connected")
            return True
        except WebDriverException as e:
            logging.info(f"[DRIVER] Disconnected (Error: {str(e)})")
            return False

    @staticmethod
    def _log_action(action: dict, log: str):
        _action = action.get('action').upper()
        if _comment := action.get('comment'):
            logging.info(f"[{_action}] {_comment}")
        logging.info(f"[{_action}] {log}")
    
    @staticmethod
    def _load_url_config(selenium_config_file_url: str) -> tuple:
        """
        Loads the configuration from a URL.

        :param selenium_config_file_url: The URL pointing to the YAML configuration file.
        :return: Tuple containing actions and configuration dictionary.
        """
        try:
            response = requests.get(selenium_config_file_url)
            if response.ok:
                try:
                    _data = yaml.safe_load(response.text)
                    return _data.get('start', []), _data.get('config', {})
                except yaml.YAMLError as e:
                    logging.error(f"[CONFIG] Error reading YAML config file {selenium_config_file_url}: {str(e)}")
                    raise ConfigFormatError(f"Error reading YAML config file {selenium_config_file_url}: {str(e)}")
            else:
                logging.error(f"[CONFIG] Error getting YAML config file {selenium_config_file_url}: Status Code {response.status_code}")
                raise ConfigFileError(f"Error getting YAML config file {selenium_config_file_url}: Status Code {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"[CONFIG] Error getting YAML config file {selenium_config_file_url}: {str(e)}")
            raise ConfigFileError(f"Error getting YAML config file {selenium_config_file_url}: {str(e)}")
        except Exception as e:
            logging.error(f"[CONFIG] Something went wrong retrieving YAML config file {selenium_config_file_url}: {str(e)}")
            raise ConfigFileError(f"Something went wrong retrieving YAML config file {selenium_config_file_url}: {str(e)}")

    @staticmethod
    def _parse_action(action: dict):
        """
        Parses an action dictionary and extracts relevant information.

        :param action: Action dictionary.
        :return: Tuple with extracted information.
        """
        _interface = action.get('interface')
        _query = action.get('query').replace('\n', '').strip()
        _timeout = action.get('timeout', DEFAULT_TIMEOUT)
        _index = action.get('index')
        if _index and _index < 1:
            _index = 1
        _content = action.get('content')
        _log = f"@body"
        if _interface and _query:
            _log = f"@{_interface}[query={_query}]{'' if not _index else '[' + str(_index) + ']'}"
        return _interface, _query, _timeout, _index, _content, _log

    @staticmethod
    def _is_valid_interface(interface: str):
        if interface not in INTERFACES:
            raise InterfaceError("Interface not supported")
        return INTERFACES.get(interface)

    @staticmethod
    def _process_keys(keys_list: list) -> list:
        """
        Process a key, fetch from the KEYBOARD configuration if it's a special key.

        :param keys_list: The key to process.
        :return: Returns the key or raises ValueError if the key is not in the configuration.
        """
        keys_res = []
        for key in keys_list:
            _processed_key = KEYBOARD.get(key.lower())
            if _processed_key is None and len(key) == 1:
                _processed_key = key
            elif _processed_key is None:
                raise ValueError(f"Special key '{key}' not found in KEYBOARD configuration.")
            keys_res.append(_processed_key)
        return keys_res


class SeleniumManager(SeleniumManagerBase):
    """
    Manages advanced Selenium actions such as navigation, clicks, input filling, screenshots, scrolling,
    and more, extending the base functionality provided by SeleniumManagerBase.

    :param selenium_config_file: Path to the Selenium configuration file.
    :param headers: Optional dictionary of headers to be used in the web requests.
    """

    def __init__(self, selenium_config_file: str, headers: dict = None,
                 destruct_on_finish: bool = True, external_functions_mapping: dict = None):
        """
        Initializes the SeleniumManager with a specific configuration file and optional headers.

        :param selenium_config_file: Path to the Selenium configuration file.
        :param headers: Optional dictionary of headers for web requests.
        """
        super().__init__(selenium_config_file, headers, destruct_on_finish, external_functions_mapping)
        self.actions_map = {
            'navigate': self._navigate,
            'click': self._click,
            'fill': self._fill,
            'screenshot': self._screenshot,
            'scroll': self._scroll,
            'sleep': self._sleep,
            'loop': self._loop,
            'keyboard': self._keyboard,
            'execute': self._execute_js_action,
            'wait': self._wait_exists,
            'submit': self._submit,
            'external': self._external_function,
            'attach': self._external_function,
            'drag_drop': self._drag_drop,
            'request': self._request
        }

    @required_fields(['do'])
    def _loop(self, action: dict):
        """
        Executes actions in a loop, which can be based on a fixed number of times or iteratively over
        content from a web source.

        :param action: Dictionary specifying the details of the loop action.
        :raises LoopError: If neither 'times' nor 'source' is specified in the action.
        """
        if not any(action.get(_mode) for _mode in ['times', 'source']):
            raise LoopError("Times or source have to be defined in 'loop' action")
        if _do_times := action.get('times'):
            for _ in range(int(action.get('times'))):
                for _action in action.get('do', []):
                    self._execute_action(_action)
            return
        if is_valid_url(action.get('source')):
            return self._loop_web_file(action)
        return self._loop_file(action)

    @required_fields(['interface', 'query'])
    def _wait_exists(self, action: dict):
        """
        Performs a click action on a web element identified by a specific interface and query.

        :param action: Dictionary containing parameters for the click action, including 'interface' and 'query'.
        """
        _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
        self._log_action(action, _log)
        self._wait(_interface, _query, _index, _timeout)

    @required_fields(['interface', 'query'])
    def _click(self, action: dict):
        """
        Performs a click action on a web element identified by a specific interface and query.

        :param action: Dictionary containing parameters for the click action, including 'interface' and 'query'.
        """
        _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
        self._log_action(action, _log)
        _element = self._wait(_interface, _query, _index, _timeout)
        _element.click()

    @required_fields(['interface', 'query', 'content'])
    def _fill(self, action: dict):
        """
        Finds a web element and fills it with content. Requires the web element's interface, query, and the content to fill.

        :param action: Dictionary containing parameters for the fill action.
        """
        _interface, _query, _timeout, _index, _content, _log = self._parse_action(action)
        _field = self._wait(_interface, _query, _index, _timeout)
        self._log_action(action, _log)
        _field.send_keys(_content)

    @required_fields(['interface', 'query', 'file_path'])
    def _attach_file(self, action: dict):
        """
        Finds a web element and fills it with content. Requires the web element's interface, query, and the content to fill.

        :param action: Dictionary containing parameters for the fill action.
        """
        _file_path = action.get('file_path')
        if not _file_path:
            raise AttachError("Attach file needs a file path")
        _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
        _field = self._wait(_interface, _query, _index, _timeout)
        self._log_action(action, _log)
        _field.send_keys(action.get('file_path'))

    @required_fields(['url'])
    def _navigate(self, action: dict):
        """
        Navigates the browser to a specified URL.

        :param action: Dictionary containing the URL for navigation.
        """
        _url = action.get('url')
        if not _url.startswith("https://") and not _url.startswith("http://"):
            raise NavigateError(f"{_url} needs to be http/s format")
        self._log_action(action, _url)
        self.driver.get(_url)

    @required_fields(['time'])
    def _sleep(self, action: dict):
        """
        Pauses the execution for a specified number of seconds.

        :param action: Dictionary containing the number of seconds to sleep.
        """
        self._log_action(action, f"{action.get('time')} seconds")
        time.sleep(int(action.get('time')))

    @required_fields(['file_name'])
    def _screenshot(self, action: dict):
        """
        Takes a screenshot of the current browser window, with optional additional CSS styling.

        :param action: Dictionary specifying the screenshot parameters, including optional CSS styling.
        :raises ScreenshotError: If 'style' is not defined for an element in the 'css' section of the action.
        """
        _file_name = f"{action.get('file_name')}.png"
        _photo_name = os.path.join(self.screenshots_dir, _file_name)
        if _styles := action.get('css'):
            for _element in _styles:
                if not _element.get('style'):
                    raise ScreenshotError("Style not defined in 'screenshot' css defined element")

                _element_instance = self._wait(_element.get('interface'), _element.get('query'))
                self._execute_js("arguments[0].setAttribute('style', arguments[1]);", _element_instance, _element.get('style'))
            time.sleep(.2)
        self._log_action(action, _photo_name)
        self.driver.save_screenshot(_photo_name)

    @required_fields([])
    def _scroll(self, action: dict):
        """
        Scrolls the webpage by a specified amount along the x and y axes.

        :param action: Dictionary containing the 'x' and 'y' scroll values.
        :raises ScrollError: If either 'x' or 'y' is not defined in the action.
        """
        _movement = (action.get('x'), action.get('y'))
        if all([m is None for m in _movement]):
            raise ScrollError("X or Y need to be defined in 'scroll' action")
        if _movement[0] is None:
            _movement = 0, _movement[1]
        if _movement[1] is None:
            _movement = _movement[0], 0
        self._log_action(action, f"{_movement}")
        self._execute_js(f"window.scrollBy{_movement};")

    @required_fields(['drag', 'drop'])
    def _drag_drop(self, action: dict):
        """
        Drag and drop an element in the DOM.

        :param action: Dictionary containing the 'drag' and 'drop' values with interface and query fields.
        """
        _interface_drag, _query_drag, _timeout_drag, _index_drag, _, _log_drag = self._parse_action(action.get('drag'))
        _interface_drop, _query_drop, _timeout_drop, _index_drop, _, _log_drop = self._parse_action(action.get('drop'))
        _drag_element = self._wait(_interface_drag, _query_drag, _index_drag, _timeout_drag)
        _drop_on_element = self._wait(_interface_drop, _query_drop, _index_drop, _timeout_drop)
        self._log_action(action, f"{_log_drag} => {_log_drop}")
        _actions = ActionChains(self.driver)
        _actions.drag_and_drop(_drag_element, _drop_on_element).perform()

    @required_fields(['js'])
    def _execute_js_action(self, action: dict):
        if _js_action := action.get('js'):
            self._log_action(action, f"{_js_action}")
            self._execute_js(_js_action)

    @required_fields(['interface', 'query'])
    def _submit(self, action: dict):
        """
        Submits a form on the webpage based on the provided selector.

        :param action: Dictionary containing parameters for the submit action, including 'interface' and 'query'.
        """
        _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
        self._log_action(action, f"{_log}")
        _form = self._wait(_interface, _query, _index, _timeout)
        _form.submit()

    @required_fields(['keys'])
    def _keyboard(self, action: dict):
        try:
            _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
            _keys = action.get('keys', [])

            if not _keys:
                raise ValueError("The 'keys' field is required for keyboard actions.")

            if (_interface and not _query) or (_query and not _interface):
                raise ValueError(
                    "Both 'interface' and 'query' should be provided together, or neither should be present.")

            self._log_action(action, f"{_log}")

            _element = None
            if _interface and _query:
                _interface = self._is_valid_interface(_interface)
                _element = self._wait(_interface, _query)

            _processed_keys = self._process_keys(_keys)

            action_chain = ActionChains(self.driver)

            if _do_times := action.get('times', 1):
                for _ in range(int(action.get('times', 1))):
                    logging.info(f"[KEYBOARD] {' + '.join([_k.capitalize() for _k in _keys])}")

                    for key in _processed_keys:
                        action_chain.key_down(key)

                    for key in reversed(_processed_keys):
                        action_chain.key_up(key)

                    action_chain.perform()

        except NoSuchElementException as e:
            logging.error(f"[KEYBOARD] Element not found when trying to perform keyboard action: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"[KEYBOARD] An error occurred while performing a keyboard action: {str(e)}")
            raise

    @required_fields(['function'])
    def _external_function(self, action: dict):
        action = self.prepare_action(action)
        _function_mapping_name = action.get('function')
        _function_args = action.get('args', '{}')
        _function_response_variable = action.get('response', [])
        if _mapped_function := self.external_functions_mapping.get(_function_mapping_name):
            _args_data = self.prepare_action(json.loads(_function_args))
            self._log_action(action, f"{_function_mapping_name}({_function_args})")
            _result = _mapped_function(**_args_data)
            if _function_response_variable:
                if ((isinstance(_result, list) or isinstance(_result, tuple))
                        and len(_function_response_variable) != len(_result)):
                    logging.error(f"[EXTERNAL] Function returns {len(_result)} elements and "
                                  f"you only took {len(_function_response_variable)}")
                    return _result
                for _new_var_i, _new_var in enumerate(_function_response_variable):
                    if _new_var.strip() not in self.environment:
                        self.environment[_new_var.strip()] = None
                    if isinstance(_result, list) or isinstance(_result, tuple):
                        self.environment[_new_var.strip()] = _result[_new_var_i]
                    else:
                        self.environment[_new_var.strip()] = _result
            return _result
        logging.warning(f"[EXTERNAL] {_function_mapping_name} not defined in external_functions_mapping variable")

    @required_fields(['method', 'url'])
    def _request(self, action: dict):
        action = self.prepare_action(action)
        _url = action.get('url')
        _method = action.get('method', 'get').lower()
        _body = action.get('body')
        _json = action.get('json')
        _data = action.get('data')
        _headers = action.get('headers')
        _timeout = action.get('timeout', DEFAULT_TIMEOUT)
        assert hasattr(requests, _method), f"Method '{_method}' is not a Request method"
        try:
            self._log_action(action, f"{_method.upper()} {_url}")
            _response = getattr(requests, _method)(_url, body=_body, json=_json,
                                                   data=_data, headers=_headers, timeout=_timeout)
            if _response.status_code >= 400:
                return dict(status=_response.status_code, error=_response.content)
            try:
                return dict(status=_response.status_code, response=_response.json())
            except AttributeError:
                return dict(status=_response.status_code, response=_response.content)
            except Exception as response_error:
                return dict(status=_response.status_code, response=_response.text, error=response_error)
        except Exception as e:
            return dict(status=500, error=str(e))
