from .spreadsheet_manager import open_spreadsheet
import pandas as pd
import numpy as np

# 勤務情報シート内でデータ取得に必要な範囲の開始列の列名
start_column_name = "id"

# 勤務情報シートから必要な情報をデータフレームとして取得
def get_df_work_history_data():
  spreadsheet = open_spreadsheet()
  work_history_master = spreadsheet.worksheet('勤務情報')
  work_history_data = work_history_master.get_all_values()
  df_work_history_data = pd.DataFrame(work_history_data)
  df_work_history_data.columns = df_work_history_data.iloc[1]
  
  # データ取得範囲の列の設定
  start_column_index = 17 # R列目 "id"列
  columns_array = df_work_history_data.columns.get_loc("----")
  end_column_index = np.where(columns_array)[0][0]

  # データ取得範囲の行の設定
  start_row_index = 2
  end_row_index = np.where(df_work_history_data[start_column_name] == "0")[0][0]
  
  # データ取得範囲を設定
  df_work_history_data = df_work_history_data.iloc[start_row_index: end_row_index, start_column_index: end_column_index]
  
  return df_work_history_data

# 従業員ごとに勤務情報を集計する
def calc_work_history_data(target_count, target):
  df_work_history_data = get_df_work_history_data()
  
  # 各行に対しての処理
  for _, row in df_work_history_data.iterrows():
    employee_code = row[start_column_name]
    total = 0  # 従業員の勤務データの合計
    
    if len(row) > 2:
      # 従業員コード以外の列（勤務データ）に対しての処理
      for work_data in row[2:]:
        # 上からtarget目の文字列を取り出し、数値に変換
        try:
          value = int(work_data[int(target)])
          total += value
        except (ValueError, IndexError):  # 文字列が数値でない、または短すぎる場合の例外処理
          continue
        
    target_count[employee_code] = total
    
  return target_count

# 従業員ごとにリーダーにアサインされた回数を集計する
def get_leader_count():
  leader_count = {}
  target = "2:3" # 勤務コードの3文字目を指定
  
  leader_count = calc_work_history_data(leader_count, target)
  
  return leader_count

# 従業員ごとの累積勤務時間を集計する
def get_total_work_time():
  total_work_time = {}
  target = "5:6" # 勤務コードの6文字目を指定

  total_work_time = calc_work_history_data(total_work_time, target)

  return total_work_time

# 従業員ごとのリーダーアサイン回数、累積勤務時間の情報を取得する
def get_work_history():
  leader_count = get_leader_count()
  total_work_time = get_total_work_time()
  
  return leader_count, total_work_time

if __name__ == "__main__":
  leader_count, total_work_time = get_work_history()
  print("leader_count: ", leader_count)
  print("total_work_time: ", total_work_time)
