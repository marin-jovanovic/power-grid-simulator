class Message:

    def __init__(self, *args):
        if len(args) == 1:
            self.message_str_representation = args[0]

            # todo call decode method
            #   and decode in header and payload

            # self.header = args[0]
            # self.payload = args[1]

        elif len(args) == 2:
            self.header = args[0]
            self.payload = args[1]

        else:
            raise NotImplementedError

    def byte_representation(self):

        # todo config to only header and payload type

        return (str(self.message_str_representation)
                    if hasattr(self, "message_str_representation") else
                str(self.header) + str(self.payload)
                     + ";").encode("utf-8")

        # if hasattr(self, "message_str_representation"):
        #     return (str(self.message_str_representation) + ";").encode("utf-8")
        # else:
        #     return (str(self.header) + str(self.payload) + ";").encode("utf-8")

    def __str__(self):
        if hasattr(self, "message_str_representation"):
            return str(["message_str_representation:",
                        self.message_str_representation])

        elif hasattr(self, "header") and hasattr(self, "payload"):
            return str(["header:", self.header, "payload", self.payload])

        else:
            raise Exception

    @staticmethod
    def decode(payload):
        # raise NotImplementedError

        print("decoding", payload)

        payload = str(payload)

        if payload.__contains__("{") and payload.__contains__("}"):
            print("header present and decodable")

            t = payload.split("}")

        else:
            print("no header present")

        return payload

def main():
    message = Message(
        {"control": "256adf", "len": 3},
        "tmp msg"
    )

    print(message)

    content = "{tmp}abc"

    if content.__contains__("{"):
        # header present
        pass


if __name__ == '__main__':
    main()
