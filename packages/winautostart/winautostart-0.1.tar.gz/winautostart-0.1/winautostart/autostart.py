from winreg import OpenKey
from winreg import QueryValueEx
from winreg import EnumValue
from winreg import SetValueEx
from winreg import DeleteValue
from winreg import HKEY_CURRENT_USER
from winreg import KEY_ALL_ACCESS
from winreg import REG_SZ


class Autostart:
    def __init__(self) -> None:
        self.__sub_key = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    def add(self, name: str, command: str) -> None:
        with OpenKey(
            key=HKEY_CURRENT_USER,
            sub_key=self.__sub_key,
            reserved=0,
            access=KEY_ALL_ACCESS,
        ) as registry_key:
            SetValueEx(registry_key, name, 0, REG_SZ, command)

    def remove(self, name: str) -> None:
        with OpenKey(
            key=HKEY_CURRENT_USER,
            sub_key=self.__sub_key,
            reserved=0,
            access=KEY_ALL_ACCESS,
        ) as registry_key:
            DeleteValue(registry_key, name)

    def update(self, name: str, new_command: str) -> None:
        if self.get_command(name=name) is None:
            raise FileNotFoundError(
                "autostart with name '%s' is not found and cannot be updated" % name
            )

        self.add(name=name, command=new_command)

    def get_command(self, name: str) -> str | None:
        with OpenKey(
            key=HKEY_CURRENT_USER,
            sub_key=self.__sub_key,
            reserved=0,
            access=KEY_ALL_ACCESS,
        ) as registry_key:
            try:
                value, _ = QueryValueEx(registry_key, name)
                return value

            except FileNotFoundError:
                return None

    def list_all(self) -> list:
        with OpenKey(
            key=HKEY_CURRENT_USER,
            sub_key=self.__sub_key,
            reserved=0,
            access=KEY_ALL_ACCESS,
        ) as registry_key:
            values = []

            try:
                index = 0

                while True:
                    value = EnumValue(registry_key, index)
                    values.append(value[0])
                    index += 1

            except OSError:
                pass

            return values
