import uuid
from abc import ABC, abstractmethod

from sempy.fabric.exceptions import FabricHTTPException
from requests.adapters import HTTPAdapter, Retry
from requests.sessions import Session
from sempy._utils._log import log_retry, log_rest_response, log_rest_request
from sempy.fabric._token_provider import SynapseTokenProvider, TokenProvider

from sempy.fabric._environment import _get_synapse_endpoint, _get_environment, _get_fabric_rest_endpoint
from typing import Optional


class RetryWithLogging(Retry):
    @log_retry
    def increment(self, *args, **kwargs):
        return super().increment(*args, **kwargs)


class SessionWithLogging(Session):
    @log_rest_request
    def prepare_request(self, *args, **kwargs):
        return super().prepare_request(*args, **kwargs)


class BaseRestClient(ABC):
    """
    REST client to access Fabric and PowerBI endpoints. Authentication tokens are automatically acquired from the execution environment.

    ***Experimental***: This class is experimental and may change in future versions.

    Parameters
    ----------
    token_provider : TokenProvider, default=None
        Implementation of TokenProvider that can provide auth token
        for access to the PowerBI workspace. Will attempt to acquire token
        from its execution environment if not provided.
    """
    def __init__(self, token_provider: Optional[TokenProvider] = None):
        self.http = SessionWithLogging()

        @log_rest_response
        def validate_rest_response(response, *args, **kwargs):
            if response.status_code >= 400:
                raise FabricHTTPException(response)
        self.http.hooks["response"] = [validate_rest_response]
        retry_strategy = RetryWithLogging(
            total=10,
            allowed_methods=["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE"],
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        retry_adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http.mount("https://", retry_adapter)

        self.token_provider = token_provider or SynapseTokenProvider()
        self.base_url = self._get_base_url()

    @abstractmethod
    def _get_base_url(self):
        pass

    def _get_headers(self) -> dict:
        # this could be static / a function
        correlation_id = str(uuid.uuid4())
        return {
            'authorization': f'Bearer {self.token_provider()}',
            'Accept': 'application/json',
            'ActivityId': correlation_id
        }

    def request(self, method: str, path: str, *args, **kwargs):
        """
        Request to the Fabric and PowerBI REST API.

        Parameters
        ----------
        method : str
            HTTP method.
        path : str
            The path to the resource.
        *args : list
            Arguments passed to the request method.
        **kwargs : dict
            Arguments passed to the request method.

        Returns
        -------
        requests.Response
            The response from the REST API.
        """
        headers = self._get_headers()
        headers.update(kwargs.get("headers", {}))

        # overwrite url + headers
        kwargs["url"] = f"{self.base_url}{path}"
        kwargs["headers"] = headers

        return self.http.request(method, *args, **kwargs)

    def get(self, path: str, *args, **kwargs):
        """
        GET request to the Fabric and PowerBI REST API.

        Parameters
        ----------
        path : str
            The relative path to the resource. The base URL is automatically prepended.
        *args : list
            Arguments passed to the request method.
        **kwargs : dict
            Arguments passed to the request method.

        Returns
        -------
        requests.Response
            The response from the REST API.
        """
        return self.request("GET", path, *args, **kwargs)

    def post(self, path: str, *args, **kwargs):
        """
        POST request to the Fabric and PowerBI REST API.

        Parameters
        ----------
        path : str
            The relative path to the resource. The base URL is automatically prepended.
        *args : list
            Arguments passed to the request method.
        **kwargs : dict
            Arguments passed to the request method.

        Returns
        -------
        requests.Response
            The response from the REST API.
        """
        return self.request("POST", path, *args, **kwargs)

    def delete(self, path: str, *args, **kwargs):
        """
        DELETE request to the Fabric and PowerBI REST API.

        Parameters
        ----------
        path : str
            The relative path to the resource. The base URL is automatically prepended.
        *args : list
            Arguments passed to the request method.
        **kwargs : dict
            Arguments passed to the request method.

        Returns
        -------
        requests.Response
            The response from the REST API.
        """
        return self.request("DELETE", path, *args, **kwargs)

    def head(self, path: str, *args, **kwargs):
        """
        HEAD request to the Fabric and PowerBI REST API.

        Parameters
        ----------
        path : str
            The relative path to the resource. The base URL is automatically prepended.
        *args : list
            Arguments passed to the request method.
        **kwargs : dict
            Arguments passed to the request method.

        Returns
        -------
        requests.Response
            The response from the REST API.
        """
        return self.request("HEAD", path, *args, **kwargs)

    def patch(self, path: str, *args, **kwargs):
        """
        PATCH request to the Fabric and PowerBI REST API.

        Parameters
        ----------
        path : str
            The relative path to the resource. The base URL is automatically prepended.
        *args : list
            Arguments passed to the request method.
        **kwargs : dict
            Arguments passed to the request method.

        Returns
        -------
        requests.Response
            The response from the REST API.
        """
        return self.request("PATCH", path, *args, **kwargs)

    def put(self, path: str, *args, **kwargs):
        """
        PUT request to the Fabric and PowerBI REST API.

        Parameters
        ----------
        path : str
            The relative path to the resource. The base URL is automatically prepended.
        *args : list
            Arguments passed to the request method.
        **kwargs : dict
            Arguments passed to the request method.

        Returns
        -------
        requests.Response
            The response from the REST API.
        """
        return self.request("PUT", path, *args, **kwargs)


class FabricRestClient(BaseRestClient):
    """
    REST client to access Fabric REST endpoints. Authentication tokens are automatically acquired from the execution environment.

    ***Experimental***: This class is experimental and may change in future versions.

    Parameters
    ----------
    token_provider : TokenProvider, default=None
        Implementation of TokenProvider that can provide auth token
        for access to the PowerBI workspace. Will attempt to acquire token
        from its execution environment if not provided.
    """
    def __init__(self, token_provider: Optional[TokenProvider] = None):
        super().__init__(token_provider)

    def _get_base_url(self):
        return _get_fabric_rest_endpoint()


class PowerBIRestClient(BaseRestClient):
    """
    REST client to access PowerBI REST endpoints. Authentication tokens are automatically acquired from the execution environment.

    ***Experimental***: This class is experimental and may change in future versions.

    Parameters
    ----------
    token_provider : TokenProvider, default=None
        Implementation of TokenProvider that can provide auth token
        for access to the PowerBI workspace. Will attempt to acquire token
        from its execution environment if not provided.
    """
    def __init__(self, token_provider: Optional[TokenProvider] = None):
        super().__init__(token_provider)

    def _get_base_url(self):
        # The endpoint api.powerbi.com does not work for REST calls using the "pbi" token due to limited audience
        if _get_environment() == "prod":
            headers = self._get_headers()
            return self.http.get("https://api.powerbi.com/powerbi/globalservice/v201606/clusterdetails", headers=headers).json()["clusterUrl"] + "/"
        else:
            return _get_synapse_endpoint()
