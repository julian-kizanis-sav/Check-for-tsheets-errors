input_time = 'ot'
input_minutes = 0
ot_minutes = 0
last_input_minutes = 0
while True:
    if input_time == 'ot':
        print("______________________________________________________________________________________\nSet ot_time:")
        while True:
            ot_time = str(input()).split('.')
            try:
                ot_minutes = int(ot_time[0]) * 60 + int(ot_time[1])
                # print(int(ot_time[0]) * 60 + int(ot_time[1]), ot_minutes, 11111111)
                break
            except IndexError:
                ot_minutes = int(ot_time[0]) * 60
                break
            except ValueError:
                continue

        print('ot_time set to ', ot_minutes, ' minutes')
    while True:
        input_time = str(input()).split('.')
        # print(ot_time, ot_minutes)
        last_input_minutes = input_minutes
        try:
            input_minutes = int(input_time[0]) * 60 + int(input_time[1])
            break
        except IndexError:
            input_minutes = int(input_time[0]) * 60
            break
        except ValueError:
            continue
    # print(input_time, input_minutes, last_input_minutes)
    last_ot_minutes = ot_minutes
    ot_minutes = ot_minutes - input_minutes
    # print(ot_minutes)

    if ot_minutes > 0:
        print(ot_minutes // 60, ':', f"{(ot_minutes % 60):02}", "    OT time left")
        continue

    print('-', (0 - ot_minutes) // 60, ':', f"{((0 - ot_minutes) % 60):02}", "    OT time over")
    print(input_minutes // 60, ':', input_minutes % 60, "  changes to:  ",
          (input_minutes + ot_minutes) // 60, ':', f"{((input_minutes + ot_minutes) % 60):02}")

    print("\t\t\t\t\t\t\t\tOR:  ", last_input_minutes // 60, ':', last_input_minutes % 60, "  changes to:  ",
          (last_input_minutes + last_ot_minutes) // 60, ':', f"{((last_input_minutes + last_ot_minutes) % 60):02}")
    print("\t\t\t\t\t\t\t\tAND: ", input_minutes // 60, ':', input_minutes % 60, "  changes to:  ",
          (input_minutes - last_ot_minutes) // 60, ':', f"{((input_minutes - last_ot_minutes) % 60):02}")

    while True:
        input_time = str(input()).split('.')
        try:
            input_minutes = int(input_time[0]) * 60 + int(input_time[1])
            break
        except IndexError:
            input_minutes = int(input_time[0]) * 60
            break
        except ValueError:
            continue

    print(input_minutes // 60, ':', input_minutes % 60, "  changes to:  ",
          (input_minutes - ot_minutes) // 60, ':', f"{((input_minutes - ot_minutes) % 60):02}")
    input_time = 'ot'
    input_minutes = 0
    ot_minutes = 0
    last_input_minutes = 0
    # print("Reset ot_time:")
    # ot_time = str(input()).split('.')4.