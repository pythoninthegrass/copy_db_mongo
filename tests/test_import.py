#!/usr/bin/env python

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import pymongo
import requests
from decouple import config
from export import main
from testcontainers.mongodb import MongoDbContainer

# env vars
DB_HOST: str = config('DB_HOST')
DB_USER: str = config('DB_USER')
DB_PASS: str = config('DB_PASS')
DB_NAME: str = config('DB_NAME')
PORT: int = config('PORT', cast=int)
