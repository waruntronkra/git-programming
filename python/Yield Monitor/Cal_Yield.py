class CalYield():
    def input(self, array_in):
        Tuple_Yield = ()
        Pass_Amount = 0
        Fail_Amount = 0
        for j in array_in:
            if j[0] == "PASS":
                Pass_Amount  += 1
            elif j[0] != "PASS":
                Fail_Amount += 1
            else:
                Pass_Amount = 0
                Fail_Amount = 0
        Input = Pass_Amount + Fail_Amount
        if Input == 0:
            Percent_Yield = 0
            Str_Percent_Yield = str(Percent_Yield) + " %"
        else:
            Percent_Yield = (Pass_Amount/Input) * 100
            Format_Percent_Yield = "{:.2f}".format(Percent_Yield)
            Str_Percent_Yield = str(Format_Percent_Yield) + " %"

        Tuple_Yield = (str(Input), str(Pass_Amount), str(Fail_Amount), Str_Percent_Yield)
        return Tuple_Yield