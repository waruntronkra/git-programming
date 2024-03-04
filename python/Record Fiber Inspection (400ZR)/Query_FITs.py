import win32com.client as win32

class QueryFITs:
    def input_data(self, SERIAL_NUMBER, PROCESS, HandCheck):
        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        # 0 = Check in 
        # 1 = Check out
        # 2 = Update check out 
        # 3 = Update check in 
        # 5 = Delete Check out
        # 6 = Delete Check in
        # 2251 = FCAL Check-In

        if PROCESS == 'FCAL':
            operation = '2251'
        elif PROCESS == 'OPM':
            operation = '3105'
        elif PROCESS == 'OPMP':
            operation = '3106'
        elif PROCESS == 'OPMT':
            operation = '3107'
        elif PROCESS == 'EndFace EXP':
            operation = '3760'
        elif PROCESS == 'EXP':
            operation = '3500'
        elif PROCESS == 'LCT1':
            operation == '2252'
        elif PROCESS == 'LCTT':
            operation == '2257'

        FITs_Init = objFITS.fn_InitDB('All Module', operation, '0', 'dbAcacia') # (model,operation,revision,dbName) --- Initial Up FITs
        if HandCheck == True:
            FITs_HandShake = objFITS.fn_Handshake('All Module', operation, '0', SERIAL_NUMBER)
        else:
            FITs_HandShake = 'True'

        if FITs_HandShake == 'True':
            if operation != '3500' and operation != '3760':
                FITs_Query = objFITS.fn_Query('All Module', operation, '0', f"{str(SERIAL_NUMBER)}", 'TEST_COUNT',',') # (model,operation,revision,serial) --- Cheack whether this serial is allow to run or not
                FITs_get_TX_RX = objFITS.fn_Query('All Module', operation, '0', f"{str(SERIAL_NUMBER)}", 'Tester Fiber Tx SN,Tester Fiber Rx SN',',')
                FITs_get_Shim_SN = objFITS.fn_Query('All Module', operation, '0', f"{str(SERIAL_NUMBER)}", 'Shim SN',',')
                objFITS.closeDB()

                Data_Tx_Rx = FITs_get_TX_RX.split(',')
                array_tx_rx = []
                for x in Data_Tx_Rx:
                    array_tx_rx.append(x)
                array_tx_rx = tuple(array_tx_rx)
                return FITs_Query,array_tx_rx,FITs_get_Shim_SN
                
            elif operation == '3500':
                FITs_Query = objFITS.fn_Query('All Module', operation, '0', f"{str(SERIAL_NUMBER)}", 'TEST_COUNT',',') # (model,operation,revision,serial) --- Cheack whether this serial is allow to run or not
                FITs_get_LoopBack_SN = objFITS.fn_Query('All Module', operation, '0', f"{str(SERIAL_NUMBER)}", 'Loop Back SN',',')
                FITs_get_Shim_SN = objFITS.fn_Query('All Module', operation, '0', f"{str(SERIAL_NUMBER)}", 'Shim SN',',')
                objFITS.closeDB()
                return FITs_Query,FITs_get_LoopBack_SN,FITs_get_Shim_SN
            elif operation == '3760':
                FITs_Query = objFITS.fn_Query('All Module', operation, '1', f"{str(SERIAL_NUMBER)}", 'TEST_COUNT',',') # (model,operation,revision,serial) --- Cheack whether this serial is allow to run or not
                FITs_get_LoopBack_SN = objFITS.fn_Query('All Module', operation, '1', f"{str(SERIAL_NUMBER)}", 'Loop Back SN',',')
                FITs_get_Shim_SN = objFITS.fn_Query('All Module', operation, '1', f"{str(SERIAL_NUMBER)}", 'Shim SN',',')
                objFITS.closeDB()
                return FITs_Query,FITs_get_LoopBack_SN,FITs_get_Shim_SN
        else:
            return FITs_HandShake
           