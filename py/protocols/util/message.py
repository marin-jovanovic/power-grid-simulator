from ast import literal_eval


class Message:
    """
    used for communication between server and client
    when server or client is sending message it is sending this object

    assumption is that we can only send strings with used protocol

    server sending
        message = Message(
            {"param 1": "val 1", "param 2": "val 2"},
            "payload content"
        )

        server.send(
            message.encode()
        )

    server receiving
        message = server.receive().decode()

    """

    def __init__(self, *args):
        if len(args) == 1:

            self.header, self.payload = Message.decode(args[0])

        elif len(args) == 2:
            self.header = args[0]
            self.payload = literal_eval(args[1])

        else:
            raise NotImplementedError

    def byte_representation(self):
        return (str(self.header) + str(self.payload) + ";").encode("utf-8")

    def __str__(self):
        return str(["header:", self.header, "payload", self.payload])

    @staticmethod
    def decode(message):

        # we assume this was used prior to calling this json.dumps
        # but we are checking for edge cases

        print(f"to decode {message=}")

        if not isinstance(message, str):
            print("input is not string")

            if not message:
                return {}, ""

            message = str(message)


        # if message.__contains__("{"):
            # try format as json
            # header present

        try:
            message_as_json = json.loads(message)

            print(f"{message_as_json=}")

            header = message_as_json["header"]
            payload = message_as_json["payload"]

        except json.decoder.JSONDecodeError:
            header = {}
            payload = message

            print("not json")

        # else:
        #     header = {}
        #     payload = message

        # if message.__contains__("{"):
        #     # header present
        #
        #     indices = [i for i, c in enumerate(content) if c == "}"]
        #     last_index = indices[-1]
        #
        #     header = message[:last_index + 1]
        #
        #     header = literal_eval(header)
        #     payload = message[last_index + 1:]
        #
        # else:
        #     header = {}
        #     payload = message

        return header, payload

    @staticmethod
    def encode(message):
        return json.dumps(message)

import json

def main():
    # message = Message(
    #     {
    #         "header":        {"control": "256adf", "len": 3},
    #         "payload":        "tmp msg"
    #     }
    # )

    # print(message)

    # header = {"a": "b", "c": "{}", "d": "{}", "e": "{}"}
    #
    # c = {
    #         "header":        {"control": "256adf", "len": 3},
    #         "payload":        "tmp msg"
    #     }
    # print(c)
    # print(type(c))

    # content =        json.dumps({
    #         "header":        {"control": "256adf", "len": 3},
    #         "payload":        "tmp msg"
    #     })
    #
    #
    #
    # print(f"{content=}")
    #
    # if content.__contains__("{"):
    #     # try format as json
    #     # header present
    #
    #     message_as_json = json.loads(content)
    #
    #     print(f"{message_as_json=}")
    #
    #     header = message_as_json["header"]
    #     payload = message_as_json["payload"]
    #
    # else:
    #     header = {}
    #     payload = content
    #
    # print(f"{header=}")
    # print(f"{payload=}")

    for header, payload in [
        (None, None),
        (None, "a"),
        ("a", None),
        ({"a": "b"}, None),
        (None, {"a": "b"}),
        ({"a": "b"}, {"c": "d"}),
        ({"a": "b", "c": {"d": "e"}}, None),
        ({"a": "b", "c": {"d": "e"}}, {"f": "g", "h": {"i": "j"}}),
    ]:
        print(f"{header=}")
        print(f"{payload=}")

        if not header:
            message = Message(payload)

        elif not payload:
            message = Message(header)

        else:
            message = Message(header, payload)

        print(message)

        assert isinstance(message.header, dict)
        assert isinstance(message.payload, str)

        # print("header type", type(message.header))
        # print("payload type", type(message.payload))
        print()

if __name__ == '__main__':
    main()
