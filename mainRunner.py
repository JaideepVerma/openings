import AMZ
import jpmc
import swiggy
import ZS
import barclays
import adobe
import MS
import mastercard, visa

def safe_run(name, func):
    try:
        func()
        print(f"----- {name} Done -----")
    except Exception as e:
        print(f"ERROR in {name}: {e}")

def run_all():
    safe_run("AMZ", AMZ.main)
    safe_run("JPMC", jpmc.main)
    safe_run("Swiggy", swiggy.main)
    safe_run("ZS", ZS.main)
    safe_run("Barclays", barclays.main)
    safe_run("Adobe", adobe.main)
    safe_run("MS", MS.main)
    safe_run("MasterCard", mastercard.main)
    # safe_run("Visa", visa.main)

if __name__ == "__main__":
    run_all()

'''
def run_all():
    AMZ.main()
    print('----- AMZ Done -----')
    jpmc.main()
    print('----- JPMC Done -----')
    swiggy.main()
    print('----- Swiggy Done -----')
    ZS.main()
    print('----- ZS Done -----')
    barclays.main()
    print('----- Barclays Done -----')
    adobe.main()
    print('----- Adobe Done -----')
    MS.main()
    print('----- MS Done -----')
    mastercard.main()
    print('----- MasterCard Done -----')
    #visa.main()
    #print('----- Visa Done -----')
'''
