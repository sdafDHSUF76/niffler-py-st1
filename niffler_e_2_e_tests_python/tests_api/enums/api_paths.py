from enum import Enum


class PathUrl(Enum):
    add_category = '/api/categories/add'
    add_spend = '/api/spends/add'
    register = '/register'
    oauth2_authorization = '/oauth2/authorize'
    oauth2_token = '/oauth2/token'
    authorization = '/authorized'
    login = '/login'
