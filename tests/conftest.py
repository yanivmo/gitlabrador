from typing import Final

import pytest
from dynaconf import Dynaconf

from gitlabrador.config import settings

DEFAULT_SETTINGS: Final = {
    "gitlab": {
        "default_group": {"name": "abc", "full_path": "path/to/abc"},
        "token": "test_token",
    },
    "app": {
        "recent_projects": [],
        "max_recent_projects": 3,
    },
    "override_user_settings": "test-settings-state.deleteme.toml",
}


@pytest.fixture
def mocked_settings():
    mock_conf = Dynaconf()
    mock_conf.update(DEFAULT_SETTINGS)
    return mock_conf


@pytest.fixture(autouse=True)
def default_gitlab_config():
    settings.update(
        {
            "gitlab": {
                "default_group": {"name": "abc", "full_path": "path/to/abc"},
                "token": "default_test_token",
            }
        }
    )
