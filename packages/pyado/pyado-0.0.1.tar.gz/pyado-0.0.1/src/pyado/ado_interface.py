from typing import TypeAlias, Annotated
from pydantic import BaseModel
from pydantic.networks import HttpUrl, UrlConstraints

AccessToken: TypeAlias = str

ADOUrl: TypeAlias = Annotated[
    HttpUrl,
    UrlConstraints(
        max_length=256,
        allowed_schemes={
            'https',
        },
    ),
]


def _encode_as_base64(value: str) -> str:
    """Encode string as base64 string."""
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')


def get_headers(token, kwargs):
    """Get authentication header from token."""
    base64_auth = _encode_as_base64(f':{token}')
    result = {'Authorization': f'Basic {base64_auth}'}
    if 'content_type' in kwargs:
        result['Content-Type'] = kwargs['content_type']
    elif 'data' in kwargs:
        result['Content-Type'] = 'application/octet-stream'
    else:
        result['Content-Type'] = 'application/json'
    return result


class ApiCall(BaseModel):
    access_token: AccessToken
    base_url: ADOUrl
    query_parameters: dict[str, str]

    def build_call(self) -> 'ADOApi':
        new_base_url
        new_query_parameters = query_parameters | self.query_parameters
        return ADOApi(access_token=access_token,
                      base_url=new_base_url,
                      query_parameters=new_query_parameters)

    def build_url(base_url: ADOUrl, *args: str | int, **kwargs: str) -> str:
        """Construct a URL with the given base URL."""
        version = kwargs.pop('version', None)
        if kwargs:
            raise ValueError(f'Invalid keyword arguments: {kwargs}')
        url_parts = [str(arg) for arg in args]
        url = '/'.join([base_url.unicode_string().rstrip('/')] + url_parts)
        if version is None:
            return url
        if '?' in url:
            return f'{url}&api-version={version}'
        return f'{url}?api-version={version}'

    def _request(self) -> Any:
        """Helper function to interact with the Azure DevOps API."""
        headers = get_headers(self.access_token, kwargs)
        kwargs.pop('content_type', None)

        response = requests.request(method,
                                    url=url,
                                    headers=headers,
                                    timeout=10,
                                    **kwargs)
        if not response.ok:
            try:
                response.raise_for_status()
            except Exception as ex:
                try:
                    error_message = response.json()['message']
                except Exception:
                    error_message = f'Invalid error response: {response.content!r}'
                raise RuntimeError(error_message) from ex

        if not response.content:  # Handle b'' return values
            return None
        try:
            return response.json()
        except Exception as ex:
            raise ValueError(
                f'Invalid API response: {response.content!r}') from ex

    def get(self) -> Any:
        return self._request('GET')

    def post(self, json: Any = None, data: Any = None) -> Any:
        return self._request('POST')

    def patch(self, json: Any = None) -> Any:
        return self._request('PATCH')

    def delete(self) -> Any:
        return self._request('DELETE')
