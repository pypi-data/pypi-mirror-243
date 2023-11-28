import os.path
import traceback
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import sys
from mysqlquerys import connect
from mysqlquerys import mysql_rm

np.set_printoptions(linewidth=250)
__version__ = 'V5'


def calculate_last_day_of_month(mnth):
    if mnth < 12:
        lastDayOfMonth = datetime(datetime.now().year, mnth + 1, 1) - timedelta(days=1)
        lastDayOfMonth = lastDayOfMonth.day
    elif mnth == 12:
        lastDayOfMonth = 31
    return lastDayOfMonth


class Income:
    def __init__(self, row, tableHead):
        self.tableHead = tableHead
        self.id = None
        self.name = None
        self.conto = None
        self.value = None
        self.valid_from = None
        self.valid_to = None
        self.freq = None
        self.pay_day = None
        self.auto_ext = None
        self.table = None
        self.read_row(row)

    def read_row(self, row):
        idIndx = self.tableHead.index('id')
        nameIndx = self.tableHead.index('name')
        contoIndx = self.tableHead.index('myconto')
        valueIndx = self.tableHead.index('value')
        validFromIndx = self.tableHead.index('valid_from')
        validToIndx = self.tableHead.index('valid_to')
        freqIndx = self.tableHead.index('freq')
        payDayIndx = self.tableHead.index('pay_day')
        autoExtIndx = self.tableHead.index('auto_ext')
        self.id = row[idIndx]
        self.name = row[nameIndx]
        self.myconto = row[contoIndx]
        self.value = row[valueIndx]
        self.valid_from = row[validFromIndx]
        self.valid_to = row[validToIndx]
        self.freq = row[freqIndx]
        self.pay_day = row[payDayIndx]

        if self.pay_day is None:
            self.pay_day = calculate_last_day_of_month(self.valid_from.month)

        auto_ext = row[autoExtIndx]
        if auto_ext is None or auto_ext == 0:
            self.auto_ext = False
        else:
            self.auto_ext = True

    def calculate_income(self):
        base = 0
        plus = []
        minus = []
        for i, col in enumerate(self.tableHead):
            # print(i, col, self.row[i])
            if col == 'value':
                base = self.row[i]
            elif '%' in col and self.row[i] > 0:
                proc = self.row[i] / 100
                plus.append(proc)
            elif '%' in col and self.row[i] < 0:
                proc = self.row[i] / 100
                minus.append(proc)

        plus_val = 0
        for p in plus:
            val = p * base
            plus_val += val

        base_plus = base + plus_val
        # print('base_plus', base_plus)

        minus_val = 0
        for m in minus:
            val = m * base_plus
            minus_val += val
        final_value = base_plus + minus_val
        # print('base', base)
        # print('plus_val', plus_val)
        # print('minus_val', minus_val)
        # print('final_value', final_value)

        return final_value


class Cheltuiala:
    def __init__(self, row, tableHead):
        # print('#####', tableHead)
        self.tableHead = tableHead
        self.id = None
        self.name = None
        self.conto = None
        self.value = None
        self.valid_from = None
        self.valid_to = None
        self.freq = None
        self.pay_day = None
        # self.post_pay = None
        self.auto_ext = None
        self.table = None
        self.read_row(row)

    def read_row(self, row):
        # print(self.tableHead)
        # print(row)

        idIndx = self.tableHead.index('id')
        nameIndx = self.tableHead.index('name')
        contoIndx = self.tableHead.index('myconto')
        valueIndx = self.tableHead.index('value')
        validFromIndx = self.tableHead.index('valid_from')
        validToIndx = self.tableHead.index('valid_to')
        freqIndx = self.tableHead.index('freq')
        payDayIndx = self.tableHead.index('pay_day')
        # postPayIndx = self.tableHead.index('post_pay')
        autoExtIndx = self.tableHead.index('auto_ext')
        self.id = row[idIndx]
        self.name = row[nameIndx]
        self.myconto = row[contoIndx]
        self.value = row[valueIndx]
        self.valid_from = row[validFromIndx]
        self.valid_to = row[validToIndx]
        self.freq = row[freqIndx]
        self.pay_day = row[payDayIndx]

        if self.pay_day is None:
            self.pay_day = calculate_last_day_of_month(self.valid_from.month)
        # print('payday.....', self.pay_day)
        # sys.exit()
        # post_pay = row[postPayIndx]
        # if post_pay is None or post_pay == 0:
        #     self.post_pay = False
        # else:
        #     self.post_pay = True

        auto_ext = row[autoExtIndx]
        if auto_ext is None or auto_ext == 0:
            self.auto_ext = False
        else:
            self.auto_ext = True

    # @table.setter
    def set_table(self, table_name):
        self.table = table_name

    @property
    def first_payment(self):
        try:
            first_payment = datetime(self.valid_from.year, self.valid_from.month, self.pay_day)
        except:
            # print(self.id, self.table, self.name)
            # print(self.valid_from.year, self.valid_from.month, self.pay_day)
            # first_payment = calculate_last_day_of_month(selectedStartDate.month)
            first_payment = datetime(self.valid_from.year, self.valid_from.month, calculate_last_day_of_month(self.valid_from.month))
        return first_payment

    def list_of_payments_valid_from_till_selected_end_date(self, selectedEndDate):
        list_of_payments_till_selected_end_date = []
        if self.valid_from <= self.first_payment.date() <= selectedEndDate:
            list_of_payments_till_selected_end_date.append(self.first_payment)

        next_payment = self.first_payment + relativedelta(months=self.freq)
        if next_payment.day != self.pay_day:
            try:
                next_payment = datetime(next_payment.year, next_payment.month, self.pay_day)
            except:
                next_payment = datetime(next_payment.year, next_payment.month, calculate_last_day_of_month(next_payment.month))
        if self.valid_from <= next_payment.date() <= selectedEndDate:
            list_of_payments_till_selected_end_date.append(next_payment)

        while next_payment.date() <= selectedEndDate:
            next_payment = next_payment + relativedelta(months=self.freq)
            if next_payment.day != self.pay_day:
                try:
                    next_payment = datetime(next_payment.year, next_payment.month, self.pay_day)
                except:
                    next_payment = datetime(next_payment.year, next_payment.month,
                                            calculate_last_day_of_month(next_payment.month))
            if self.valid_from <= next_payment.date() <= selectedEndDate:
                list_of_payments_till_selected_end_date.append(next_payment)
        return list_of_payments_till_selected_end_date

    def cut_all_before_selectedStartDate(self, lista, selectedStartDate):
        new_list = []
        for date in lista:
            if date.date() >= selectedStartDate:
                new_list.append(date)
        return new_list

    def cut_all_after_valid_to(self, lista):
        new_list = []
        for date in lista:
            if date.date() <= self.valid_to:
                new_list.append(date)
        return new_list

    def calculate_payments_in_interval(self, selectedStartDate, selectedEndDate):
        list_of_payments_valid_from_till_selected_end_date = self.list_of_payments_valid_from_till_selected_end_date(selectedEndDate)
        # print(20*'*')
        # for i in list_of_payments_valid_from_till_selected_end_date:
        #     print(i)
        # print(20*'*')

        list_of_payments_selected_start_date_till_selected_end_date = self.cut_all_before_selectedStartDate(list_of_payments_valid_from_till_selected_end_date, selectedStartDate)
        # print(20*'*')
        # for i in list_of_payments_selected_start_date_till_selected_end_date:
        #     print(i)
        # print(20*'*')

        if self.valid_to and self.valid_to < selectedEndDate and not self.auto_ext:
            list_of_payments_selected_start_date_till_selected_end_date = self.cut_all_after_valid_to(list_of_payments_selected_start_date_till_selected_end_date)
            # print(20*'*')
            # for i in list_of_payments_selected_start_date_till_selected_end_date:
            #     print(i)
            # print(20*'*')

        return list_of_payments_selected_start_date_till_selected_end_date

    @property
    def first_payment_date(self):
        first_payment_date = datetime(self.valid_from.year, self.valid_from.month, self.pay_day)
        return first_payment_date

    @property
    def payments_for_interval(self):
        return self.pfi

    @payments_for_interval.setter
    def payments_for_interval(self, payments_days):
        self.pfi= payments_days


class CheltuieliPlanificate:
    def __init__(self, ini_file):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        self.ini_file = ini_file
        self.conf = connect.Config(self.ini_file)
        self.tableHead = ['id', 'name', 'value', 'myconto', 'freq', 'pay_day', 'valid_from', 'valid_to', 'auto_ext']
        self.myAccountsTable = self.sql_rm.Table(self.conf.credentials, 'banca')
        self.myContos = self.myAccountsTable.returnColumn('name')

        try:
            self.dataBase = self.sql_rm.DataBase(self.conf.credentials)
        except FileNotFoundError as err:
            iniFile, a = QFileDialog.getOpenFileName(None, 'Open data base configuration file', os.getcwd(), "data base config files (*.ini)")
            if os.path.exists(iniFile):
                self.dataBase = connect.DataBase(iniFile, self.data_base_name)
            # ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)
        except Exception as err:
            print(traceback.format_exc())

    @property
    def sql_rm(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        if self.conf.db_type == 'mysql':
            sql_rm = mysql_rm
        return sql_rm

    @property
    def default_interval(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        startDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        if datetime.now().month != 12:
            mnth = datetime.now().month + 1
            lastDayOfMonth = datetime(datetime.now().year, mnth, 1) - timedelta(days=1)
        else:
            lastDayOfMonth = datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)

        return startDate, lastDayOfMonth

    def get_monthly_interval(self, month:str):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        mnth = datetime.strptime(month, "%B").month
        startDate = datetime(datetime.now().year, mnth, 1)

        if mnth != 12:
            lastDayOfMonth = datetime(datetime.now().year, mnth + 1, 1) - timedelta(days=1)
        else:
            lastDayOfMonth = datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)

        return startDate, lastDayOfMonth

    def tot_no_of_irregular_expenses(self):
        indxMonthly = np.where(self.expenses[:,self.tableHead.index('freq')] != 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        return monthly.shape[0]

    def tot_val_of_irregular_expenses(self):
        indxMonthly = np.where(self.expenses[:,self.tableHead.index('freq')] != 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        if None in monthly:
            monthly = monthly[monthly != np.array(None)]
        totalMonthly = round(sum(monthly.astype(float)), 2)
        return totalMonthly

    def tot_no_of_monthly_expenses(self):
        indxMonthly = np.where(self.expenses[:,self.tableHead.index('freq')] == 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        return monthly.shape[0]

    def tot_val_of_monthly_expenses(self):
        indxMonthly = np.where(self.expenses[:,self.tableHead.index('freq')] == 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        if None in monthly:
            monthly = monthly[monthly != np.array(None)]
        totalMonthly = round(sum(monthly.astype(float)), 2)
        return totalMonthly

    def tot_no_of_expenses(self):
        allValues = self.expenses[:,self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        return len(allValues)

    def tot_val_of_expenses(self):
        allValues = self.expenses[:,self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalVal = round(sum(allValues.astype(float)), 2)
        return totalVal

    def tot_no_of_income(self):
        allValues = self.income[:,self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        return len(allValues)

    def tot_val_of_income(self):
        allValues = self.income[:,self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalVal = round(sum(allValues.astype(float)), 2)
        return totalVal

    def tot_no_of_expenses_income(self):
        allExpenses = self.expenses[:,self.tableHead.index('value')]
        allIncome = self.income[:,self.tableHead.index('value')]
        tot = len(allExpenses) + len(allIncome)
        return tot

    def tot_val_of_expenses_income(self):
        allValues = self.income[:,self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalIncome = round(sum(allValues.astype(float)), 2)
        allValues = self.expenses[:,self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalExpenses = round(sum(allValues.astype(float)), 2)
        return round(totalIncome + totalExpenses, 2)

    def get_all_sql_vals(self):
        print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        all_chelt = []
        for table in self.dataBase.allAvailableTablesInDatabase:
            active_table = self.sql_rm.Table(self.conf.credentials, table)
            active_table_head = active_table.columnsNames
            if 'table' in self.tableHead:
                self.tableHead.remove('table')
            if 'payDay' in self.tableHead:
                self.tableHead.remove('payDay')
            check = all(item in active_table_head for item in self.tableHead)
            if check:
                vals = active_table.returnColumns(self.tableHead)
                for row in vals:
                    row = list(row)
                    # if table == 'income':
                    #     chelt = Income(row, self.tableHead)
                    # else:
                    chelt = Cheltuiala(row, self.tableHead)
                    chelt.set_table(table)
                    all_chelt.append(chelt)
        return all_chelt

    def filter_dates(self, all_chelt, selectedStartDate, selectedEndDate):
        print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        remaining = []
        for chelt in all_chelt:
            # print(chelt.table, chelt.name, chelt.id, chelt.pay_day)
            payments_in_interval = chelt.calculate_payments_in_interval(selectedStartDate, selectedEndDate)
            # print(payments_in_interval)
            # if chelt.name == 'Steuererklärung_2022':
            #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, payments_in_interval)
            if isinstance(payments_in_interval, list):
                chelt.payments_for_interval = payments_in_interval
                # print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.payments_for_interval)
                if chelt.payments_for_interval:
                    remaining.append(chelt)
        return remaining

    def filter_conto(self, chelt_list, conto):
        print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        remaining = []
        for ch in chelt_list:
            if conto == 'all' and ch.table != 'intercontotrans':
                remaining.append(ch)
            elif ch.myconto == conto:
                remaining.append(ch)

        return remaining

    def split_expenses_income(self, chelt):
        print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        arr_expenses = []
        arr_income = []
        for ch in chelt:
            if ch.value == 0:
                continue
            for payment_day in ch.payments_for_interval:
                # if ch.value and ch.value > 0:
                #     incomeTable = self.sql_rm.Table(self.conf.credentials, ch.table)
                #     full_row = list(incomeTable.returnRowsWhere(('id', ch.id))[0])
                #     venit_instance = Income(full_row, incomeTable.columnsNames)
                #     ch.value = venit_instance.calculate_income()

                variables = vars(ch)
                row = [ch.table]
                for col in self.tableHead:
                    val = variables[col]
                    row.append(val)
                row.append(payment_day)
                if ch.value and ch.value > 0:
                    arr_income.append(row)
                else:
                    arr_expenses.append(row)
        arr_expenses = np.atleast_2d(arr_expenses)
        arr_income = np.atleast_2d(arr_income)
        self.tableHead.insert(0, 'table')
        self.tableHead.append('payDay')
        return arr_expenses, arr_income

    def prepareTablePlan(self, conto, selectedStartDate, selectedEndDate):
        print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))

        all_chelt = self.get_all_sql_vals()
        # for i in all_chelt:
        #     print(i.freq)
        # all_chelt = self.get_one_time_transactions(all_chelt)

        chelt_in_time_interval = self.filter_dates(all_chelt, selectedStartDate, selectedEndDate)
        # for chelt in chelt_in_time_interval:
        #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.conto, chelt.payments_for_interval)

        chelt_after_contofilter = self.filter_conto(chelt_in_time_interval, conto)
        # for chelt in chelt_after_contofilter:
        #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.conto, chelt.payments_for_interval)

        self.expenses, self.income = self.split_expenses_income(chelt_after_contofilter)
        if self.expenses.shape == (1, 0):
            expenses = np.empty((0, len(self.tableHead)))
        if self.income.shape == (1, 0):
            income = np.empty((0, len(self.tableHead)))
