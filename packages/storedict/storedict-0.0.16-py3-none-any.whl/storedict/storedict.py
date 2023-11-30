import json
from abc import ABC, abstractmethod
from collections.abc import ItemsView, Iterable, KeysView, ValuesView
from typing import Any, Optional, TypeAlias

import requests

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class ProxyError(Exception):
    pass


class BaseStore(ABC):
    is_in_transaction = False

    def transaction(self, lock: bool = False):
        return self.Transaction(self, lock)

    class Transaction:
        def __init__(self, store, lock: bool):
            ...

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    @abstractmethod
    def __getitem__(self, key: str) -> JSON:
        ...

    @abstractmethod
    def __setitem__(self, key: str, value: JSON) -> None:
        ...

    @abstractmethod
    def __delitem__(self, key: str) -> None:
        ...

    @abstractmethod
    def __iter__(self) -> Iterable:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...

    @abstractmethod
    def __contains__(self, key: str) -> bool:
        ...

    @abstractmethod
    def get(self, key: str, default=None) -> JSON:
        ...

    @abstractmethod
    def items(self) -> ItemsView[str, JSON]:
        ...

    @abstractmethod
    def keys(self) -> KeysView[str]:
        ...

    @abstractmethod
    def values(self) -> ValuesView[JSON]:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    def validate_key(self, key: Any) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

    def validate_value(self, value: Any) -> None:
        try:
            json.dumps(value)
        except Exception:
            raise TypeError(
                f"Value must be JSON serializable. Value's type is JSON: TypeAlias = {JSON}."
            )


class DummyStore(BaseStore):
    def __init__(self):
        super().__init__()
        self._data = {}

    def __getitem__(self, key: str) -> JSON:
        self.validate_key(key)
        return self._data[key]

    def __setitem__(self, key: str, value: JSON) -> None:
        self.validate_key(key)
        self.validate_value(value)
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        self.validate_key(key)
        del self._data[key]

    def __iter__(self) -> Iterable:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        self.validate_key(key)
        return key in self._data

    def get(self, key: str, default=None) -> JSON:
        self.validate_key(key)
        return self._data.get(key, default)

    def items(self) -> ItemsView[str, JSON]:
        return self._data.items()

    def keys(self) -> KeysView[str]:
        return self._data.keys()

    def values(self) -> ValuesView[JSON]:
        return self._data.values()

    def clear(self) -> None:
        self._data.clear()


class Store(BaseStore):
    def __init__(self, datastore_proxy_url: str):
        super().__init__()
        self.datastore_proxy_url = datastore_proxy_url
        self.urls = {
            "get-value": self.datastore_proxy_url + "/get-value",
            "set-value": self.datastore_proxy_url + "/set-value",
            "delete-key": self.datastore_proxy_url + "/delete-key",
            "key-exists": self.datastore_proxy_url + "/key-exists",
            "get-data": self.datastore_proxy_url + "/get-data",
            "get-data-size": self.datastore_proxy_url + "/get-data-size",
            "delete-data": self.datastore_proxy_url + "/delete-data",
            "begin-transaction": self.datastore_proxy_url + "/begin-transaction",
            "commit-transaction": self.datastore_proxy_url + "/commit-transaction",
            "rollback-transaction": self.datastore_proxy_url + "/rollback-transaction",
            "lock-table": self.datastore_proxy_url + "/lock-table",
        }

    def __getitem__(self, key: str) -> JSON:
        self.validate_key(key)
        r = requests.post(self.urls["get-value"], json={"key": key})
        if r.status_code == 404:
            raise KeyError()
        if r.status_code != 200:
            raise ProxyError()
        return r.json()["value"]

    def __setitem__(self, key: str, value: JSON) -> None:
        self.validate_key(key)
        self.validate_value(value)
        r = requests.post(self.urls["set-value"], json={"key": key, "value": value})
        if r.status_code != 200:
            raise ProxyError()

    def __delitem__(self, key: str) -> None:
        self.validate_key(key)
        r = requests.post(self.urls["delete-key"], json={"key": key})
        if r.status_code == 404:
            raise KeyError()
        if r.status_code != 200:
            raise ProxyError()

    def __iter__(self) -> Iterable:
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return iter(r.json()["data"])

    def __len__(self) -> int:
        r = requests.post(self.urls["get-data-size"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json()["size"]

    def __contains__(self, key: str) -> bool:
        self.validate_key(key)
        r = requests.post(self.urls["key-exists"], json={"key": key})
        if r.status_code != 200:
            raise ProxyError()
        return r.json()["exists"]

    def get(self, key: str, default=None) -> JSON:
        self.validate_key(key)
        r = requests.post(self.urls["get-value"], json={"key": key})
        if r.status_code == 404:
            return default
        if r.status_code != 200:
            raise ProxyError()
        return r.json()["value"]

    def items(self) -> ItemsView[str, JSON]:
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json()["data"].items()

    def keys(self) -> KeysView[str]:
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json()["data"].keys()

    def values(self) -> ValuesView[JSON]:
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json()["data"].values()

    def clear(self) -> None:
        r = requests.post(self.urls["delete-data"])
        if r.status_code != 200:
            raise ProxyError()

    def _begin_transaction(self) -> None:
        r = requests.post(self.urls["begin-transaction"])
        if r.status_code != 200:
            raise ProxyError()

    def _commit_transaction(self) -> None:
        r = requests.post(self.urls["commit-transaction"])
        if r.status_code != 200:
            raise ProxyError()

    def _rollback_transaction(self) -> None:
        r = requests.post(self.urls["rollback-transaction"])
        if r.status_code != 200:
            raise ProxyError()

    def _lock_table(self) -> None:
        r = requests.post(self.urls["lock-table"])
        if r.status_code != 200:
            raise ProxyError()

    class Transaction:
        def __init__(self, store, lock: bool):
            if store.is_in_transaction:
                raise RuntimeError("Nested transactions are not supported.")
            self.store = store
            self.lock = lock

        def __enter__(self):
            self.store.is_in_transaction = True
            self.store._begin_transaction()
            if self.lock:
                self.store._lock_table()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                self.store._rollback_transaction()
            else:
                self.store._commit_transaction()

            self.store.is_in_transaction = False


def create_store(datastore_proxy_url: Optional[str] = None) -> BaseStore:
    if datastore_proxy_url is None:
        return DummyStore()
    else:
        return Store(datastore_proxy_url)
