from ..base import ProtoClient, T, ProtoPath, Response, Request


def build_request(path: ProtoPath[T], client: ProtoClient) -> Request:
    info = path.__info__
    url = client.build_url(path)
    params = client.config.serializer.to_builtins(path)
    query_params = {}
    path_params = {}
    for k, v in params.items():
        if k in info.path_params:
            path_params[k] = v
        else:
            query_params[k] = v
    headers = (
        {"Content-Type": "application/json; charset=UTF-8"}
        if info.method != "GET"
        else {}
    )
    content = None
    if info.method == "GET":
        params = {k: v for k, v in params.items() if k not in info.path_params}
    else:
        if not info.path_params:
            content = client.config.serializer.to_json(path)
        else:
            content = client.config.serializer.to_json(
                {k: v for k, v in params.items() if k not in info.path_params}
            )
    return Request(
        method=info.method,
        url=url,
        params=params,
        headers=headers,
        content=content,
    )


def build_result(path: ProtoPath[T], response: Response, client: ProtoClient) -> T:
    return client.config.serializer.from_json(response.content, path.__info__.type)


def check_response(response: Response) -> Response:
    if response.status != 200:
        raise Exception("Invalid response")
    return response
