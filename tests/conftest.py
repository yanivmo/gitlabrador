from typing import Final

import pytest
from dynaconf import Dynaconf

DEFAULT_SETTINGS: Final = {
    "gitlab": {"default_group": {"name": "abc", "full_path": "path/to/abc"}},
    "app": {"recent_projects": []},
}


@pytest.fixture
def mocked_settings(mocker):
    settings = Dynaconf()
    settings.update(DEFAULT_SETTINGS, merge=True)
    return settings
