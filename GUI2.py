from  Komoot_Ana3 import K_Analize
from datetime import datetime as dt
from datetime import timedelta


class GUI2():
    def __init__(self):
        typed_date = "01/01/2023"
        date = dt.strptime(typed_date, "%d/%m/%Y")
        self.start_date = date.strftime("%m/%d/%Y")
        self.conf = [self.start_date, 1, 0,0,0,1]
        self.data = self.get_data(self.conf)

    def get_data(self, conf):
        run_k = K_Analize("no_need", conf)
        run_k.fill_data()
        data = run_k.data
        return data
