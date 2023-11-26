from setuptools import setup, find_packages
from io import open


def read(filename):
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()


setup(
   name="CryptomusAPI",
   version="1.0.0",
   description="Easy interaction with Cryptomus API, support for asynchronous approaches",
   long_description_content_type="text/markdown",
   author="Fsoky",
   author_email="cyberuest0x12@gmail.com",
   keywords="api cryptomus asyncio crypto cryptomusapi",
   packages=find_packages()
)
