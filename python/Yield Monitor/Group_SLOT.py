class GroupSLOT:
    def Input(self, Data_In, Name_LANE0_TX, Name_LANE0_RX, Name_LANE1_TX, Name_LANE1_RX, Product_Type):
        if Product_Type == 'AC1200' or Product_Type == 'AX1200':
            LANE0_TX = []
            LANE0_RX = []
            LANE1_TX = []
            LANE1_RX = []

            for i in Data_In[Name_LANE0_TX]:
                LANE0_TX.append(i[1])
            for i in Data_In[Name_LANE0_RX]:
                LANE0_RX.append(i[1])
            for i in Data_In[Name_LANE1_TX]:
                LANE1_TX.append(i[1])
            for i in Data_In[Name_LANE1_RX]:
                LANE1_RX.append(i[1])               
            Array_to_Graph = [LANE0_TX, LANE0_RX, LANE1_TX, LANE1_RX]

        elif Product_Type == '400ZR':
            LANE0_TX = []
            LANE0_RX = []

            for i in Data_In[Name_LANE0_TX]:
                LANE0_TX.append(i[1])
            for i in Data_In[Name_LANE0_RX]:
                LANE0_RX.append(i[1])            
            Array_to_Graph = [LANE0_TX, LANE0_RX]
        
        return Array_to_Graph