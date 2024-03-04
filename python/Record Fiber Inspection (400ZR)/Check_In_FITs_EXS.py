import win32com.client as win32
import time

class CheckInFITsEXS:
    def input_data(self, SERIAL_NUMBER, STATION_ID, EN, LoopBack_SN,PI_Location, Shim_SN, Endface_Result, Water_Mark, File_1,File_2, file_type, PROCESS):
        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        # 0 = Check in 
        # 1 = Check out
        # 2 = Update check out 
        # 3 = Update check in 
        # 5 = Delete Check out
        # 6 = Delete Check in
        # 2251 = FCAL Check-In

        FITs_Init = objFITS.fn_InitDB('All Module', '3760', '1', 'dbAcacia') # (model,operation,revision,dbName) --- Initial Up FITs

        EndFace_Path = '\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\' + str(SERIAL_NUMBER) + file_type

        if FITs_Init == 'True':
            if PROCESS == 'EndFace EXP':
                # Register Fiber
                objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{LoopBack_SN},{EN},PASS', ',')
                time.sleep(0.1)

                # Check in Endface EXP then send to EXP (check in)
                parameter_endface_exp = 'EN,FBN Serial No,Loop Back SN,Endface Result,Water Mark on End Face,send to,PI Location,UUT file,Attach File #2'
                value_endface_exp = f'{EN},{SERIAL_NUMBER},{LoopBack_SN},PASS,NO,3500 : EXP,{PI_Location},{EndFace_Path},{File_2}'
                output = objFITS.fn_Log('All Module', '3760', '1', parameter_endface_exp, value_endface_exp, ',')
                time.sleep(0.1)

                objFITS.closeDB()    

                return output

            elif PROCESS == 'EXP':
                # Register Fiber
                objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{LoopBack_SN},{EN},PASS', ',')
                time.sleep(0.1)

                # Check in EXP
                parameter_exp = 'FBN Serial No,Loop Back SN,Shim SN,EN,PI Location'
                value_exp = f'{SERIAL_NUMBER},{LoopBack_SN},{Shim_SN},{EN},BAY6.EXS.02.A'
                output = objFITS.fn_Log('All Module', '3500', '0', parameter_exp, value_exp,',')  
                time.sleep(0.1)

                return output