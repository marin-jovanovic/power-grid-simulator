from ast import literal_eval

# todo check if literal eval is safe
class Message:
    """
    used for communication between server and client

    when server or client is sending message it is sending this object

    assumption is that we can only send strings with used protocol

    header is stored as dictionary

    payload is stored as any

    ----------------------------------------------------------------------------

    recommended use

            message = Message(
                {"param 1": "val 1", "param 2": "val 2"},
                "payload content"
            )

        server sending

            server.send(
                message.encode()
            )

        server receiving
            message = server.receive().decode()

    supported use

            message = Message(arg[0], arg[1])
            arg[0] = None, any
            arg[1] = None, any, left out


    """

    def __init__(self, *args):
        if len(args) == 1:

            message = args[0]

            if isinstance(args[0], str):
                print("not string, performing casting")

                message = str(message)
                # args[0] = str(args[0])

            self.header, self.payload = Message.decode(message)

        elif len(args) == 2:

            h, p = args[0], args[1]

            if not p:

                p = h if h else p

                h = {}

            if h:

                try:
                    self.header = literal_eval(h)

                    # todo check cast to json

                except ValueError:
                    print("error parsing header")
                    self.header = h

            else:
                self.header = {}
            payload_buffer = None
            if not isinstance(self.header, dict):
                # self.payload = self.header
                payload_buffer = self.header
                self.header = {}

            if p:

                try:
                    # todo see if json casting is better suited
                    self.payload = literal_eval(p)
                except ValueError:
                    print("error parsing payload")
                    self.payload = p

            else:
                self.payload = None

            if payload_buffer:
                self.payload = str(payload_buffer) + str(self.payload)

        else:
            raise NotImplementedError

    def byte_representation(self):
        return (str(self.header) + str(self.payload) + ";").encode("utf-8")

    def __str__(self):
        return str(["header:", self.header, "payload", self.payload])

    @staticmethod
    def decode(message: str):
        """
        decodes message and tries to evaluate its content

        expected
            message = {
                "header": any,
                "payload": any
            }


        :param message: input as string
        :return: decoded message as (header, payload)
        """

        print(f"to decode {message=} {type(message)=}")

        if not isinstance(message, str):
            print("input is not string")

            if not message:
                return {}, None

            message = str(message)

        try:
            message_as_json = json.loads(message)

            print(f"{message_as_json=}")

            header = message_as_json["header"]
            payload = message_as_json["payload"]

        except json.decoder.JSONDecodeError:
            print("not json")

            header = {}

            try:
                payload = literal_eval(message)
            except ValueError:
                print(f"val err for {message=}")
                header = {}
                payload = message


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

    try:
        Message()
        assert False
    except NotImplementedError:
        pass

    # import pathlib
    # curr_path = pathlib.Path(__file__).parent.resolve()
    #
    # with open(curr_path / "message.py", "r") as f:
    #     lines = f.readlines()
    #
    # from inspect import currentframe
    #
    # def get_line_number():
    #     cf = currentframe()
    #     # print(cf.f_back.f_lineno)
    #     return cf.f_back.f_lineno
    #
    # print("test", lines[get_line_number()])
    # message = Message(None)
    # assert message.header == {}
    # assert message.payload is None
    #
    # print("test", lines[get_line_number()])
    # message = Message(None, None)
    # assert message.header == {}
    # assert message.payload is None
    #
    # print("test", lines[get_line_number()])
    # message = Message(None, "a")
    # assert message.header == {}
    # assert message.payload == "a"
    #
    # print("test", lines[get_line_number()])
    # message = Message("a", None)
    # assert message.header == {}
    # assert message.payload == "a"
    #
    # print("test", lines[get_line_number()])
    # message = Message({"a": "b"}, None)
    # assert message.header == {}
    # assert message.payload == {"a": "b"}
    #
    # print("test", lines[get_line_number()])
    # message = Message(None, {"a": "b"})
    # assert message.header == {}
    # assert message.payload == {"a": "b"}
    #
    # print("test", lines[get_line_number()])
    # message = Message({"a": "b"}, {"c": "d"})
    # assert message.header == {"a": "b"}
    # assert message.payload == {"c": "d"}
    #
    # print("test", lines[get_line_number()])
    # message = Message({"a": "b", "c": {"d": "e"}}, None)
    # assert message.header == {}
    # assert message.payload == {"a": "b", "c": {"d": "e"}}
    #
    # print("test", lines[get_line_number()])
    # message = Message({"a": "b", "c": {"d": "e"}}, {"f": "g", "h": {"i": "j"}})
    # assert message.header == {"a": "b", "c": {"d": "e"}}
    # assert message.payload == {"f": "g", "h": {"i": "j"}}
    #
    #
    # return

    # message_as_json = json.loads(str('{"a": {"b": {"d": ["e", "f"]}}}'))
    # print(message_as_json)
    # print(message_as_json["a"])
    # print(message_as_json["a"]["b"])
    # print(message_as_json["a"]["b"]["d"])
    #
    # message_as_json = json.loads("['a', 'b']")
    # print(message_as_json)
    # return

    for m, expected_header, expected_payload in [
        (None, {}, None),
        ("a", {}, "a"),
        ({"a": "b"}, {}, {"a": "b"}),
        ({"a": "b", "c": {"d": "e"}}, {}, {"a": "b", "c": {"d": "e"}}),
        (["a", "b"], {}, ["a", "b"]),
        ({"c", "ab"}, {}, {"c", "ab"}),

    ]:

        print(f"test {m=}, {expected_header=} {expected_payload=}")

        # todo test with one arg
        message = Message(m)
        print(f"{message.header=}")
        print(f"{message.payload=}")

        assert message.header == expected_header
        assert message.payload == expected_payload

        print()


    for header, payload, expected_header, expected_payload in [
        (None, None, {}, None),
        (None, "a", {}, "a"),
        ("a", None, {}, "a"),
        ({"a": "b"}, None, {}, {"a": "b"}),
        (None, {"a": "b"}, {}, {"a": "b"}),
        ({"a": "b"}, {"c": "d"}, {"a": "b"}, {"c": "d"}),
        ({"a": "b", "c": {"d": "e"}}, None, {}, {"a": "b", "c": {"d": "e"}}),
        ({"a": "b", "c": {"d": "e"}}, {"f": "g", "h": {"i": "j"}}, {"a": "b", "c": {"d": "e"}}, {"f": "g", "h": {"i": "j"}}),

        (None, ["a", "b"], {}, ["a", "b"]),
        (["a", "b"], None, {}, ["a", "b"]),

        ("c", ["a", "b"], {}, "c" + str(["a", "b"])),
        (["d", "e"], ["a", "b"], {}, str(["d", "e"]) + str(["a", "b"])),
        ({"c"}, ["a", "b"], {}, str({"c"}) + str(["a", "b"])),
        ({"c"}, None, {}, {"c"}),
        ({"c"}, "ab", {}, str({"c"}) + "ab"),
    ]:

        print(f"test {header=} {payload=}")

        # todo test with one arg
        message = Message(header, payload)
        print(f"{message.header=}")
        print(f"{message.payload=}")

        assert message.header == expected_header
        assert message.payload == expected_payload

        print()

if __name__ == '__main__':
    main()
