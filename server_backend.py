

class ServerBackend:
    def __init__(self):
        self._is_server = False

        print(self._is_server)


class ControllerBackend(ServerBackend):
    def __init__(self):
        ServerBackend.__init__(self)
        self._is_server = True


if __name__ == '__main__':
    moin = ControllerBackend()
