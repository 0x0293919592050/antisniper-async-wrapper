import aiohttp
from antisniper.exceptions import *

class AntisniperAPI:
    def __init__(self, key: str, baseUrl="https://api.antisniper.net/v2"):
        self.key = key
        self.url = baseUrl
        self.session = aiohttp.ClientSession()
        self.session.headers.add("Apikey", self.key)
        self.player = Player(self)
        self.user = User(self)

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def get(self, endpoint: str, params: dict = None) -> dict:
        try:
            async with self.session.get(self.url + endpoint, params=params or {}) as r:
                return await self._handle_response(r)
        except aiohttp.ClientError as e:
            raise AntisniperConnectionException from e

    async def post(self, endpoint: str, body: dict = None, headers: dict = None) -> dict:
        try:
            headers = {**self.session.headers, **(headers or {})}
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
            players (list): A list of players to check.
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

    async def online_check(self, players: list, reason: str) -> dict:
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

    async def get_capes(self) -> dict:
        """
        Get texture URLs for each cape type.

        Returns:
            dict: Result with capes data obtained from the Antisniper API.
        """
        return await self.get("/capes")

    async def get_blacklist(self, player: str, token: str = None) -> dict:
        """
        Checks if a player is considered a Hacker or Sniper.
        Args:
            player (str): Player to check.
            token (str, optional): Blacklist token to be used.
        Returns:
            dict: Result with blacklist data obtained from the Antisniper API.
        """
        params = {'player': player}
        if token: params['token'] = token
        return await self.get("/blacklist", params)

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

class Player:
    """A class with all /player endpoints."""
    def __init__(self, api: AntisniperAPI, endpoint="/player"):
        self.api = api
        self.endpoint = endpoint

    async def get_ping(self, player: str, legacy: bool = False, lookback: int = None) -> dict:
        """
        Returns ping data for a provided player.
        **WARNING**: This endpoint is premium-only.
        Args:
            player (str): Player to check.
            legacy (bool): Whether to use the slower legacy ping data collection.
            lookback (int): How many seconds to search back for player ping from the current time (legacy only).
        Returns:
            dict: Result with ping data obtained from the Antisniper API.
        """
        params = {
            'player': player,
            'legacy': legacy,
            'lookback': lookback
        }
        return await self.api.get(self.endpoint + "/ping", params)

    async def quickshop(self, player: str) -> dict:
        """
        Returns quickshop of the provided player and a list of up to 1000 other
        players with the same quickshop layout on Hypixel.
        **WARNING**: This endpoint is premium-only.
        Args:
            player (str): Player to be checked.
        Returns:
            dict: Result with quickshop data obtained from the Antisniper API.
        """
        params = {'player': player}
        return await self.api.get(self.endpoint + "/quickshop", params)

    async def chat_history(self, player: str, limit: int = None) -> dict:
        """
        Returns Hypixel chat history of the provided player.
        **WARNING**: This endpoint is premium-only.
        Args:
            player (str): Player to be checked.
            limit (int, optional): Limit to be used. (A negative limit will return data from newest).
        Returns:
            dict: Result with chat history data obtained from the Antisniper API.
        """
        params: dict = {'player': player}
        if limit: params['limit'] = limit
        return await self.api.get(self.endpoint + "/chat", params)

class User:
    """A class with all /user endpoints."""
    def __init__(self, api: AntisniperAPI, endpoint="/user"):
        self.api = api
        self.endpoint = endpoint

    async def get(self) -> dict:
        """
        Get all information that Antisniper has stored for the current user

        Returns:
            dict: Result with user data obtained from the Antisniper API.
        """
        return await self.api.get(self.endpoint)

    async def get_requests(self) -> dict:
        """
        Get all requests to the API in the last hour.

        Returns:
            dict: Result with requests data obtained from the Antisniper API.
        """
        return await self.api.get(self.endpoint + "/requests")

    async def get_old_requests(self) -> dict:
        """
        Get up to 1000 of the user's most recent requests to the API.

        Returns:
            dict: Result with requests data obtained from the Antisniper API.
        """
        return await self.api.get(self.endpoint + "/requests/old")

    async def get_products(self) -> dict:
        """
        Get active and expired products purchased by the user.

        Returns:
            dict: Result with products data obtained from the Antisniper API.
        """
        return await self.api.get(self.endpoint + "/products")

    async def get_usage(self) -> dict:
        """
        Get the number of requests every hour that the user has ever requested the API.

        Returns:
            dict: Result with usage data obtained from the Antisniper API.
        """
        return await self.api.get(self.endpoint + "/usage")

    async def get_endpoint_usage(self) -> dict:
        """
        Get the number of requests to each path in the API.

        Returns:
            dict: Result with endpoint usage data obtained from the Antisniper API.
        """
        return await self.api.get(self.endpoint + "/usage/paths")