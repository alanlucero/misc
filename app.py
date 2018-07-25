import datetime, time
import msvcrt as m
from colorama import Fore
from colorama import Style

def initiate():
    print(f'{Fore.GREEN} Initiating program... Press any key to start.{Style.RESET_ALL}')
    input()
    status = True
    return status

def stop():
    status = False
    return status

def startProgram():
    ts = time.time()
    ts_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("=====================" + ts_str + "=====================")
    print("  BND for searching for bond \n  EQ for searching for an equity")
    opt = input("   Type the type of instrument")
    if opt == "EQ":
        isin = input("ISIN:")
    else:
        isin = input("Bond ISIN: ")
    print("Please confirm the following transaction:")
    print("Instrument: " + opt)
    print("ISIN: " + isin)
    confirm = input("Do you want to confirm this transaction? y/n")
    if confirm == 'y' or confirm == "Y":
        print('Transaction recorded.')
    else:
        exit()

    stay = input("Do you want to stay in the program?")
    if stay == "n":
        stop()
    else:
        exit()
    return print("Saved at " + ts_str)

if __name__ == "__main__":
    status = initiate()
    while status == True:
        startProgram()
    else:
        exit()
