# fastapi-request-memoize

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/fastapi-request-memoize/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

In-request memoization decorator for FastAPI using `contextvars`. Caches expensive function calls for the lifecycle of a single HTTP request.

---

## 🚀 Features

- ⚡ **Deduplicate Database Calls**: If multiple dependencies call `get_current_user(token)`, only the first call executes; subsequent calls return the cached user.
- 🧵 **ContextVar Isolation**: Cache is strictly bound to the active async task and cleans up automatically upon request completion.
- 🔄 **Async & Sync Support**: Works with both `async def` and `def`.

---

## 📦 Installation

```bash
pip install fastapi-request-memoize
```

---

## 🛠️ Quickstart

```python
from fastapi import FastAPI, Request
from fastapi_request_memoize import request_memoize, RequestMemoizeMiddleware

app = FastAPI()
app.add_middleware(RequestMemoizeMiddleware)

@request_memoize
async def get_user(user_id: int):
    # Only executes once per request for the same user_id!
    print("Database query executed!")
    return {"id": user_id, "name": "Alice"}
```

---

## ☕ Support My Studies / Buy Me a Coffee

I am an independent developer and student building open-source developer productivity tools. If this memoization decorator eliminated duplicate queries, please consider supporting my studies:

- ☕ **Buy Me a Coffee:** [buymeacoffee.com/kcidi4148](https://buymeacoffee.com/kcidi4148)
- ⭐ **Star this repository** on GitHub!

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
