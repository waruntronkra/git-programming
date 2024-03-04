class CalculateBaseLine:
    def input(self, Array_BaseLine, Array_Data, Mode):
        if Mode == 'CAL':
            array_in = []
            for val in Array_Data:    
                array_in.append(format((float(val) - float(Array_BaseLine)), ".2f"))
            return array_in
        elif Mode == 'NOT CAL':
            array_in = []
            for val in Array_Data:    
                array_in.append(format(float(Array_BaseLine), ".2f"))
            return array_in