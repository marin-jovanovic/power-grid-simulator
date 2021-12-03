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
        return (str(self.header) + str(self.payload)).encode("utf-8")

    def __str__(self):
        if hasattr(self, "message_str_representation"):
            return str(["message_str_representation:",
                        self.message_str_representation])

        elif hasattr(self, "header") and hasattr(self, "payload"):
            return str(["header:", self.header, "payload", self.payload])

        else:
            raise Exception

    def decode(self, payload):
        raise NotImplementedError

        # if sw == "upload":
        #
        #     sw = raw_data[1]
        #
        #     if sw == "get_curr_state":
        #         print("get curr state")
        #
        #     elif sw == "get_init_data":
        #         print("get init data")
        #
        #     elif sw == "get_curr_data":
        #         print("get curr data")
        #
        #     elif sw == "update_data":
        #         print("update data")
        #
        # elif sw == "download":
        #     pass
        #
        # else:
        #     raise NotImplementedError

def main():
    message = Message(
        {"control": "256adf", "len": 3},
        "tmp msg"
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
