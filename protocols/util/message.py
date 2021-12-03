class Message:

    def __init__(self, header, payload):
        self.header = header
        self.payload = payload

    def byte_representation(self):
        return (str(self.header) + str(self.payload)).encode("utf-8")

    def __str__(self):
        return str(["header:", self.header, "payload", self.payload])


def main():
    message = Message(
        header={"control": "256adf", "len": 3},
        payload="tmp msg"
    )

    print(message)

    # s = "abcdef"
    # a = s.encode("utf-8")
    # print(a, type(a))

    # ascii_repr = [ord(c) for c in s]
    # print(ascii_repr)
    # binary_repr = [bin(i)[2:] for i in ascii_repr]
    # print(binary_repr)


if __name__ == '__main__':
    main()
