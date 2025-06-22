import aiohttp
from antisniper.exceptions import *

class AntisniperAPI:
    def __init__(self, key: str, baseUrl="https://api.antisniper.net/v2"):
        self.key = key
        self.url = baseUrl
        self.session = aiohttp.ClientSession()
        self.session.headers.add("Apikey", self.key)

    async def get(self, endpoint: str, params: dict = None) -> dict:
        try:
            async with self.session.get(self.url + endpoint, params=params or {}) as r:
                return await self._handle_response(r)
        except aiohttp.ClientError as e:
            raise AntisniperConnectionException from e

    async def post(self, endpoint: str, body: dict = None, headers: dict = None) -> dict:
        try:
            async with self.session.post(self.url + endpoint, json=body or {}, headers=headers) as r:
                return await self._handle_response(r)
        except aiohttp.ClientError as e:
            raise AntisniperConnectionException from e

    async def convert(self, player: str, collection: str = "mojang") -> dict:
        """
        Converts UUID <-> IGN using Antisniper databases.

        Args:
            player (str): Player to be checked.
            collection (str, optional): Collection to use. Available values: "mojang", "hypixel". Default to "mojang".

        Returns:
            dict: Result with player data obtained from the Antisniper API.
        """
        params = {'player': player}
        return await self.get(f"/convert/{collection}", params)

    async def bulk_convert(self, players: list, collection: str = "mojang") -> dict:
        """
        Converts UUID <-> IGN for up to 100 players using Antisniper databases.

        Args:
            players (list): A list of players to be checked.
            collection (str, optional): Collection to use. Available values: "mojang", "hypixel". Default to "mojang".

        Returns:
            dict: Result with data obtained from the Antisniper API.
        """
        if len(players) > 100: raise ValueError("You can only check up to 100 players at a time.")
        data = {
            'players': players
        }
        return await self.post(f"/convert/{collection}", data)

    async def mojang_data(self, uuid: str) -> dict:
        """
        Returns basic data of the supplied Minecraft account including name changes, skin history and more.

        Args:
            uuid (str): UUID of a player to check.

        Returns:
            dict: Result with mojang data obtained from the Antisniper API.
        """
        params = {'uuid': uuid}
        return await self.get("/mojang", params)

    async def name_owners(self, name: str) -> dict:
        """
        Returns all previous owners of the provided name.

        Args:
            name (str): Name of a player to check.

        Returns:
            dict: Result with name owners data obtained from the Antisniper API.
        """
        params = {'name': name}
        return await self.get("/mojang/name", params)

    async def online_check(self, players: list, reason: str):
        """
        Check the online / offline status of up to 100 accounts. Accurate to 10 minutes.
        You have to briefly describe your use case for this endpoint.

        Args:
            players (list): List of players to check.
            reason (str): Your reason for using this endpoint.

        Returns:
            dict: Result with online data obtained from the Antisniper API.
        """
        if len(players) > 100: raise ValueError("You can only check up to 100 players at a time.")
        data = {'players': players}
        headers = {'reason': reason}
        return await self.post("/other/online", data, headers)

    async def get_capes(self):
        """
        Get texture URLs for each cape type.

        Returns:
            dict: Result with capes data obtained from the Antisniper API.
        """
        return await self.get("/capes")

    async def get_user(self):
        """
        Returns all information stored by Antisniper on the current user.

        Returns:
            dict: Result with user data obtained from the Antisniper API
        """


    async def _handle_response(self, r: aiohttp.ClientResponse) -> dict:
        match r.status:
            case 200:
                return await r.json()
            case 403:
                raise AntisniperForbiddenException()
            case 422:
                raise AntisniperUnprocessableException()
            case 429:
                raise AntisniperRatelimitException()
            case _:
                raise AntisniperUnknownException()
