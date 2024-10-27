from typing import Final

import pytest
from dynaconf import Dynaconf

DEFAULT_SETTINGS: Final = {
    "gitlab": {"default_group": {"name": "abc", "full_path": "path/to/abc"}},
    "app": {
        "recent_projects": [],
        "max_recent_projects": 3,
    },
    "override_user_settings": "test-settings-state.deleteme.toml",
}


@pytest.fixture
def mocked_settings(mocker):
    settings = Dynaconf()
    settings.update(DEFAULT_SETTINGS, merge=True)
    return settings
