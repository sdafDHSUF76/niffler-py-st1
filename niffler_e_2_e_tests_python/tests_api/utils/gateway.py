from configs import Configs
from tests_api.utils.base_logic_api import BaseLogicApi


class Gateway(BaseLogicApi):
    def __init__(self, base_url: str = Configs.GATEWAY_URL):
        super().__init__(base_url)
