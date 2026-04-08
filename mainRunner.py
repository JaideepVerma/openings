import AMZ
import jpmc
import swiggy
import ZS

def run_all():
    AMZ.main()
    print('----- AMZ Done -----')
    jpmc.main()
    print('----- JPMC Done -----')
    swiggy.main()
    print('----- Swiggy Done -----')
    ZS.main()
    print('----- ZS Done -----')

if __name__ == "__main__":
    run_all()
