import logging 


class opts:
    port = 105
    dbg_flag = False
    log_type = logging.INFO
    def __init__(self,type):
        if type == 'debug':
            self.port = 106
            self.dbg_flag = True
            self.log_type = logging.DEBUG
