import AMZ
import jpmc
import swiggy
import ZS
import barclays

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
    
if __name__ == "__main__":
    run_all()
