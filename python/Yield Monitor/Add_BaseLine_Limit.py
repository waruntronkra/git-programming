class AddBaseLineLimit:
    def input(self, data_in):
        file_limit = open('temp/LIMIT.txt', 'r')
        limit_read = file_limit.read()
        limit_read = limit_read.split('\n')
        data_ucl = []
        data_lcl = []
        for i in range(len(data_in[0]['data'])):
            value = []
            for item in data_in:
                value.append(item['data'][i])
            data_ucl.append((i, limit_read[0]))
            data_lcl.append((i, limit_read[1]))
        data_in.append({'name': 'UCL', 'data': data_ucl})
        data_in.append({'name': 'LCL', 'data': data_lcl})

        return data_in

