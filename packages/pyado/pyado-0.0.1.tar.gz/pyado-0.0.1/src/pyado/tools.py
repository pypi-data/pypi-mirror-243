"""Tools to interact with Azure DevOps."""

def _base64_encode(value: str) -> str:
    """Encode string into a base64 string."""
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')


def get_headers(token):
    """Get authentication header from token."""
    base64_auth = _base64_encode(f':{token}')
    return {'Authorization': f'Basic {base64_auth}'}


def request_with_auth(method: Callable, url: str, access_token: str,
                      **kwargs) -> Any:
    """Helper function to interact with the Azure DevOps API."""
    response = method(url,
                      headers=get_headers(access_token),
                      timeout=10,
                      **kwargs)
    if not response.ok:
        try:
            error_message = response.json()['message']
        except Exception:
            response.raise_for_status()
        raise RuntimeError(error_message)
    response.raise_for_status()
    return response


def post_with_auth(url: str, access_token: str, **kwargs) -> Any:
    """Helper function to interact with the Azure DevOps API via POST."""
    return request_with_auth(requests.post, url, access_token, **kwargs)


def patch_with_auth(url: str, access_token: str, **kwargs) -> Any:
    """Helper function to interact with the Azure DevOps API via PATCH."""
    return request_with_auth(requests.patch, url, access_token, **kwargs)


def get_with_auth(url: str, access_token: str, **kwargs) -> Any:
    """Helper function to interact with the Azure DevOps API via GET."""
    return request_with_auth(requests.get, url, access_token, **kwargs)


def delete_with_auth(url: str, access_token: str, **kwargs) -> Any:
    """Helper function to interact with the Azure DevOps API via GET."""
    return request_with_auth(requests.delete, url, access_token, **kwargs)


def get_active_task_from_timeline(token: str, base_url: str, build_id: int,
                                  timeline_id: str,
                                  task_id_fragment: str) -> Dict[str, Any]:
    """Iterate over the full timeline and match the first active task that
    matches the partial task ID fragment.

    Reference: https://github.com/MicrosoftDocs/vsts-rest-api-specs/blob/master/specification/build/7.1/build.json#L2478
    """
    url = f'{base_url}/build/builds/{build_id}/timeline/{timeline_id}'
    url += '?api-version=7.1-preview.2'
    response = requests.get(url, headers=get_headers(token), timeout=10)
    response.raise_for_status()
    records = response.json()['records']
    for entry in records:
        if entry['state'] == 'completed':
            continue
        if entry['id'].startswith(task_id_fragment):
            return entry
    records = {entry['id'] for entry in records}
    raise Exception(f'No task matching {task_id_fragment!r} found: {records}')
