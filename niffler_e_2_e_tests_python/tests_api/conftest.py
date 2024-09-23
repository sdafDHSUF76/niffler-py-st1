from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


pytest_plugins = ('fixtures.helper_database', 'fixtures.helper_category')
