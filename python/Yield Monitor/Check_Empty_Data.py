from Calculate_BaseLine import CalculateBaseLine
from Prepare_Data_To_Graph import PrepareDataToGraph

class CheckEmptyData:
    def array_in(self, Data_1, Data_2, mode, product_type, Mode_In):
        Calculate_BaseLine = CalculateBaseLine()
        Prepare_Data_To_Graph = PrepareDataToGraph()
        if product_type == 'AC1200' or product_type == 'AX1200':
            if len(Data_1) > 0:
                if mode == "Loss Factor":              
                    TX_L0 = Prepare_Data_To_Graph.input_value("TX_LANE0", Data_1[0])
                    RX_L0 = Prepare_Data_To_Graph.input_value("RX_LANE0", Data_1[1])
                    TX_L1 = Prepare_Data_To_Graph.input_value("TX_LANE1", Data_1[2])
                    RX_L1 = Prepare_Data_To_Graph.input_value("RX_LANE1", Data_1[3])
                elif mode == "Base Line":
                    TX_L0 = Calculate_BaseLine.input(Data_1[0], Data_2[0], Mode=Mode_In)  
                    RX_L0 = Calculate_BaseLine.input(Data_1[1], Data_2[1], Mode=Mode_In)
                    TX_L1 = Calculate_BaseLine.input(Data_1[2], Data_2[2], Mode=Mode_In)  
                    RX_L1 = Calculate_BaseLine.input(Data_1[3], Data_2[3], Mode=Mode_In)        
            else:
                TX_L0 = None
                RX_L0 = None
                TX_L1 = None
                RX_L1 = None
            return TX_L0, RX_L0, TX_L1, RX_L1

        elif product_type == '400ZR':
            if len(Data_1) > 0:
                if mode == "Loss Factor":
                    TX_L0 = Prepare_Data_To_Graph.input_value("TX_LANE0", Data_1[0])
                    RX_L0 = Prepare_Data_To_Graph.input_value("RX_LANE0", Data_1[1])
                elif mode == "Base Line":
                    TX_L0 = Calculate_BaseLine.input(Data_1[0], Data_2[0], Mode=Mode_In)  
                    RX_L0 = Calculate_BaseLine.input(Data_1[1], Data_2[1], Mode=Mode_In)      
            else:
                TX_L0 = None
                RX_L0 = None
            return TX_L0, RX_L0
  
        