import logging 
import logging.config

def setlogger(filename,level=logging.INFO):
    logging.basicConfig(filename=f"/var/log/restadmin/{filename}.log",filemode='w',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=level)
    return logging.getLogger(f"{filename}")
