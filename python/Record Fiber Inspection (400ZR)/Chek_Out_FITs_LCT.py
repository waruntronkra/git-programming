import win32com.client as win32
import time

class CheckOutFITsLCT:
    def input_data(self, SERIAL_NUMBER, STATION_ID, EN, TX_SN, RX_SN,PI_Location, PROCESS, Shim_SN):
        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        # 0 = Check in 
        # 1 = Check out
        # 2 = Update check out 
        # 3 = Update check in 
        # 5 = Delete Check out
        # 6 = Delete Check in

        # 2253 : LCT1 => 3010 : Endface Inspection (Temp Cycling)
        # 2254 : LCT2 => 3796 : Endface Inspection (OPM)
        # 2257 : LCTT => EOLR3 : Fiber Endface Inspection (ORL3)

        if PROCESS == 'LCT1':
            operation = '2253'
        elif PROCESS == 'LCT2':
            operation = '2254'
        elif PROCESS == 'LCTT':
            operation = '2257'

        FITs_Init = objFITS.fn_InitDB('All Module', operation, '0', 'dbAcacia') # (model,operation,revision,dbName) --- Initial Up FITs
        
        if FITs_Init == 'True':
            if PROCESS != 'LCTT':
                FITs_Check_In_TX = objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{TX_SN},{EN},PASS', ',')
                time.sleep(0.1)
                FITs_Check_In_RX = objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{RX_SN},{EN},PASS', ',')
                time.sleep(0.1)

                parameter = 'FBN Serial No,TEST_COUNT,Login Name,Mode,Station ID,Fixture ID,TEST_SOCKET_INDEX,EN,Tester Fiber Tx SN,Tester Fiber Rx SN,Shim SN,Product_Code,Product Code Revision,HW_PART_NUMBER,HE_REV,SW_REV,Date/Time,Excution Time,Result,Lid RT & SN,send to,PI Location,Line Card Counts'
                value = f'{SERIAL_NUMBER},{STATION_ID},{EN},{TX_SN},{RX_SN},{PI_Location},{Shim_SN}'
                FITs_Log_Check_In = objFITS.fn_Log('All Module', operation, '0', parameter, value, ',') # (model,operation,revision,parameters,values[,fsp]) --- Function for save data into FITs
                time.sleep(0.1)

                return FITs_Log_Check_In
                objFITS.closeDB()
                    

            