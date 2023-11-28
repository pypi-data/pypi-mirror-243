import chelt_plan
import masina
import salariu_prime
from mysqlquerys import connect, mysql_rm
from datetime import date
import time


def main():
    script_start_time = time.time()
    selectedStartDate = date(2023, 1, 1)
    selectedEndDate = date(2023, 1, 31)

    income_ini = r"D:\Python\MySQL\cheltuieli_db.ini"

    app = chelt_plan.CheltuieliPlanificate(income_ini)
    # all_chelt = app.get_all_sql_vals()
    # for i in all_chelt:
    #     print(i.table, i.name)
    # print('FINISH')
    # chelt_in_time_interval = app.filter_dates(all_chelt, selectedStartDate, selectedEndDate)
    # for i in chelt_in_time_interval:
    #     if i.table == 'income':
    #         print(i.table, i.name, i.value)
    # print('FINISH')
    # chelt_after_contofilter = app.filter_conto(chelt_in_time_interval, 'EC')
    # for i in chelt_in_time_interval:
    #     if i.table == 'income':
    #         print(i.table, i.name, i.value)
    # print('FINISH')
    # chelt_after_contofilter = app.filter_conto(chelt_in_time_interval, 'EC')
    # for i in chelt_in_time_interval:
    #     if i.table == 'income':
    #         print(i.table, i.name, i.value)
    # print('FINISH')
    # app.prepareTablePlan('all', selectedStartDate, selectedEndDate)
    # print(app.expenses)
    # print(app.tot_val_of_irregular_expenses())
    # print(app.tot_no_of_irregular_expenses())

    conf = connect.Config(income_ini)
    active_table = mysql_rm.Table(conf.credentials, 'income')
    vals = active_table.returnColumns(app.tableHead)
    all_incomes = []
    for row in vals:
        row = list(row)
        income = chelt_plan.Cheltuiala(row, app.tableHead)
        income.set_table('income')
        # print(row)
        all_incomes.append(income)
    # payments_in_interval = income.calculate_payments_in_interval(selectedStartDate, selectedEndDate)
    incomes_interval = []
    for inc in all_incomes:
        payments_in_interval = inc.calculate_payments_in_interval(selectedStartDate, selectedEndDate)
        if payments_in_interval:
            print(inc.name, inc.value, payments_in_interval)
            inc.payments_for_interval = payments_in_interval
            incomes_interval.append(inc)


    scrip_end_time = time.time()
    duration = scrip_end_time - script_start_time
    duration = time.strftime("%H:%M:%S", time.gmtime(duration))
    print('run time: {}'.format(duration))

if __name__ == '__main__':
    main()
