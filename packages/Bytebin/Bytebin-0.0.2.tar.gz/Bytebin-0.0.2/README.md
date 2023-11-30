# Bytebin.py

[![Image from Gyazo](https://i.gyazo.com/2ddbbc37300edbe85c873074fb0e4208.png)](https://gyazo.com/2ddbbc37300edbe85c873074fb0e4208)

A simple python wrapper for [Bytebin](https://bytebin.dev/)

## Installation

```sh
pip install Bytebin
```

## Example

```py
import Bytebin

bb = Bytebin.Bytebin()

paste = bb.create("Hello World!")

print(paste.url)
print(paste.key)

lookup = bb.lookup(paste.key)

print(lookup.url)
print(lookup.key)
print(lookup.content)
```
