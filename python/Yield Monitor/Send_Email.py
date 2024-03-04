import win32com.client
import pyautogui
import time

class SendEmail:
    def data_in(self, text_in, attachments):     
        # myScreenshot = pyautogui.screenshot()
        # myScreenshot.save("temp/alert.png")
        # time.sleep(1)

        ol=win32com.client.Dispatch("outlook.application")
        olmailitem=0x0 #size of the new email
        newmail=ol.CreateItem(olmailitem)
        newmail.Subject= 'Calibration Out of Control Alert'

        recipients = ["arpassorn_b@fabrinet.co.th", "kamonpakornp@fabrinet.co.th"]
        cc_recipients = ["sakol_b@fabrinet.co.th", "nitithon_s@fabrinet.co.th", "petmanee_s@fabrinet.co.th", "arnon_ti@fabrinet.co.th"]
        newmail.To = ';'.join(recipients)  # Join multiple recipients with semicolon (;)
        newmail.CC = ';'.join(cc_recipients)  # Join multiple CC recipients with semicolon (;)  
        # newmail.To='waruntronk@fabrinet.co.th'

        newmail.Body= text_in

        for attach in attachments:
            if os.path.exists(attach):
                newmail.Attachments.Add(attach)
            else:
                print(f"Attachment path does not exist: {attach}")

        try:
            newmail.Send()
            print("Email sent successfully.")
        except Exception as e:
            print(f"An error occurred while sending the email: {str(e)}")

        newmail.Send()