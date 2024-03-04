import win32com.client as win32
import time

class CheckInFITs:
    def input_data(self, SERIAL_NUMBER, HW_PART_NUMBER, Model, MC_Slot, Mode, START_DATE_TIME, UUT_STATUS, UUT_ID, Tx_OSNR_In_Band, Rx_Power_Monitor, Temperature_Laser, Temperature_ASIC, Tx_Power, ATS_PROCESS, UUT_Turnup_Tx_Max, ITLA_Frequency, OSNR, PROCESS):
        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

        if PROCESS == 'FCAL':
            operation = 'KGB_C'
        elif PROCESS == 'OPM':
            operation = 'KGB_M'

        FITs_Init = objFITS.fn_InitDB('*', operation, '1', 'dbAcacia')

        if FITs_Init == 'True':
            if operation == 'KGB_C':
                parameters = 'UUT_SERIAL_NUMBER,HW_PART_NUMBER,Model,MC_Slot,Mode,START_DATE_TIME,UUT_STATUS,UUT_ID,Tx OSNR In-Band,Rx Power Monitor,Temperature - Laser,Temperature - ASIC,Tx Power,ATS_PROCESS,Operation,UUT_Turnup_Tx_Max_PowerScreen'
                values = f"{SERIAL_NUMBER},{HW_PART_NUMBER},{Model},{MC_Slot},{Mode},{START_DATE_TIME},{UUT_STATUS},{UUT_ID},{Tx_OSNR_In_Band},{Rx_Power_Monitor},{Temperature_Laser},{Temperature_ASIC},{Tx_Power},{ATS_PROCESS},{operation},{UUT_Turnup_Tx_Max}"
            elif operation == 'KGB_M':
                parameters = 'UUT_SERIAL_NUMBER,HW_PART_NUMBER,Model,MC_Slot,Mode,START_DATE_TIME,UUT_STATUS,UUT_ID,Tx Power,ITLA Frequency Offset (GHz),Rx Power Monitor,OSNR - FEC Threshold,Temperature - ASIC,Temperature - Laser'
                values = f"{SERIAL_NUMBER},{HW_PART_NUMBER},{Model},{MC_Slot},{Mode},{START_DATE_TIME},{UUT_STATUS},{UUT_ID},{Tx_Power},{ITLA_Frequency},{Rx_Power_Monitor},{OSNR},{Temperature_ASIC},{Temperature_Laser}"

            FITs_Log_Check_In = objFITS.fn_Log('*', operation, '1', parameters, values, ',')
            
            time.sleep(0.1)

            if FITs_Log_Check_In == 'True':
                return FITs_Log_Check_In
            else:
                return FITs_Log_Check_In

        else:
            return FITs_Init
        
                        

                