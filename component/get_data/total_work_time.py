from .spreadsheet_manager import open_spreadsheet
import pandas as pd

def get_total_work_time():
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

  all_employees = df_availability.index.tolist() # 全従業員のリスト
  dates = df_availability.columns[1:]
  total_work_time = {employee: 0 for employee in all_employees}

  return total_work_time

if __name__ == "__main__":
  total_work_time = get_total_work_time()
  print(f'total_work_time : {total_work_time}')