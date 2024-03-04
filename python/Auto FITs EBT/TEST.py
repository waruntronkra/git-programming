import win32com.client as win32
objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")

FITs_Init = objFITS.fn_InitDB('All Module', '2251', '1', 'dbAcacia')

parameters = 'FBN Serial No,send to,EN'
values = f"240653379,3796 : Endface Inspection (OPM),511997"
                   
FITs_Check_Out = objFITS.fn_Log('All Module', '2251', parameters, values, ',')

print(FITs_Check_Out)

objFITS.closeDB()
