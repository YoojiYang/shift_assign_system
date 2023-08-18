from .spreadsheet_manager import open_spreadsheet
import pandas as pd

def get_game_days():
    spreadsheet = open_spreadsheet()

    # 特定のワークシートを開く
    availability_sheet = spreadsheet.worksheet('出勤可否連絡シート')
    availability_data = availability_sheet.get_all_values()
    df_game_days = pd.DataFrame(availability_data)
    df_game_days = df_game_days.iloc[:5, 3:]

    # キーとして使用する1行目の値を取得
    keys_row_index = 1 # キーが存在する行のインデックス
    keys = df_game_days.iloc[keys_row_index]

    # 値が存在する列だけを取得
    valid_columns = [col for col in df_game_days.columns if pd.notna(keys[col]) and keys[col] != '']

    # 必要な行と列だけを取得
    df_game_days = df_game_days.loc[[3, 4], valid_columns]
    
    # 3行目と4行目の値を取得
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

if __name__ == "__main__":
    game_days = get_game_days()
    print(game_days)