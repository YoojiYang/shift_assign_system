from .spreadsheet_manager import open_spreadsheet
import pandas as pd
import numpy as np

def get_work_history_data():
  
  spreadsheet = open_spreadsheet()
  employee_master = spreadsheet.worksheet('勤務情報')
  employee_data = employee_master.get_all_values()
  df_employee = pd.DataFrame(employee_data)
  df_employee.columns = df_employee.iloc[1]
  
  # データ取得範囲の列の設定
  start_column_index = 17 # Q列目
  columns_array = df_employee.columns.get_loc("Sheet not found")
  end_column_index = np.where(columns_array)[0][0]

  # データ取得範囲の行の設定
  start_row_index = 2
  end_row_index = np.where(df_employee["従業員コード"] == "0")[0][0]
  
  # データ取得範囲を設定
  df_employee = df_employee.iloc[start_row_index: end_row_index, start_column_index: end_column_index]
  
  return df_employee

def get_leader_count():
  df_employee = get_work_history_data()
  
  leader_count = {}
  
  # 各行に対しての処理
  for _, row in df_employee.iterrows():
      employee_code = row["従業員コード"]
      total = 0  # 従業員の勤務データの合計
      
      if len(row) > 2:
        # 従業員コード以外の列（勤務データ）に対しての処理
        for work_data in row[2:]:
            # 上から3桁目の文字列を取り出し、数値に変換
            try:
                value = int(work_data[2:3])
                total += value
            except (ValueError, IndexError):  # 文字列が数値でない、または短すぎる場合の例外処理
                continue

      leader_count[employee_code] = total

  return leader_count

def get_total_work_time():
  df_employee = get_work_history_data()
  
  total_work_time = {}
  
  # 各行に対しての処理
  for _, row in df_employee.iterrows():
      employee_code = row["従業員コード"]
      total = 0  # 従業員の勤務データの合計
      
      if len(row) > 2:
        # 従業員コード以外の列（勤務データ）に対しての処理
        for work_data in row[2:]:
            # 上から6桁目の文字列を取り出し、数値に変換
            try:
                value = int(work_data[5:6])
                total += value
            except (ValueError, IndexError):  # 文字列が数値でない、または短すぎる場合の例外処理
                continue
      
      total_work_time[employee_code] = total

  return total_work_time

def get_work_history():
  leader_count = get_leader_count()
  total_work_time = get_total_work_time()
  
  return leader_count, total_work_time

if __name__ == "__main__":
  leader_count, total_work_time = get_work_history()
  print("leader_count: ", leader_count)
  print("total_work_time: ", total_work_time)
