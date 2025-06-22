
# Antisniper API Wrapper

**Asynchronous Python wrapper for the [Antisniper API](https://api.antisniper.net)**  
Built on top of `aiohttp`.

## ❗️Warning

---
### Below are only the methods currently being updated by Antisniper.

---

# Features

- Fully asynchronous (`async/await`)
- Easy-to-use methods for all main API endpoints
- Built-in error handling and custom exceptions
- Clean structure, ready for extension
- Type hints and docstrings for better development experience

---



## 📦 Installation

```bash
pip install aiohttp
git clone https://github.com/0x0293919592050/antisniper-async-wrapper.git
cd antisniper-api
pip install -e .
```

## 🧠 Basic Usage

```python
import asyncio
from antisniper.api import AntisniperAPI

async def main():
    async with AntisniperAPI("your-api-key") as api:
        data = await api.convert("PlayerName")
        print(data)

asyncio.run(main())
```

---

## 🔧 Available Methods

| Method                                       | Description                      |
| -------------------------------------------- | -------------------------------- |
| `convert(player, collection="mojang")`       | Convert username ⇄ UUID          |
| `bulk_convert(players, collection="mojang")` | Bulk conversion (up to 100)      |
| `mojang_data(uuid)`                          | Get Mojang profile info          |
| `name_owners(name)`                          | Find all UUIDs that owned a name |
| `online_check(players, reason)`              | Check online/offline status      |
| `get_capes()`                                | Get cape texture URLs            |
| `get_user()`                                 | Get API key information          |

---

## ❗ Exceptions

| Exception                          | Raised when...                |
| ---------------------------------- | ----------------------------- |
| `AntisniperForbiddenException`     | API key is invalid or missing |
| `AntisniperRatelimitException`     | You hit the rate limit        |
| `AntisniperUnprocessableException` | Invalid input or request      |
| `AntisniperConnectionException`    | Network or server error       |
| `AntisniperUnknownException`       | Other unexpected responses    |

---

## 📄 License

MIT License

---
