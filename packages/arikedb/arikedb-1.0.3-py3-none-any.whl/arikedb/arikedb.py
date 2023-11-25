import json
import random
import time
import socket
from json.decoder import JSONDecodeError
from queue import Queue, Empty
from threading import Thread
from typing import Optional, List, Union

from .tag_type import TagType
from .exceptions import ArikedbError
from .event import Event

START_MSG = "_!1@#2$%3^&4*_"
END_MSG = "*_4&^3%$2#@1!_"
SLEN = len(START_MSG)
ELEN = len(END_MSG)


class ArikedbClient:

    def __init__(self, host: str = "localhost", port: int = 6923):
        """RTDB Client constructor"""
        self._host = host
        self._port = port
        self._socket: Optional[socket.socket] = None
        self._recv_th = None
        self._resp_data = Queue()

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._recv_th = Thread(target=self._read_response_batch, daemon=True)
        self._recv_th.start()

    def add_collection(self, collection_name: str):
        cmd = {"ac": "add_coll", "cl": collection_name}
        resp = self.exec_command(cmd)
        status = resp.get("st")
        msg = resp.get("mg")
        if status != 0:
            raise ArikedbError(f"Status: {status}. {msg}")

    def remove_collection(self, collection_name: str):
        cmd = {"ac": "rm_coll", "cl": collection_name}
        resp = self.exec_command(cmd)
        status = resp.get("st")
        msg = resp.get("mg")
        if status != 0:
            raise ArikedbError(f"Status: {status}. {msg}")

    def list_collections(self) -> List[str]:
        cmd = {"ac": "list_coll"}
        resp = self.exec_command(cmd)
        status = resp.get("st")
        msg = resp.get("mg")
        if status != 0:
            raise ArikedbError(f"Status: {status}. {msg}")
        return sorted(resp["cl"])

    def set(self, collection: str, tag_names: List[str],
            tag_types: List[TagType],
            tag_values: List[Union[int, float, bool, str]],
            timestamps_ns: Optional[List[int]] = None):
        cmd = {"ac": "set", "t": []}
        if timestamps_ns:
            for tn, tt, tv, ts in zip(tag_names, tag_types, tag_values,
                                      timestamps_ns):
                cmd["t"].append({"tn": tn, "ts": ts, tt.value: tv})
        else:
            for tn, tt, tv in zip(tag_names, tag_types, tag_values):
                cmd["t"].append({"tn": tn, tt.value: tv})
        resp = self.exec_command(cmd, collection)
        status = resp.get("st")
        msg = resp.get("mg")
        if status != 0:
            raise ArikedbError(f"Status: {status}. {msg}")

    def get(self, collection: str, tag_names: List[str]) -> List[tuple]:
        cmd = {"ac": "get", "t": []}
        for tn in tag_names:
            cmd["t"].append({"tn": tn})
        resp = self.exec_command(cmd, collection)
        status = resp.get("st")
        msg = resp.get("mg")
        if status != 0:
            raise ArikedbError(f"Status: {status}. {msg}")
        return [tuple(rt.values()) for rt in resp["t"]]

    def rm(self, collection: str, tag_names: List[str]):
        cmd = {"ac": "rm", "t": []}
        for tn in tag_names:
            cmd["t"].append({"tn": tn})
        resp = self.exec_command(cmd, collection)
        status = resp.get("st")
        msg = resp.get("mg")
        if status != 0:
            raise ArikedbError(f"Status: {status}. {msg}")

    def list(self, collection: str, per_type: bool = True) -> Union[list, dict]:
        if not per_type:
            tags = []
            for tags_ in self.list(collection, True).values():
                tags += tags_
            return sorted(tags)
        cmd = {"ac": "list"}
        resp = self.exec_command(cmd, collection)
        status = resp.get("st")
        msg = resp.get("mg")
        if status != 0:
            raise ArikedbError(f"Status: {status}. {msg}")

        return {
            TagType.INT: sorted(resp["tl"]["int"]),
            TagType.FLOAT: sorted(resp["tl"]["float"]),
            TagType.BOOL: sorted(resp["tl"]["bool"]),
            TagType.STR: sorted(resp["tl"]["str"]),
        }

    def subscribe(self, collection: str, tag_names: List[str], event: Event):
        uid = time.time_ns() + random.randint(-1000_000, 1000_000)
        cmd = {"ac": "sub", "t": [{"tn": tn} for tn in tag_names],
               "id": uid, "ev": event.value}
        batch = {"commands": [cmd], "collection": collection}

        self._send_command_batch(batch)

        while True:
            try:
                resp = self._resp_data.get(timeout=5)
            except Empty:
                continue
            if resp["id"] == uid:
                if resp["mg"] == "Subscribed":
                    continue
                if resp["st"] != 0:
                    raise ArikedbError(f"Status: {resp['st']}. {resp['mg']}")
                for tag in resp["t"]:
                    yield tuple(tag.values())
            elif resp["id"] == -1:
                raise ArikedbError(f"Status: {resp['st']}. {resp['mg']}")
            else:
                self._resp_data.put(resp)

    def exec_command_batch(self, commands: List[dict],
                           collection: Optional[str] = None,
                           timeout: Optional[float] = None) -> List[dict]:
        batch = {"commands": commands}
        if collection:
            batch.update(collection=collection)

        t0 = time.time_ns() + random.randint(-1000_000, 1000_000)
        uids = [t0 + i for i in range(len(commands))]

        for cmd, uid in zip(commands, uids):
            cmd["id"] = uid

        self._send_command_batch(batch)
        responses = []
        t0 = time.time()
        while True:
            try:
                to = None
                if timeout is not None:
                    elapsed = time.time() - t0
                    to = timeout - elapsed
                    if to < 0:
                        to = 0
                resp = self._resp_data.get(timeout=to)
            except Empty:
                break
            if resp["id"] in uids:
                responses.append(resp)
                uids.remove(resp["id"])
                if not uids:
                    break
            elif resp["id"] == -1:
                return [resp]
            else:
                self._resp_data.put(resp)

        assert len(responses) == len(commands)
        return responses

    def exec_command(self, command: dict, collection: Optional[str] = None,
                     timeout: Optional[float] = None) -> dict:
        return self.exec_command_batch([command], collection, timeout)[0]

    def _send_command_batch(self, cmd_batch: dict):
        self._socket.sendall(f"{START_MSG}{json.dumps(cmd_batch)}"
                             f"{END_MSG}".encode())

    def _read_response_batch(self):
        stream = ""
        while True:
            try:
                data = self._socket.recv(8192)
            except socket.error:
                continue
            if len(data) == 0:
                break
            stream += data.decode()
            while START_MSG in stream and END_MSG in stream:
                start = stream.find(START_MSG)
                end = stream.find(END_MSG)
                batch_str = stream[start + SLEN: end]
                try:
                    batch = json.loads(batch_str)
                    for resp in batch["responses"]:
                        self._resp_data.put(resp)
                except (KeyError, TypeError, JSONDecodeError):
                    pass
                stream = stream[end + ELEN:]
