from urllib.parse import urljoin


def get_join_url(*url: str) -> str:
    """Получить соединенные части url."""
    return urljoin(*url)

