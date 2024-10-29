from dataclasses import dataclass, asdict


@dataclass
class CurrentUser:
    """
    GitLab CurrentUser: https://docs.gitlab.com/ee/api/graphql/reference/#currentuser
    """

    id: str
    username: str
    name: str


@dataclass
class Group:
    """
    GitLab Group: https://docs.gitlab.com/ee/api/graphql/reference/#group
    """

    id: str
    name: str
    full_path: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Project:
    """
    GitLab Project: https://docs.gitlab.com/ee/api/graphql/reference/#project
    """

    id: str
    name: str
    name_with_namespace: str
    description: str
    path: str
    full_path: str
    web_url: str

    def to_dict(self):
        return asdict(self)
