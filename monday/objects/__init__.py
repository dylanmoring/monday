from monday import MondayClient

from dylan_utils.metaclasses import SelfLogging
from dylan_utils.classproperty import classproperty


class MondayObject(metaclass=SelfLogging):
    client = None
    name = None

    def __init__(self, id, **kwargs):
        self.id = id

    def __repr__(self):
        output = f'Monday{type(self).__name__}'
        if self.id:
            output += f' {self.id}'
        if self.name:
            output += f' - {self.name}'
        return output

    @classmethod
    def authenticate(cls, api_key):
        cls.client = MondayClient(api_key)

    @classmethod
    def process_kwargs(cls, **kwargs):
        processed_kwargs = {}
        for k, v in kwargs.items():
            if v is not None:
                if v is True or v is False:
                    processed_kwargs[k] = str(v).lower()
                else:
                    processed_kwargs[k] = v
        return processed_kwargs


class Workspace(MondayObject):
    @classproperty
    def client(self):
        return super().client.workspaces


class Item(MondayObject):
    @classproperty
    def client(self):
        return super().client.items


class Update(MondayObject):
    @classproperty
    def client(self):
        return super().client.updates


class Tag(MondayObject):
    @classproperty
    def client(self):
        return super().client.tags


class Board(MondayObject):
    @classproperty
    def client(self):
        return super().client.boards


class User(MondayObject):
    @classproperty
    def client(self):
        return super().client.users

    def __init__(self, id, name: str = None, email: str = None, enabled: bool = None, teams: list = None):
        super().__init__(id)
        self.name = name
        self.email = email
        self.enabled = enabled
        self.teams = teams

    @classmethod
    def fetch_users(
            cls,
            ids: list = None,
            kind: str = None,
            newest_first: bool = False,
            limit: int = None,
            emails: list = None,
            page: int = 1,
            name: str = None
    ):
        kwargs = cls.process_kwargs(
            ids=ids,
            kind=kind,
            newest_first=newest_first,
            limit=limit,
            emails=emails,
            page=page,
            name=name
        )
        response = cls.client.fetch_users(**kwargs)
        users = response['data']['users']
        return [cls(**user) for user in users]


class Group(MondayObject):
    @classproperty
    def client(self):
        return super().client.groups


class Notification(MondayObject):
    @classproperty
    def client(self):
        return super().client.notifications
