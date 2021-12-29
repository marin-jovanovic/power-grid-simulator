class Message:

    def __init__(self, *args):
        if len(args) == 1:
            self.message_str_representation = args[0]

            # todo call decode method

        elif len(args) == 2:
            self.header = args[0]
            self.payload = args[1]

        else:
            raise NotImplementedError

    def byte_representation(self):
        if hasattr(self, "message_str_representation"):
            return (str(self.message_str_representation) + ";").encode("utf-8")
        else:
            return (str(self.header) + str(self.payload) + ";").encode("utf-8")

    def __str__(self):
        if hasattr(self, "message_str_representation"):
            return str(["message_str_representation:",
                        self.message_str_representation])

        elif hasattr(self, "header") and hasattr(self, "payload"):
            return str(["header:", self.header, "payload", self.payload])

        else:
            raise Exception

    def decode(self, payload):
        # raise NotImplementedError
        if payload.contains("{") and payload.contains("}"):
            print("header present and decodable")

            t = payload.split("}")

        else:
            print("no header present")


def main():
    message = Message(
        {"control": "256adf", "len": 3},
        "tmp msg"
    )

    print(message)


if __name__ == '__main__':
    main()
