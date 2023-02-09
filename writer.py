import numpy as np
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import networkx as nx
from urllib.parse import urljoin, urlparse
from typing import (List, Sequence, Dict, Iterable,
    Optional, Union, Any)
import logging
from pathlib import Path

LOG_PATH = Path("./.log/exceptions.log")
if not LOG_PATH.parent.exists():
    LOG_PATH.parent.mkdir()
    LOG_PATH.touch()


LOGGER = logging.getLogger(LOG_PATH.as_posix())

class Writer:
    def __init__(self, 
        source: str="networkx",
        mode: str="bolt",
        ipaddress: str="127.0.0.1",
        port: int=7687,
        username: str="neo4j",
        password: str=None
        ):
        """
        :param source: takes "networkx" or "pandas"
        :param mode: takes "neo4j", "bolt", "http"
        :param ipaddress: ip address of the database
        :param port: port number of the database
        """
        protocol = mode if "://" in mode else f"://{mode}"
        address = f"{ipaddress}:{port}"
        self.uri = urljoin(protocol, address)
        self._username = username
        self._password = password
        self.driver = GraphDatabase.driver(self.uri, 
            auth=(username, password))

    @staticmethod
    def _node_exists(driver: GraphDatabase.driver, 
        type: str, 
        attributes: Dict[Any], 
        **kwargs):
        """check if a particular node exists"""
        attributes.update(**kwargs)
        attributes_str = ", ".join(f"{k}: {v}" for k, v in attributes.items())
        attributes_str = f"{{{attributes_str}}}"
        query = f"""OPTIONAL MATCH (p:{type} {attributes_str})"""
        LOGGER.log(level=logging.INFO,  msg=query)
        with driver.session as session:
            session.execute_read(query)

    # @staticmethod
    # def _create_edge(driver: GraphDatabase.driver, 
    #     source_node: Dict[Any], 
    #     target_node: Dict[Any], )
    #     """staticmethod for creating an edge"""


        

# class NetworkxWriter(Writer)