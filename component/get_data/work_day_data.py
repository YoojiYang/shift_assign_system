from .spreadsheet_manager import open_spreadsheet
import pandas as pd

def get_employees_by_condition(df, dates, condition):
  employees_by_condition = {}
  for date in dates:
      employees_by_condition[date] = df[df[date] == condition].index.tolist()
  return employees_by_condition


def get_spreadsheet_data():
  spreadsheet = open_spreadsheet()
  availability_sheet = spreadsheet.worksheet('出勤可否連絡シート')
  target_period_sheet = spreadsheet.worksheet('アサイン対象期間設定')
  
  availability_data = availability_sheet.get_all_values()
  df_availability = pd.DataFrame(availability_data)

  # アサイン対象期間の情報を取得
  start_day = target_period_sheet.cell(4, 2).value
  end_day = target_period_sheet.cell(4, 4).value
  target_period = {"start_day": start_day, "end_day": end_day}
  
  return df_availability, target_period


# 従業員ごとの出勤可否情報を取得する
def get_employees_availability():
  df_availability, target_period = get_spreadsheet_data()
  
  # 不要なデータをdfから削除する
  # 行を整える
  header_row = 6
  start_row = 7
  end_row = 99
  
  df_availability.columns = df_availability.iloc[header_row]
  df_availability = df_availability.iloc[start_row: end_row]
  
  # idをキーに設定
  df_availability = df_availability[df_availability['id'].notna() & (df_availability['id'] != '')]
  df_availability.set_index('id', inplace=True)
  
  # 列を整える
  start_day = target_period['start_day']
  end_day = target_period['end_day']
  cols = [col for col in df_availability.columns if start_day <= col <= end_day]
  df_availability = df_availability[cols]
  
  # 辞書の条件を設定
  available_terms = "〇"
  lateStart_terms = "18"
  leaveEarly_terms = "20"
  
  # work_days_indexの前までのすべての列名を取得
  dates = [col for col in df_availability.columns]

  # 辞書に従業員IDを割り当てる
  availability_employees = get_employees_by_condition(df_availability, dates, available_terms)
  late_start_employees = get_employees_by_condition(df_availability, dates, lateStart_terms)
  leave_early_employees = get_employees_by_condition(df_availability, dates, leaveEarly_terms)

  late_start_or_leave_early = {key: late_start_employees.get(key, []) + leave_early_employees.get(key, []) for key in late_start_employees}
  
  return availability_employees, late_start_or_leave_early


# 試合日ごとの試合開始時間と必要従業員数を取得
def get_game_days():
  df_game_days, target_period = get_spreadsheet_data()
  
  # 必要な列と行だけ取り出す
  header_row = 1
  df_game_days.columns = df_game_days.iloc[header_row]
  start_day = target_period['start_day']
  end_day = target_period['end_day']
  target_period_columns = [col for col in df_game_days.columns if start_day <= col <= end_day]
  df_game_days = df_game_days.loc[[3, 4], target_period_columns]
  
  # 必要情報を辞書に格納する
  keys = df_game_days.columns.values
  playballTime_values = df_game_days.iloc[0].values
  potentialAttendance_values = df_game_days.iloc[1].values
  # 辞書に格納
  game_days = {}
  for key, playballTime, potentialAttendance in zip(keys, playballTime_values, potentialAttendance_values):
      game_days[key] = {
          "playballTime": playballTime,
          "potentialAttendance": potentialAttendance
      }
      
  return game_days

# 1つの辞書にまとめる
def get_work_day_data():
  availability_employees, late_start_or_leave_early = get_employees_availability()
  game_days = get_game_days()
  
  work_day_data = {
      'availability_employees': availability_employees,
      'late_start_or_leave_early': late_start_or_leave_early,
      'game_days': game_days
  }
  
  return work_day_data

if __name__ == "__main__":
  work_day_data = get_work_day_data()
  print(f'availability_employees: {work_day_data["availability_employees"]}')
  print(f'late_start_or_leave_early: {work_day_data["late_start_or_leave_early"]}')
  print(f'game_days: {work_day_data["game_days"]}')