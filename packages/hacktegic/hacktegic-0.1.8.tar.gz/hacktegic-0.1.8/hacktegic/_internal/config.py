import os

import aiofiles
import platformdirs
import tomlkit


class ConfigManager:
    def __init__(self) -> None:
        self.__config_path = (
            platformdirs.user_config_dir("hacktegic", ensure_exists=True)
            + "/config.toml"
        )
        self.__default_config = {
            "api_base_url": "https://cloud.hacktegic.com/",
            "oauth_client_id": "9a8cc86f-18d7-4767-97bf-66577c653356",
        }
        self.config = {}

    async def load(self) -> None:
        """
        Load the config.
        """
        if os.path.exists(self.__config_path):
            async with aiofiles.open(self.__config_path, mode="r") as f:
                doc = tomlkit.loads(await f.read())
                self.config = doc["hacktegic"]

        for k, v in self.__default_config.items():
            if k not in self.config:
                self.config[k] = v

    async def save(self) -> None:
        """
        Save the config to file.
        """
        async with aiofiles.open(self.__config_path, mode="w") as f:
            await f.write(tomlkit.dumps({"hacktegic": self.config}))
