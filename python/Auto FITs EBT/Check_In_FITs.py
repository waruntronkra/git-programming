import win32com.client as win32

class CheckInFITs:
    def input_data(self, SERIAL_NUMBER, TEST_COUNT, STATION_ID,):
        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        FITs_Init = objFITS.fn_InitDB('*', 'P030', '0', 'dbAcacia')

        if FITs_Init == 'True':
            FITs_HandShake = objFITS.fn_Handshake('*', 'P030', '0', SERIAL_NUMBER)
            if FITs_HandShake == 'True':
                # ================ Check In ================
                parameters = 'PCBA Serial Number,TEST_COUNT,Station ID'
                values = f"{SERIAL_NUMBER},{TEST_COUNT},{STATION_ID}"
                FITs_Check_In = objFITS.fn_Log('*', 'P030', '0', parameters, values, ',')
                
                if FITs_Check_In == 'True':
                    return FITs_Check_In
                else:
                    return FITs_Check_In
            else:
                return FITs_HandShake

        else:
            return FITs_Init
        
                        

                