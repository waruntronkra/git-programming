import win32com.client as win32

class CheckOutFITs:
    def input_data(self, EN, SERIAL_NUMBER, TEST_COUNT, PRODUCT_CODE, FIXTURE_ID, START_DATE_TIME, EXECUTION_TIME, MODE, USER_LOGIN_NAME, TEST_SOCKET_INDEX, TPS_REV, HW_PART_NUMBER, HW_REV, FW_REV, Result, send_to, LC_Count, operation):
        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        FITs_Init = objFITS.fn_InitDB('*', operation, '1', 'dbAcacia')

        if FITs_Init == 'True':
            FITs_HandShake = objFITS.fn_Handshake('*', operation, '1', SERIAL_NUMBER)
            if FITs_HandShake == 'True':
                # ================ Check Out ================
                if operation == 'P030':
                    parameters = 'EN,PCBA Serial Number,TEST_COUNT,Product_Code,Fixture ID,Date/Time,Execute Time,Mode,Login Name,TEST_SOCKET_INDEX,TPS_REV,HW_PART_NUMBER,HW_REV,FW_REV,Result,send to,Line Card Counts'
                    values = f"{EN},{SERIAL_NUMBER},{TEST_COUNT},{PRODUCT_CODE},{FIXTURE_ID},{START_DATE_TIME},{EXECUTION_TIME},{MODE},{USER_LOGIN_NAME},{TEST_SOCKET_INDEX},{TPS_REV},{HW_PART_NUMBER},{HW_REV},{FW_REV},{Result},{send_to},{LC_Count}"
                    FITs_Check_Out = objFITS.fn_Log('*', operation, '1', parameters, values, ',')
                    
                    if FITs_Check_Out == 'True':
                        return FITs_Check_Out
                    else:
                        return FITs_Check_Out

                elif operation == 'P025':
                    parameters = 'EN,PCBA Serial Number,Result,send to'
                    values = f"{EN},{SERIAL_NUMBER},PASS,{send_to}"
                    FITs_Check_Out = objFITS.fn_Log('*', operation, '1', parameters, values, ',')

                    if FITs_Check_Out == 'True':
                        return FITs_Check_Out
                    else:
                        return FITs_Check_Out
            else:
                return FITs_HandShake

        else:
            return FITs_Init
        
                        

                