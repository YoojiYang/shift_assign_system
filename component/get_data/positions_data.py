from .spreadsheet_manager import open_spreadsheet
from collections import defaultdict
import pandas as pd

# 各ポジションの必要人数を計算する処理
def get_position_counts(position_list):
    position_counts = defaultdict(int)
    for code in position_list.values():
        position_type = str(code)[:3]
        position_counts[position_type] += 1
    return dict(position_counts)


# シフト表マスタのデータを取得
def get_positions_by_start_time():
    spreadsheet = open_spreadsheet()
    position_master = spreadsheet.worksheet('シフト表マスタ')
    position_data = position_master.get_all_values()
    df_position = pd.DataFrame(position_data)
    df_position = df_position.iloc[:, :9]
    
    # 13時試合開始のデータ取得範囲
    startRow_13 = 10
    endRow_13 = 40
    # 14時試合開始のデータ取得範囲
    startRow_14 = 50
    endRow_14 = 80
    # 18時試合開始のデータ取得範囲
    startRow_18 = 100
    endRow_18 = 130
    
    positionlist_13 = df_position.iloc[startRow_13 : endRow_13, [0, 7]].set_index(0).to_dict()[7]
    positionlist_14 = df_position.iloc[startRow_14 : endRow_14, [0, 7]].set_index(0).to_dict()[7]
    positionlist_18 = df_position.iloc[startRow_18 : endRow_18, [0, 7]].set_index(0).to_dict()[7]
    
    return positionlist_13, positionlist_14, positionlist_18


def get_positions_data():
    positionlist_13, positionlist_14, positionlist_18 = get_positions_by_start_time()

    position_counts_13 = get_position_counts(positionlist_13)
    position_counts_14 = get_position_counts(positionlist_14)
    position_counts_18 = get_position_counts(positionlist_18)
    
    positions_data = {
        '13:00': {'positions': positionlist_13, 'counts': position_counts_13},
        '14:00': {'positions': positionlist_14, 'counts': position_counts_14},
        '18:00': {'positions': positionlist_18, 'counts': position_counts_18},
    }
    
    return positions_data



if __name__ == "__main__":
    position_data = get_positions_data()
    print(f'13:00のポジション数 : {len(position_data["13:00"]["positions"])}')
    print(f'13:00のポジション内訳 : {position_data["13:00"]["counts"]}')
    print(f'14:00のポジション数 : {len(position_data["14:00"]["positions"])}')
    print(f'14:00のポジション内訳 : {position_data["14:00"]["counts"]}')
    print(f'18:00のポジション数 : {len(position_data["18:00"]["positions"])}')
    print(f'18:00のポジション内訳 : {position_data["18:00"]["counts"]}')
