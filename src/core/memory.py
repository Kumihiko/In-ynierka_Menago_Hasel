class SecureString:
    def __init__(self, data: str | bytes):
        if isinstance(data, str):
            self._data = bytearray(data.encode('utf-8'))
        elif isinstance(data, bytes):
            self._data = bytearray(data)
        else:
            raise TypeError("Dane musza byc typu str lub bytes")

    def get_bytes(self) -> bytes:
        return bytes(self._data)

    def destroy(self) -> None:
        for i in range(len(self._data)):
            self._data[i] = 0