raw_input = [i[:-1].split(" | ") for i in open("in.txt").readlines()]

s = 0




for row in raw_input:
    # print(row)

    decoded = {}

    todo = sorted(row[0].split(" "), key=len)

    for number in todo:

        print(len(number))


        decoded[
            {
                2:1,
                3:7,
                4:4

            }
            [len(number)]] = number



        t = {
            2: 1,
            3: 7,
            4: 4,
            5: 3 if set(decoded[1]).issubset(set(number)) else
            (5 if set(number).issubset(set(decoded[9])) else 2),
            6 : 9 if set(decoded[4]).issubset(set(number)) else
            (6 if not set(decoded[1]).issubset(set(number)) else (
                0 if set(decoded[4]).issubset(set(number)) and set(decoded[1]).issubset(set(number)) else -1
            )),
            7:8
        }

        decoded[t[len(number)]] = number



        # if len(number) == 2:
        #     decoded[1] = number
        #
        # elif len(number) == 3:
        #     decoded[7] = number
        #
        # elif len(number) == 4:
        #     decoded[4] = number
        #
        # elif len(number) == 6 and set(decoded[4]).issubset(set(number)):
        #     decoded[9] = number
        #
        # elif len(number) == 6 and not set(decoded[1]).issubset(set(number)):
        #     decoded[6] = number
        #
        # elif len(number) == 6 and not set(decoded[4]).issubset(set(number)) and set(decoded[1]).issubset(set(number)):
        #     decoded[0] = number
        #
        # elif len(number) == 7:
        #     decoded[8] = number

    for number in todo:

        if  len(number) == 5 and set(decoded[1]).issubset(set(number)):
            decoded[3] = number

        elif  len(number) == 5 and set(number).issubset(set(decoded[9])):
            decoded[5] = number

        elif len(number) == 5 and not set(number).issubset(set(decoded[9])):
            decoded[2] = number

    formatted = {"".join(sorted(v)): k for k,v in decoded.items()}

    t = ""
    for i in ["".join(sorted(i)) for i in row[1].split(" ")]:
        t += str(formatted[i])

    print(t)
    print()

    s += int(t)

print(s)