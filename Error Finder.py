import pandas as pd
from openpyxl import load_workbook
# TODO travel without any work
timesheet = pd.read_csv("timesheet_report.csv")



# "username", "group", "local_date", "jobcode_1", "jobcode_2", "payroll item", "service item"
current_person = ""
current_phase = ""
current_job = ""
current_pay_type = ""
holidays = ['01/01/2020', '05/25/2020', '07/03/2020', '09/07/2020', '11/26/2020', '11/27/2020', '12/25/2020',
            '2020-01-01', '2020-05-25', '2020-07-03', '2020-09-07', '2020-11-26', '2020-11-27', '2020-12-25']
for index, (username, group, local_date, jobcode_1, jobcode_2, payroll_item, service_item) in \
        enumerate(zip(timesheet.loc[:, 'username'], timesheet.loc[:, 'group'], timesheet.loc[:, 'local_date'],
                      timesheet.loc[:, 'jobcode_1'], timesheet.loc[:, 'jobcode_2'], timesheet.loc[:, 'payroll item'],
                      timesheet.loc[:, 'service item'])):
    try:
        # Lunch Check
        if 'LUNCH' == jobcode_1:
            continue

        # New person check
        if username != current_person:
            current_person = username
            i = 1
            while 'LUNCH' in timesheet.loc[index + i, 'jobcode_1']:
                i += 1
            if 'Salary' in timesheet.loc[index + i, 'payroll item']:
                current_pay_type = 'Salary'
            elif 'Hourly' in timesheet.loc[index + i, 'payroll item']:
                current_pay_type = 'Hourly'

        if 'Other' in payroll_item or 'Holiday' in payroll_item or 'PTO' in payroll_item:
            if 'SAV Digital Environments, Inc MT' not in jobcode_1 or 'Overhead' not in jobcode_2:
                print(f"SAV overhead Error: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                      f"{payroll_item}, {service_item}")
            if 'LABOR:Office/Meetings' != service_item and 'LABOR:Training' != service_item and \
                    'LABOR:Ops/Admin/Sales' != service_item:
                print(f"Payroll not Other Error: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                      f"{payroll_item}, {service_item}")
        # TODO make last section more robust/ add reverse clause/ iff vs if
        # phase match
        elif ('Travel Time' not in service_item) and (('Rough' in payroll_item and 'Rough' not in service_item) or
                                                      ('Rough' not in payroll_item and 'Rough' in service_item) or
                                                      ('Finish' in payroll_item and 'Finish' not in service_item and
                                                       'Programming' not in service_item) or
                                                      ('Finish' not in payroll_item and 'Finish' in service_item) or
                                                      ('Security' in payroll_item and 'Security' not in service_item) or
                                                      ('Security' not in payroll_item and 'Security' in service_item)):
            print(f"Phase Error: {username}, {local_date}, {jobcode_1}:{jobcode_2}, {payroll_item}, {service_item}")

        if not (service_item == "LABOR:Finish:Base" or service_item == "LABOR:Rough-in:Base" or
                service_item == "LABOR:Security Finish:Base" or service_item == "LABOR:Security Rough:Base" or
                service_item == "LABOR:Finish:Design" or service_item == "LABOR:Rough-in:Design" or
                service_item == "LABOR:Security Finish:Design" or service_item == "LABOR:Security Rough:Design" or
                service_item == "LABOR:Finish:Management" or service_item == "LABOR:Rough-in:Management" or
                service_item == "LABOR:Security Finish:Management" or
                service_item == "LABOR:Security Rough:Management" or
                service_item == "LABOR:Office/Meetings" or service_item == "LABOR:Travel Time" or
                service_item == "LABOR:Ops/Admin/Sales" or service_item == "LABOR:Training" or
                service_item == "LABOR:Programming:Base"):
            print(f"Bad Service Item Error: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                  f"{payroll_item}, {service_item}")

        if 'Travel Time' in service_item and current_job == (str(jobcode_1) + ':' + str(jobcode_2)) and \
                current_phase not in payroll_item:
            print(
                f"Travel Phase Error: {username}, {local_date}, {jobcode_1}:{jobcode_2}, {payroll_item}, {service_item}")

        if current_pay_type not in payroll_item:
            print(f"Pay Type Error: {username}, {local_date}, {jobcode_1}:{jobcode_2}, {payroll_item}, {service_item}")

        if 'Holiday' in payroll_item:
            holiday_check = False
            for day in holidays:
                if day in local_date:
                    holiday_check = True
            if holiday_check is False:
                print(f"Not a Holiday Error: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                      f"{payroll_item}, {service_item}")

        if 'Salary' in payroll_item:
            current_pay_type = 'Salary'
        elif 'Hourly' in payroll_item:
            current_pay_type = 'Hourly'
        current_job = str(jobcode_1) + ':' + str(jobcode_2)

    except TypeError:
        print(f"TypeError: {username}, {local_date}, {jobcode_1}:{jobcode_2}, {payroll_item}, {service_item}")

a = input("Press Enter to Exit.")