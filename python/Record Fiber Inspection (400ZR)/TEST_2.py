import win32com.client as win32
import time

file_type = '.pdf'
SERIAL_NUMBER = '233250157'
EN = '511997'
LoopBack_SN = 'FB0074'
Shim_SN = "TEST123"
PROCESS = "EndFace EXP"
PI_Location = "BAY6.FBER.01.A"
File_2 = ""

objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

FITs_Init = objFITS.fn_InitDB('All Module', '3760', '1', 'dbAcacia')
EndFace_Path = '\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\' + str(SERIAL_NUMBER) + file_type


if FITs_Init == 'True':
    if PROCESS == 'EndFace EXP':
        # Register Fiber
        print(objFITS.fn_Log('*', 'TSEI', '1', 'TSEI SN,EN,Result', f'{LoopBack_SN},{EN},PASS', ','))

        # Check in Endface EXP then send to EXP (check in)
        parameter_endface_exp = 'EN,FBN Serial No,Loop Back SN,Endface Result,Water Mark on End Face,send to,PI Location,Attach File #1,Attach File #2'
        value_endface_exp = f'{EN},{SERIAL_NUMBER},{LoopBack_SN},PASS,NO,3500 : EXP,{PI_Location},{EndFace_Path},{File_2}'
        print(objFITS.fn_Log('All Module', '3760', '1', parameter_endface_exp, value_endface_exp, ','))
        time.sleep(0.1)

        # Check in EXP
        parameter_exp = 'FBN Serial No,Tester Fiber Tx SN,Tester Fiber Rx SN,Shim SN,EN,PI Location'
        value_exp = f'{SERIAL_NUMBER},{LoopBack_SN},{LoopBack_SN},{Shim_SN},{EN},BAY6.EXS.02.A'
        print(objFITS.fn_Log('All Module', '3500', '0', parameter_exp, value_exp,','))             
        time.sleep(0.1)

        objFITS.closeDB()      

    elif PROCESS == 'EXP':
        # Check in EXP
        parameter_exp = 'FBN Serial No,Tester Fiber Tx SN,Tester Fiber Rx SN,Shim SN,EN,PI Location'
        value_exp = f'{SERIAL_NUMBER},{LoopBack_SN},{LoopBack_SN},{Shim_SN},{EN},BAY6.EXS.02.A'
        objFITS.fn_Log('All Module', '3500', '0', parameter_exp, value_exp,',')  
        time.sleep(0.1)

    