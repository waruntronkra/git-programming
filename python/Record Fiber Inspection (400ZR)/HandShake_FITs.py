import win32com.client as win32

class HandShakeFITs:
    def input_data(self, SERIAL_NUMBER, PROCESS):
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
        elif PROCESS == 'LCT1':
            operation == '2252'
        elif PROCESS == 'LCTT':
            operation == '2257'

        FITs_Init = objFITS.fn_InitDB('All Module', '2251', '0', 'dbAcacia') # (model,operation,revision,dbName) --- Initial Up FITs
        FITs_HandShake = objFITS.fn_Handshake('All Module', operation, '0', SERIAL_NUMBER) # (model,operation,revision,serial) --- Cheack whether this serial is allow to run or not
        objFITS.closeDB()

        return FITs_HandShake
           