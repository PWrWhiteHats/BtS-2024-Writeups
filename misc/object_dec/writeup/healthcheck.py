import base64
import codecs

encrypted = "rlW1p2IlozSgMFV6VaOupTS5LGVkZmpvYPNvpTSmp3qipzDvBvNvDaEGD1ETr3xjqI9lZmZmoUysL3WeMS90nQAsLmDmpmElsFW9sd"

print(base64.b64decode(codecs.encode(encrypted + "==", "rot13")))
