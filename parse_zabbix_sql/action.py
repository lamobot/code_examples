import classes
import config

try:
    open(config.filename, "w").close()

    classes.Report.get_report('incoming_traffic') ### 2 ###
    classes.Report.get_report('hdd_size') ### 3 ###
    classes.Report.get_report('speed_reading')  ### 3.5 ###
    classes.Report.get_report('speed_writing') ### 3.6 ###
    classes.Report.get_report('using_hdd_size') ### 3.7 ###
    classes.Report.get_report('memory_used') ### 4 ###
    classes.Report.get_report('cpu_used') ### 5 ###

    print('The files have been created')

except TypeError:
    print('You have to put classes.py and config.py to directory where is action.py located')


