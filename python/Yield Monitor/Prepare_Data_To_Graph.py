class PrepareDataToGraph:
    def input_value(self, serie_name, data_in):
        Dict = {"name": serie_name, "data": []}
        if data_in is not None:
            for i, val in enumerate(data_in):
                Dict["data"].append((i,val))
        return Dict