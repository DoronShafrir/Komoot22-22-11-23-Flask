import pandas as pd
from datetime import datetime as dt

class Comments:
    def __init__(self):
        self.main = pd.read_csv('main.csv')


    def fetch_comments(self):
        try:
            comments = pd.read_csv('comments.csv')

        # except IOError:

            init_line = ['Date','A_Comment', 'A_Duration', 'A_Distance']
            data = [['2023-12-16', 'Cycling with Mali to Kfar Gvirol and Mrar',0,0 ],
                    ['2018-06-01','buy new w Ghost',0,0],
                    ['2023-12-05','Replace rear tier',1,10.5],
                    ['2023-12-23', 'Arad Masada Tour', 4, 31]]
            comments = pd.DataFrame(data, columns=init_line)


            # line = pd.DataFrame([[date, additinal_comments, corrected_duration, corrected_distance]],columns=init_line)
            # comments = comments.append(line, ignore_index=True)
            print(comments.head(5))
            print(self.main.head(7))
            comments.to_csv('comments.csv')

        finally:
            print(comments.head(5))
            print(self.main.head(7))
            united = pd.merge(self.main, comments, on='Date', how='outer')
            united.to_csv('united.csv')

    @staticmethod
    def show_comments():
        try:
            comments = pd.read_csv("comments.csv")
            s_list = comments.sort_values(by="Date", ascending=False)
            data = []
            for n in range(len(s_list)):
                line = []
                line.append(str(s_list.Date.iloc[n])[:10])
                line.append(s_list.A_Comment.iloc[n])
                line.append(str(round((s_list.A_Duration.iloc[n]), 2)))
                line.append(str(round((s_list.A_Distance.iloc[n]), 2)))
                data.append(line)
        except IOError:
            raise Warning("comments.cse does not exist")

        return data




if __name__ == '__main__':
    get_comments = Comments()
    get_comments.fetch_comments()