import AMZ
import jpmc
import swiggy
import ZS
import barclays
import adobe
import MS
import mastercard

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
    

if __name__ == "__main__":
    run_all()
