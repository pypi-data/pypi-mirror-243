# Native Modules
import json
import logging
import pprint
# noinspection StandardLibraryXml
import xml.etree.ElementTree as etxml

# Module Additions
import requests
import urllib3

logger = logging.getLogger("iupy_restconf")

# Private methods class.  Extendable.


class Rest:

    def __init__(self):
        self._config = dict()

    def _delete(self, url, **kwargs):
        """
        Performs an authenticated DELETE against a URL.  If successful, returns a resposne object.

        :param url:
        :param kwargs:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/Rest/_delete")
        _logger.debug("{}".format(url))

        # Try the request as given.
        try:
            response = requests.delete(url, verify=self._config['ssl_verify'],
                                       headers=kwargs.get("headers"),
                                       auth=(self._config['un'], self._config['pw']))

        # Don't raise an exception on connection errors.
        except requests.exceptions.ConnectionError as error_message:
            _logger.error("Connection error to {}: {}".format(self._config['host'], error_message))
            return None

        # Log Response Text to debug with an error state.
        if response.status_code >= 400:
            _logger.debug("Response Text: {}".format(response.text))

        return response

    def _get(self, url, **kwargs):
        """
        Performs an authenticated GET against a URL.  If successful, returns a response object.

        :param url:
        :param kwargs:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/Rest/_get")
        _logger.debug("{}".format(url))

        # Try the request as given.
        try:
            response = requests.get(url, verify=self._config['ssl_verify'],
                                    headers=kwargs.get("headers"),
                                    auth=(self._config['un'], self._config['pw']))

        # Don't raise an exception on connection errors.
        except requests.exceptions.ConnectionError as error_message:
            _logger.error("Connection error to {}: {}".format(self._config['host'], error_message))
            return None

        # Log Response Text to debug with an error state.
        if response.status_code >= 300:
            _logger.debug("Response Text: {}".format(response.text))

        return response

    def _head(self, url, **kwargs):
        """
        Performs an authenticated HEAD against a URL.  If successful, returns a response object.

        :param url:
        :param kwargs:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/Rest/_head")
        _logger.debug("{}".format(url))

        # Try the request as given.
        try:
            response = requests.head(url, verify=self._config['ssl_verify'],
                                     headers=kwargs.get("headers"),
                                     auth=(self._config['un'], self._config['pw']))

        # Don't raise an exception on connection errors.
        except requests.exceptions.ConnectionError as error_message:
            _logger.error("Connection error to {}: {}".format(self._config['host'], error_message))
            return None

        # Log Response Text to debug with an error state.
        if response.status_code >= 300:
            _logger.debug("Response Text: {}".format(response.text))

        return response

    def _patch(self, url, data, **kwargs):
        """
        Performs an authenticated GET against a URL.  If successful, returns a response object.

        :param url:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/Rest/_patch")
        _logger.debug("{}".format(url))

        # Try the request as given.
        try:
            response = requests.patch(url, data, verify=self._config['ssl_verify'],
                                      headers=kwargs.get("headers"),
                                      auth=(self._config['un'], self._config['pw']))

        # Don't raise an exception on connection errors.
        except requests.exceptions.ConnectionError as error_message:
            _logger.error("Connection error to {}: {}".format(self._config['host'], error_message))
            return None

        # Log Response Text to debug with an error state.
        if response.status_code >= 300:
            _logger.debug("Response Text: {}".format(response.text))

        return response

    def _post(self, url, data, **kwargs):
        """
        Performs an authenticated GET against a URL.  If successful, returns a response object.

        :param url:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/Rest/_post")
        _logger.debug("{}".format(url))

        # Try the request as given.
        try:
            response = requests.post(url, data, verify=self._config['ssl_verify'],
                                     headers=kwargs.get("headers"),
                                     auth=(self._config['un'], self._config['pw']))

        # Don't raise an exception on connection errors.
        except requests.exceptions.ConnectionError as error_message:
            _logger.error("Connection error to {}: {}".format(self._config['host'], error_message))
            return False

        # Log Response Text to debug with an error state.
        if response.status_code >= 400:
            _logger.debug("Response Text: {}".format(response.text))

        return response

    def _put(self, url, data, **kwargs):
        """
        Performs an authenticated GET against a URL.  If successful, returns a response object.

        :param url:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/Rest/_put")
        _logger.debug("{}".format(url))

        # Try the request as given.
        try:
            response = requests.put(url, data, verify=self._config['ssl_verify'],
                                    headers=kwargs.get("headers"),
                                    auth=(self._config['un'], self._config['pw']))

        # Don't raise an exception on connection errors.
        except requests.exceptions.ConnectionError as error_message:
            _logger.error("Connection error to {}: {}".format(self._config['host'], error_message))
            return False

        # Log Response Text to debug with an error state.
        if response.status_code >= 400:
            _logger.debug("Response Text: {}".format(response.text))

        return response


# Extensions to class Rest, for RESTCONF purposes.

class RestConf(Rest):

    configReady = True

    def __init__(self):
        """
        Initialize the variables in the RestConf class.
        """
        super().__init__()

        self.netconf_state = dict()
        self.rc_operations = dict()
        self.rc_data_modules = dict()
        self.yang_library = str()

    def delete(self, url):
        """
        Access to the _delete function.

        :param url:
        :param kwargs:
        :return:
        """

        # Add Transport, Host, and RestConf base to a URL.
        new_url = "{}://{}:{}{}/{}".format(self._config['transport'],
                                           self._config['host'],
                                           self._config['port'],
                                           self._config['base'],
                                           url)

        # Get the response
        response = self._delete(new_url,
                                headers={'Accept': 'application/yang-data+json, application/yang-data.errors+json'})

        return response

    def get(self, url):
        """
        Access to the _get function, but building out the whole base URL.

        :param url:
        :return:
        """

        # Add Transport, Host, and RestConf base to a URL.
        new_url = "{}://{}:{}{}/{}".format(self._config['transport'],
                                           self._config['host'],
                                           self._config['port'],
                                           self._config['base'],
                                           url)

        # Get the response.
        response = self._get(new_url,
                             headers={'Accept': 'application/yang-data+json, application/yang-data.errors+json'})

        return response

    def head(self, url):
        """
        Access to the _head function, but building out the whole base URL.

        :param url:
        :return:
        """

        # Add Transport, Host, and RestConf base to a URL.
        new_url = "{}://{}:{}{}/{}".format(self._config['transport'],
                                           self._config['host'],
                                           self._config['port'],
                                           self._config['base'],
                                           url)

        # Get the response.
        response = self._head(new_url,
                              headers={'Accept': 'application/yang-data+json, application/yang-data.errors+json'})

        return response

    def patch(self, url, data):
        # Add Transport, Host, and RestConf base to a URL.
        new_url = "{}://{}:{}{}/{}".format(self._config['transport'],
                                           self._config['host'],
                                           self._config['port'],
                                           self._config['base'],
                                           url)

        # Get the response, import JSON data.
        response = self._patch(new_url,
                               headers={'Accept': 'application/yang-data+json, application/yang-data.errors+json',
                                        'Content-Type': 'application/yang-data+json'},
                               data=json.dumps(data))

        # Return the response
        return response

    def post(self, url, data=None):
        # Add Transport, Host, and RestConf base to a URL.
        new_url = "{}://{}:{}{}/{}".format(self._config['transport'],
                                           self._config['host'],
                                           self._config['port'],
                                           self._config['base'],
                                           url)

        if data is None:
            # POST w/o data
            response = self._post(new_url, data,
                                  headers={'Accept': 'application/yang-data+json, application/yang-data.errors+json',
                                           'Content-Type': 'application/yang-data+json'})
        else:
            # POST w/ data converted to JSON.
            response = self._post(new_url,
                                  headers={'Accept': 'application/yang-data+json, application/yang-data.errors+json',
                                           'Content-Type': 'application/yang-data+json'},
                                  data=json.dumps(data))

        # Return the response
        return response

    def put(self, url, data):
        # Add Transport, Host, and RestConf base to a URL.
        new_url = "{}://{}:{}{}/{}".format(self._config['transport'],
                                           self._config['host'],
                                           self._config['port'],
                                           self._config['base'],
                                           url)

        # Get the response, import JSON data.
        response = self._put(new_url,
                             headers={'Accept': 'application/yang-data+json, application/yang-data.errors+json',
                                      'Content-Type': 'application/yang-data+json'},
                             data=json.dumps(data))

        # Return the response
        return response

    # Method Consumers

    def connect(self, **kwargs):
        """
        This function connects to the target and gets the RESTCONF root.  RFC-8040, section 3.1.

        This expects a default response to be XML encoded.
        """
        _logger = logging.getLogger("iupy_restconf/RestConf/connect")

        self._config = kwargs

        if 'base' not in self._config:
            self._config['base'] = None
        if 'port' not in self._config:
            self._config['port'] = 443

        # Loop through and make sure all the required attributes are present.
        _attributes = ('transport', 'host', 'un', 'pw')
        for i in _attributes:
            if i not in self._config:
                _logger.debug("Key {} not in config.")
                self.configReady = False

        # Disable SSL Verification and warnings by default.
        if "ssl_verify" not in self._config:
            self._config['ssl_verify'] = False
            urllib3.disable_warnings()

        # Config must be ready before we can continue.
        if not self.configReady:
            _logger.error("Config is not ready.")
            return False
        else:
            _logger.debug("Config: {}".format(self._config))

        # Check and see if we have a base specified in the connect.  This is set for devices that don't properly
        # support Meta Context Discovery.

        if self._config['base'] is not None:
            _logger.debug("Base provided as: {}".format(self._config['base']))
        else:
            # RFC6415 - Meta Context Discovery
            connect_url = "{}://{}:{}/.well-known/host-meta".format(self._config['transport'],
                                                                    self._config['host'],
                                                                    self._config['port'])
            response = self._get(connect_url)

            # We must have a response code of 200 in order to find the root.
            if response.status_code == 200:
                rdict = etxml.fromstring(response.text)

                # Cycle through the attributes, looking for both rel and href.  Use the first reported value.
                for child in rdict:
                    if 'rel' in child.attrib and 'href' in child.attrib:
                        if child.attrib['rel'] == 'restconf':
                            self._config['base'] = child.attrib['href']
                            _logger.debug("Restconf Base: {}".format(self._config['base']))
                            break

                # If the base is None, log and return empty handed.
                if self._config['base'] is None:
                    _logger.error("RESTCONF base not found.")
                    return False
            else:
                _logger.error("Status code {} returned.".format(response.status_code))
                return response.text

        return True

    def get_data_modules(self):
        if self.configReady is False or self._config['base'] is None:
            return None

        response = self.get("data/ietf-yang-library:modules-state")

        try:
            self.rc_data_modules = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            logger.debug("Status Code: {} / {}".format(response.status_code,
                                                       response.text.strip()))
            self.rc_data_modules = None

    def get_netconf_state(self):
        if self.configReady is False or self._config['base'] is None:
            return None

        response = self.get("data/netconf-state")

        if response is not False:
            try:
                self.netconf_state = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                logger.debug("Status Code: {} / {}".format(response.status_code,
                                                           response.text.strip()))
                self.netconf_state = None

    def get_operations_resources(self):
        if self.configReady is False or self._config['base'] is None:
            return None

        response = self.get("operations")

        try:
            self.rc_operations = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            logger.debug("Status Code: {} / {}".format(response.status_code,
                                                       response.text.strip()))
            self.rc_operations = None

    def get_yang_date(self):
        """
        This function retrieves and stores the reported YANG Library version information.

        :return:
        """
        if self.configReady is False or self._config['base'] is None:
            return None

        response = self.get("yang-library-version")

        # JSON Load, only if we have an ok response.
        try:
            self.yang_library = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            logger.debug("Status Code: {} / {}".format(response.status_code,
                                                       response.text.strip()))
            self.yang_library = None

    # Checks on loaded resources.

    def check_operations_resources(self, resource):
        """
        Returns the URL, if a given resource is found.

        :param resource:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/RestConf/check_operations_resources")

        if self.rc_operations is None:
            _logger.debug("Resource is None.")
            return False

        if len(self.rc_operations) == 0:
            return False

        for root in self.rc_operations:
            if resource in self.rc_operations[root]:
                _logger.debug("Resource {} found at {}".format(resource, self.rc_operations[root][resource]))
                return self.rc_operations[root][resource]
            else:
                _logger.debug("Resource {} not found".format(resource))
                return False

    def check_data_module(self, module):
        """
        Returns a module dictionary if the information is found.

        :param module:
        :return:
        """
        _logger = logging.getLogger("iupy_restconf/RestConf/check_data_modules")

        if self.rc_data_modules is None:
            _logger.debug("rc_data_modules is None")
            return False

        if len(self.rc_data_modules) == 0:
            return False

        # Need to loop through the modules because there is no direct ID we can use.
        for m in self.rc_data_modules["ietf-yang-library:modules-state"]["module"]:
            if m["name"] == module:
                _logger.debug("Module {} found, returning dictionary: {}".format(module, m))
                return m

        _logger.debug("Module {} not found".format(module))

        return False

    # Diagnostic Prints

    def show_operations_resources(self):
        if self.rc_operations is not None:
            if len(self.rc_operations):
                for root in self.rc_operations:
                    print("{}".format(root))
                    for child in self.rc_operations[root]:
                        print("  {} -> {}".format(child, self.rc_operations[root][child]))
            else:
                print("0 Operations to display.")
        else:
            print("No operations reported")

    def show_data_modules(self):
        if self.rc_data_modules is not None:
            if len(self.rc_data_modules['ietf-yang-library:modules-state']['module']):
                print("{} Data Modules".format(len(self.rc_data_modules['ietf-yang-library:modules-state']['module'])))
                for root in self.rc_data_modules['ietf-yang-library:modules-state']['module']:
                    pprint.pprint(root)
            else:
                print("0 Data Modules to display.")
        else:
            print("No data modules reported.")
