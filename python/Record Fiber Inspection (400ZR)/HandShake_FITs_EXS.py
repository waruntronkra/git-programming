import win32com.client as win32

class HandShakeFITsEXS:
    def input_data(self, SERIAL_NUMBER, PROCESS):
        if PROCESS == 'EndFace EXP':
            operation = '3760'
        elif PROCESS == 'EXP':
            operation = '3500'

        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        FITs_Init = objFITS.fn_InitDB('All Module', operation, '1', 'dbAcacia') # (model,operation,revision,dbName) --- Initial Up FITs
        if FITs_Init == 'True':
            FITs_HandShake = objFITS.fn_Handshake('All Module', operation, '1', SERIAL_NUMBER) # (model,operation,revision,serial) --- Cheack whether this serial is allow to run or not
            return FITs_HandShake
        else:
            return FITs_Init
                
        objFITS.closeDB()