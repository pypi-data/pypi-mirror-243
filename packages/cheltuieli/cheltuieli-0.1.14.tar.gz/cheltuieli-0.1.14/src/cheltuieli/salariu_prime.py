import numpy as np
from datetime import datetime, timedelta
from mysqlquerys import connect, mysql_rm
import chelt_plan


class Income:
    def __init__(self, row, tableHead):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        ini_file = r"D:\Python\MySQL\database.ini"
        data_base_name = 'cheltuieli'
        incomeTable = mysql_rm.Table(ini_file, 'income')
        self.row = row
        self.tableHead = tableHead

    # def basic_salary(self):
    #     basic_salary = self.row[]

# def get_income(start_date, end_date):
#     ini_file = r"D:\Python\MySQL\database.ini"
#     data_base_name = 'cheltuieli'
#     # dataBase = connect.DataBase(ini_file, data_base_name)
#     incomeTable = connect.Table(ini_file, data_base_name, 'salariu')
#
#     incomeArr = np.atleast_2d(incomeTable.data)
#     print(incomeArr)
#     # cls = chelt_plan.CheltPlanificate(ini_file, data_base_name)
#     # # table_head, data = list(incomeTable[0]), incomeTable[1:]
#     # table_head = incomeTable.columnsNames
#     # # print('***', table_head)
#     # inter = cls.filter_dates(table_head, incomeArr, start_date.date(), end_date.date())
#     # for i in inter:
#     #     print(i)
#
# def main():
#     start_date = datetime(2022, 1, 1)
#     end_date = datetime(2022, 3, 31)
#     get_income(start_date, end_date)


if __name__ == '__main__':
    main()
