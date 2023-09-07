import logging
logging.basicConfig(level=logging.INFO)

from models import (
    get_employee_skills,
    get_positions_data,
    must_have_skills_positions,
    get_work_history,
)

from services.for_single_day import (
    assign_sub_positions,
    assign_main_positions,
    handle_assignment_error,
    assign_main_positions_additional_employee,
)



# 関数の中身を展開
employee_skills = get_employee_skills()
positions_data = get_positions_data()
leader_count, total_work_time = get_work_history()


# =================================================================
# create_single_day_list関数から呼び出される
# =================================================================


# 次に割り当てを行う対象のポジションを取り出す
def get_target_work_code7_list(current_position_code3, current_game_time):
    position_code = [position_code for _, position_code in positions_data[current_game_time]['work_code7_list'].items()
                    if position_code[:3] == current_position_code3
                    ]
    return position_code

# アサインされたリストをスプレッドシートに書き込む形に並び替える関数
def sort_current_day_dict(new_dict, current_game_time):
    sorted_new_dict = {}
    for key in sorted(positions_data[current_game_time]['positions'].keys(), key=int):
        position_code = positions_data[current_game_time]['positions'][key]
        sorted_new_dict[position_code] = new_dict[position_code]
    return sorted_new_dict

# =================================================================
# メイン関数であるcreate_single_day_list_for_game_days関数から呼び出される
# =================================================================

# 従業員を条件に従ってアサインする関数
def create_single_day_list(available_employees, positions_count, current_game_time):
    # この関数が返すリストを初期化
    current_day_dict = {} # ポジションコードをキーとして、値にアサインされた従業員のIDが入る辞書
    assigned_employees = set() # 重複選択を防ぐためのリスト
    
    # 3桁のポジションコードを割り当て順に並び替える（リーダー優先、その後はポジションコードの小さい順）
    sorted_positions_code3 = sorted(positions_count.items(), key=lambda x: (-int(x[0][2]), int(x[0][:2])))

    # 3桁のポジションコードの数だけ以下の処理を繰り返す
    for current_position_code3, original_required_count in sorted_positions_code3:
        # 現在のポジションに必要な従業員数を取得する
        required_count = int(original_required_count)
        
        target_work_code7_list = get_target_work_code7_list(current_position_code3, current_game_time) # current_position_code3に一致するポジションコードを取り出す
        
        # ポジションごとの必要な人数の数だけ以下の処理を繰り返す
        for current_target_work_code7 in target_work_code7_list:
            if required_count <= 0: # 必要な従業員数が0になったら次のポジションへ
                break
            best_employee, required_count = get_best_employee(current_target_work_code7, available_employees, assigned_employees, current_position_code3, required_count, total_work_time, leader_count)
            if best_employee:
                current_day_dict[current_target_work_code7] = best_employee
                # アサインするポジションがリーダーの場合、leader_countを+1する
                if current_position_code3[2] == '1':
                    
                    logging.info(f'current_position_code3 : {current_position_code3}')
                    logging.info(f'assigned_leader : {best_employee}')
                    leader_count[best_employee] += 1
                    logging.info(f'leader_count : {leader_count[best_employee]}')

            else:
                current_day_dict[current_target_work_code7] = None

    return current_day_dict, assigned_employees

