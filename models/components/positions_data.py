from collections import defaultdict
import pandas as pd



# シフト表マスタのデータを取得
def get_work_code9_by_start_time(spreadsheet, sheet_name):
    position_master = spreadsheet.worksheet(sheet_name['position_master'])
    position_data = position_master.get_all_values()
    df_position = pd.DataFrame(position_data)
    
    # データ取得対象の列
    index_col = 0
    work_code9_col = 42
    
    # 13時試合開始のデータ取得範囲
    startRow_13 = 10
    endRow_13 = 40
    # 14時試合開始のデータ取得範囲
    startRow_14 = 50
    endRow_14 = 80
    # 18時試合開始のデータ取得範囲
    startRow_18 = 100
    endRow_18 = 130

    # データフレームから試合開始時間別のポジション情報を取得
    def create_work_code9_dict(start_row, end_row):
        df_filtered = df_position.iloc[start_row:end_row, [index_col, work_code9_col]]
        # 空文字列の値を持つ行を除外
        df_filtered = df_filtered[df_filtered[work_code9_col] != '']
        return df_filtered.set_index(index_col).to_dict()[work_code9_col]
    
    # 辞書を作成
    work_code9_list_13 = create_work_code9_dict(startRow_13, endRow_13)
    work_code9_list_14 = create_work_code9_dict(startRow_14, endRow_14)
    work_code9_list_18 = create_work_code9_dict(startRow_18, endRow_18)
    
    return work_code9_list_13, work_code9_list_14, work_code9_list_18

# 各ポジションの必要人数を計算する処理
def get_position_code3_counts(work_code9_list):
    position_code3_counts = defaultdict(int)
    for code in work_code9_list.values():
        position_type = str(code)[:3]
        if position_type:
            position_code3_counts[position_type] += 1
    return dict(position_code3_counts)

# 試合開始時間別のポジション情報を取得
def get_positions_data(spreadsheet, sheet_name):
    work_code9_list_13, work_code9_list_14, work_code9_list_18 = get_work_code9_by_start_time(spreadsheet, sheet_name)

    position_code3_counts_13 = get_position_code3_counts(work_code9_list_13)
    position_code3_counts_14 = get_position_code3_counts(work_code9_list_14)
    position_code3_counts_18 = get_position_code3_counts(work_code9_list_18)

    positions_data = {
        '13:00': {'work_code9_list': work_code9_list_13, 'position_code3_counts': position_code3_counts_13},
        '14:00': {'work_code9_list': work_code9_list_14, 'position_code3_counts': position_code3_counts_14},
        '18:00': {'work_code9_list': work_code9_list_18, 'position_code3_counts': position_code3_counts_18},
    }
    
    return positions_data

# if __name__ == "__main__":
#     positions_data = get_positions_data(spreadsheet, sheet_name)
#     print(f'13:00のポジション一覧 : {positions_data["13:00"]["work_code9_list"]}')
#     print(f'13:00のポジション内訳 : {positions_data["13:00"]["position_code3_counts"]}')
#     print(f'14:00のポジション数 : {len(positions_data["14:00"]["work_code9_list"])}')
#     print(f'14:00のポジション内訳 : {positions_data["14:00"]["position_code3_counts"]}')
#     print(f'18:00のポジション数 : {len(positions_data["18:00"]["work_code9_list"])}')
#     print(f'18:00のポジション内訳 : {positions_data["18:00"]["position_code3_counts"]}')
