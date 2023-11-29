import json
import os
import shutil
import zipfile

import click
import requests
from pymaybe import maybe

from . import crypto_svc, status_svc

BASE_DIR = ".data"


def get_by_hash_id(hash_id: str, host: str):
    uri = f"{host}/recording/hash/{hash_id}/?format=json"
    try:
        resp = requests.get(uri)
        if resp.ok:
            data = resp.json()
            return get_by_uuid(data['guid'], host)
    except Exception:
        status_svc.prog()
        click.secho("Error: ", fg="red", nl=False)
        click.secho(f"This URL is invalid: {uri}", nl=False)


def get_by_uuid(uuid: str, host: str):
    return fetch_zip(f"{host}/recording/{uuid}/authenticity-data")


def fetch_zip(uri):
    try:
        resp = requests.get(uri, stream=True)
        if resp.ok:

            if not os.path.exists(BASE_DIR):
                os.mkdir(BASE_DIR)

            with open(f"{BASE_DIR}/all.zip", "wb") as f:
                for chunk in resp.iter_content(chunk_size=512):
                    f.write(chunk)

            with open(f"{BASE_DIR}/all.zip", "rb") as f:
                z = zipfile.ZipFile(f)
                z.extractall(f"{BASE_DIR}/")

            os.remove(f"{BASE_DIR}/all.zip")

            return True
    except Exception:
        status_svc.prog()
        click.secho("Error: ", fg="red", nl=False)
        click.secho(f"This URL is invalid: {uri}", nl=False)


def get_by_url(url: str):
    return fetch_zip(url.rstrip("/") + "/authenticity-data")


def get_by_zip(path: str):

    if os.path.exists(path) and maybe(path).split(".")[-1].lower().or_else("") == "zip":

        if not os.path.exists(BASE_DIR):
            os.mkdir(BASE_DIR)

        with open(path, "rb") as f:
            z = zipfile.ZipFile(f)
            z.extractall(f"{BASE_DIR}/")

        return True


def load_key(name):
    fname = f"{BASE_DIR}/{name}"
    return crypto_svc.load_pem_public_key_from_file(fname)


def gather():
    data = {"timestamps": {},
            "sensor": {},
            "recording": {},
            "device": {}}
    filenames = os.listdir(BASE_DIR)
    for fn in [x for x in filenames if x[-3:] != "pem"]:
        name, ext = fn.split(".")
        full = f"{BASE_DIR}/{fn}"
        if ext in {"tsq", "tsr"}:
            data['timestamps'][ext] = full
        else:
            chunks = name.split("_")
            uuid = chunks[2]
            key = chunks[1]
            data[key].setdefault(uuid, {})
            if "verum_sig" in fn:
                data[key][uuid]["verum"] = full
            elif "device_sig" in fn:
                data[key][uuid]["device"] = full
            elif "json" in fn:
                data[key][uuid]["data"] = full
    return data


def load_file(fn):
    with open(fn, "rb") as raw:
        return raw.read()


def clear():
    shutil.rmtree(BASE_DIR, ignore_errors=True)


def extract_data(file_map, key):
    data = file_map.get(key, {})
    keys = list(data.keys())
    if key in {"device", "recording"}:
        with open(data[keys[0]]['data']) as raw:
            return json.load(raw)
    elif key == "sensor":
        _data = {}
        for x in keys:
            with open(data[x]['data']) as raw:
                _data[x] = json.load(raw)
        return _data
    else:
        return {}
