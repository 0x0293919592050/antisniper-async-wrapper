import asyncio
from antisniper.api import AntisniperAPI

API_KEY = "your-api-key-here"

async def main():
    async with AntisniperAPI(API_KEY) as api:
        # Example: Converting IGN -> UUID
        player_data = await api.convert("Notch")
        print("Convert:", player_data)

        # Example: bulk convert
        players = ["MonsterGG", "Seeecret"]
        bulk_data = await api.bulk_convert(players)
        print("Bulk Convert:", bulk_data)

        # Example: get mojang data by UUID
        if "uuid" in player_data:
            mojang_info = await api.mojang_data(player_data["uuid"])
            print("Mojang Data:", mojang_info)

        # Example: check online status for a list of players
        online_status = await api.online_check(players, reason="Testing script usage")
        print("Online Check:", online_status)

        # Example: get data of a current user
        user_info = await api.get_user()
        print("User Info:", user_info)

if __name__ == "__main__":
    asyncio.run(main())