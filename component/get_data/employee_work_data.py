from .spreadsheet_manager import open_spreadsheet
import pandas as pd
import re

def get_employees_by_condition(df, dates, condition):
    employees_by_condition = {}
    for date in dates:
        employees_by_condition[date] = df[df[date] == condition].index.tolist()
    return employees_by_condition


def get_employees_availability():
    spreadsheet = open_spreadsheet()
    availability_sheet = spreadsheet.worksheet('出勤可否連絡シート')
    availability_data = availability_sheet.get_all_values()
    df_availability = pd.DataFrame(availability_data)
    df_availability.columns = df_availability.iloc[6]
    df_availability = df_availability.iloc[7:94]
    work_days_index = df_availability.columns.get_loc("work_days")
    df_availability = df_availability.iloc[:, :work_days_index+1]
    df_availability = df_availability.iloc[:, df_availability.columns != '']
    df_availability = df_availability[df_availability['id'].notna() & (df_availability['id'] != '')]
    df_availability.set_index('id', inplace=True)

    # 辞書の条件を設定
    available_terms = "〇"
    lateStart_terms = "18"
    leaveEarly_terms = "20"
    
    # work_days_indexの前までのすべての列名を取得
    dates = [col for col in df_availability.columns if re.match(r'\d{2}/\d{2}', col)]

    # 辞書に従業員IDを割り当てる
    availability_employees = get_employees_by_condition(df_availability, dates, available_terms)
    late_start_employees = get_employees_by_condition(df_availability, dates, lateStart_terms)
    leave_early_employees = get_employees_by_condition(df_availability, dates, leaveEarly_terms)

    late_start_or_leave_early = {key: late_start_employees.get(key, []) + leave_early_employees.get(key, []) for key in late_start_employees}
    late_start_or_leave_early.pop('work_days', None)
    
    return availability_employees, late_start_or_leave_early

if __name__ == "__main__":
    availability_employees, late_Start_or_leave_early = get_employees_availability()
    print("Availability Employees Data:", availability_employees)
    print("Late Start or leave early:", late_Start_or_leave_early)