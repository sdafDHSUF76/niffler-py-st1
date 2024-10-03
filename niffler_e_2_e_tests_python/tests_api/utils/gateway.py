from configs import Configs
from tests_api.utils.base_logic_api import BaseLogicApi


class Gateway(BaseLogicApi):
    """Класс, где организована связь с общим базовым url.

    Есть дочерние класс, что используют тот же base_url и вынес этот класс, как родитель для них.
    """
    def __init__(self, base_url: str = Configs.GATEWAY_URL):
        super().__init__(base_url)
