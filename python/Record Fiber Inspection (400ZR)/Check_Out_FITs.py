import win32com.client as win32
import time
from Query_Last_Result_Test import QueryLastResultTest
from FITs_LINECARD_Count import FITsLINECARDCount

#*************************************Check out only OPMP************************************
class CheckOutFITs:
    def input_detail(self, SERIAL_NUMBER, STATION_ID, EN, TX_SN, RX_SN, PI_Location, PROCESS):
        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        # 0 = Check in 
        # 1 = Check out
        # 2 = Update check out 
        # 3 = Update check in 
        # 5 = Delete Check out
        # 6 = Delete Check in

        if PROCESS == 'FCAL':
            operation = '2251'
        elif PROCESS == 'OPM':
            operation = '3105'
        elif PROCESS == 'OPMP':
            operation = '3106'
        elif PROCESS == 'OPMT':
            operation = '3107'

        FITs_Init = objFITS.fn_InitDB('All Module', operation, '0', 'dbAcacia') # (model,operation,revision,dbName) --- Initial Up FITs
        FITs_HandShake = objFITS.fn_Handshake('All Module', operation, '1', SERIAL_NUMBER)

        Query_Last_Result_Test = QueryLastResultTest()
        FITs_LINECARD_Count = FITsLINECARDCount()
        
        if FITs_Init == 'True' and FITs_HandShake == 'True':
            Data_ATS = Query_Last_Result_Test.input_data(SERIAL_NUMBER, PROCESS)
            LINECARD_Count = FITs_LINECARD_Count.input_data(str(Data_ATS[6]))
            if Data_ATS[14] == 'PASS':
                parameters = f'{SERIAL_NUMBER},{STATION_ID},{str(Data_ATS[3])},{Data_ATS[4]},{Data_ATS[5]},{str(Data_ATS[6])},{str(Data_ATS[1])},{Data_ATS[7]},{str(Data_ATS[8])},{EN},{PI_Location},{str(Data_ATS[9])},{str(Data_ATS[10])},{str(Data_ATS[11])},{str(Data_ATS[12])},{str(Data_ATS[13])},{str(Data_ATS[14])},NA,-,3107 : OPMT,{str(LINECARD_Count[1])},{TX_SN},{RX_SN}'
                FITs_Log_Check_Out = objFITS.fn_Log('All Module', operation, '1', 'FBN Serial No,Station ID,TEST_COUNT,Login Name,Mode,Fixture ID,TEST_SOCKET_INDEX,Product_Code,Product Code Revision,EN,PI Location,HW_PART_NUMBER,HW_REV,SW_REV,Date/Time,Execute Time,Result,Lid RT _SN,Disposition,send to,Line Card Counts,Tester Fiber Tx SN,Tester Fiber Rx SN', parameters, ",") # (model,operation,revision,parameters,values[,fsp]) --- Function for save data into FITs
                time.sleep(0.1)
                objFITS.closeDB()

                return FITs_Log_Check_Out, SERIAL_NUMBER
        else:
            return FITs_HandShake