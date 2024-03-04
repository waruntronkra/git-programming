import win32com.client as win32
import time
from Query_Last_Result_Test_LCT import QueryLastResultTestLCT

class CheckInFITs:
    def input_data(self, SERIAL_NUMBER, STATION_ID, EN, TX_SN, RX_SN, PI_Location, PROCESS, Shim_SN):
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
            operation == '2253'
        elif PROCESS == 'LCT2':
            operation == '2254'

        FITs_Init = objFITS.fn_InitDB('All Module', operation, '0', 'dbAcacia') # (model,operation,revision,dbName) --- Initial Up FITs

        if FITs_Init == 'True':
            if PROCESS == 'FCAL':            
                FITs_Log_Check_In = objFITS.fn_Log('All Module', operation, '0', 'FBN Serial No,Station ID,EN,Tester Fiber Tx SN,Tester Fiber Rx SN,PI Location,Shim SN', f'{SERIAL_NUMBER},{STATION_ID},{EN},{TX_SN},{RX_SN},{PI_Location},{Shim_SN}', ',') # (model,operation,revision,parameters,values[,fsp]) --- Function for save data into FITs
                time.sleep(0.1)
                return FITs_Log_Check_In
                objFITS.closeDB()

            elif PROCESS == 'LCT1' or PROCESS == 'LCT2':            
                FITs_Check_In_TX = objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{TX_SN},{EN},PASS', ',')
                time.sleep(0.1)
                FITs_Check_In_RX = objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{RX_SN},{EN},PASS', ',')
                time.sleep(0.1)

                Data_ATS = QueryLastResultTestLCT().input_data(UUT_SN, PROCESS)

                parameter = "EN,FBN Serial No,TEST_COUNT,Login Name,Mode,Station ID,Fixture ID,TEST_SOCKET_INDEX,EN,Tester Fiber Tx SN,Tester Fiber Rx SN,Shim SN,Product_Code,Product Code Revision,HW_PART_NUMBER,HE_REV,SW_REV,Date/Time,Excution Time,Result,Lid RT & SN,Error Code,Disposition,send to,PI Location,Line Card Counts"            
                value = f"{EN},{str(Data_ATS[0])},{str(Data_ATS[1])},{str(Data_ATS[2])},{str(Data_ATS[3])},{str(Data_ATS[4])},{str(int(Data_ATS[5]) - 1)},{str(Data_ATS[6])},{EN},{str(TX_SN)},{str(RX_SN)},{str(Shim_SN)},{str(Data_ATS[7])},{str(Data_ATS[8])},{str(Data_ATS[9])},{str(Data_ATS[10])},{str(Data_ATS[11])},{str(Data_ATS[12])},{str(Data_ATS[13])},{str(Data_ATS[14])},NA,-,-,3010 : Endface Inspection (Temp Cycling),{PI_Location},762"
        
                FITs_Log_Check_In = objFITS.fn_Log('All Module', operation, '1', parameter, value, ',')
                time.sleep(0.1)

                objFITS.closeDB()

            else:
                FITs_Check_In_TX = objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{TX_SN},{EN},PASS', ',')
                time.sleep(0.1)
                FITs_Check_In_RX = objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{RX_SN},{EN},PASS', ',')
                time.sleep(0.1)
                FITs_Log_Check_In = objFITS.fn_Log('All Module', operation, '0', 'FBN Serial No,Station ID,EN,Tester Fiber Tx SN,Tester Fiber Rx SN,PI Location,Shim SN', f'{SERIAL_NUMBER},{STATION_ID},{EN},{TX_SN},{RX_SN},{PI_Location},{Shim_SN}', ',') # (model,operation,revision,parameters,values[,fsp]) --- Function for save data into FITs
                time.sleep(0.1)
                return FITs_Log_Check_In
                objFITS.closeDB()

        else:
            return 'Connection Failed !'
                

           