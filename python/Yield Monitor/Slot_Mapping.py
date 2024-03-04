class SlotMapping():
    def input_data(self, LANE_Quantity, Start_From, Data_in, Array_DateTime_in):
        Array_SLOT = []
        for i in range(LANE_Quantity):
            i += Start_From
            Array_SLOT.append("Calibrate Port PORT" + str(i) + "TX")
            Array_SLOT.append("Calibrate Port PORT" + str(i) + "RX")

        Group_SLOT = {k:[] for k in Array_SLOT}
        for i in Data_in:
            if i[3] in Array_SLOT:
                Group_SLOT[i[3]].append(i[1:2] + i[4:5])
        for key in Group_SLOT:
            values = Group_SLOT[key]
            new_values = []
            for date in Array_DateTime_in:
                found = False
                for value in values:
                    if value[0] == date:
                        new_values.append(value)
                        found = True
                        break
                if not found:
                    new_values.append((date, ''))
            Group_SLOT[key] = new_values

        return Group_SLOT