import sys
sys.path.append('/Users/yoojiyang/Desktop/dev/ESCON/esconShiftAsignProject/component')
import logging
logging.basicConfig(level=logging.INFO)

from get_data.employee_skills_data import get_employee_skills
from get_data.positions_data import get_positions_data
from get_data.employee_work_data import get_employees_availability
from get_data.game_days_data import get_game_days
from get_data.total_work_time import get_total_work_time

employee_skills = get_employee_skills()
positions_data = get_positions_data()
availability_employees, late_Start_or_leave_early = get_employees_availability()
game_days = get_game_days()
total_work_time = get_total_work_time()

# position_codeの上2桁とskillsの参照するインデックスを対応付ける辞書
position_skill_index_mapping = {
    "11": 1,
    "12": 5,
    "13": 9,
    "14": 9,
    "15": 13,
    "16": 17,
    "17": 21,
    "18": 23,
}

# 誰でもアサインできるが、優先的に選ぶ人が存在するポジション
# ２０２３年８/18時点では階段上とLounge受付
skip_additional_employee_positions = {
    "17",
    "18",
}


# アサイン可能な従業員のIDをリストアップする
def select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index, position_code):
    suitable_employees = []
    
    if position_code[2] == '1':
        for employee_id, skill in employee_skills.items():
            if employee_id in available_employees and skill[0] == '1' and skill[skill_index] == '1' and employee_id not in assigned_employees:
                suitable_employees.append((employee_id, int(skill[skill_index + 1])))
        
    else:
        for employee_id, skill in employee_skills.items():
            if employee_id in available_employees and skill[skill_index] == '1' and employee_id not in assigned_employees:
                suitable_employees.append((employee_id, int(skill[skill_index + 1])))
    
    logging.debug(f'select_suitale_employees : {position_code}, {suitable_employees}')
    return suitable_employees

# 条件に一致する従業員の中から、最も優先順位の高い従業員を選択する（勤務時間が少ない > スキルランクが高い）
def assign_best_employee(suitable_employees, assigned_employees, total_work_time):
    if suitable_employees:
        suitable_employees.sort(key=lambda x: (total_work_time[x[0]], x[1]))
        best_employee = suitable_employees[0][0]
        assigned_employees.add(best_employee)
        return best_employee
    return None

# =================================================================
# assign_employees_to_position関数から呼び出される
# =================================================================

# 特定ポジションへの割り当て処理
def assign_main_positions(position_code, available_employees, employee_skills, assigned_employees, total_work_time):
    # ポジションコードの上2桁を取得
    position_type = position_code[:2]
    # ポジションコードに対応するskillsの開始桁数を取得する
    skill_index = position_skill_index_mapping[position_type] # スキルインデックスを取得
    # 従業員をリストアップ
    suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index, position_code)
    # 従業員をアサイン
    return assign_best_employee(suitable_employees, assigned_employees, total_work_time)



# 特定ポジションへの割り当てが足りなかった時の処理
def assign_main_positions_additional_employee(position_code, available_employees, employee_skills, assigned_employees, total_work_time):

    # ポジションコードの上2桁を取得
    position_type = str(position_code)[:2]
    # ポジションコードに対応するskillsの開始桁数を取得する
    skill_index = position_skill_index_mapping[position_type] # スキルインデックスを取得
    suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index + 2, position_code)
    return assign_best_employee(suitable_employees, assigned_employees, total_work_time)


# スキルが関係ないポジションへの割り当て処理
def assign_sub_positions(available_employees, assigned_employees, total_work_time):
    suitable_employees = [
        employee_id for employee_id in available_employees
        if employee_id not in assigned_employees
    ]
    
    # total_work_timeの値が低い順にソート
    suitable_employees.sort(key=lambda employee_id: total_work_time[employee_id])

    if suitable_employees:
        best_employee = suitable_employees[0] # 最初の適切な従業員を選ぶ
        assigned_employees.add(best_employee)
        return best_employee





# =================================================================
# assign_employees関数から呼び出される
# =================================================================


# 次に割り当てを行う対象のポジションを取り出す
def get_position_codes(positions_data, now_position, now_game_playball):
    position_code = [position_code for _, position_code in positions_data[now_game_playball]['positions'].items()
                    if position_code[:3] == now_position
                    ]
    return position_code

# 指定されたポジションコードに従業員を割り当てて、必要な従業員の数を更新する
def assign_employee_to_position(position_code, available_employees, employee_skills, assigned_employees, now_position, required_employees, total_work_time):
    
    # 条件なしでアサインできるポジションに従業員をアサインする処理
    # 20238/18時点ではエントランスとスタンドが条件のないポジション
    if now_position[:2] not in position_skill_index_mapping:
        assigned_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
        logging.debug(f'from assign_sub_positions : {assigned_employee}')
    else:
        # その他のポジションは条件に従って、ベストな従業員をアサインする
        assigned_employee = assign_main_positions(position_code, available_employees, employee_skills, assigned_employees, total_work_time)
        logging.debug(f'from assign_main_positions : {assigned_employee}')
        if not assigned_employee:
            # 階段上か階段下の場合は誰でもOK
            if now_position[:2] in skip_additional_employee_positions: # skip_additional_employee_positions = "階段上" と "Lounge受付"
                assigned_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
                logging.debug(f'from skip_additional_employee_positions : {assigned_employee}')
            else:
                # メインポジションの人が足りなかった場合は、サブポジションの人を優先に割り当てる
                assigned_employee = assign_main_positions_additional_employee(position_code, available_employees, employee_skills, assigned_employees, total_work_time)
                logging.debug(f'from assign_additional_positions : {assigned_employee}')

    if assigned_employee:
        required_employees -= 1
    else:
        handle_assignment_error(position_code)
        return None, required_employees
    return assigned_employee, required_employees # assigned_employee = "この処理でアサインされた従業員のID"

# エラーメッセージをログに出力する
def handle_assignment_error(position_code):
    logging.error(f"Error: Could not assign employee for position_code: {position_code}")


# =================================================================
# メイン関数であるassign_employees_for_game_days関数から呼び出される
# =================================================================

# 従業員を条件に従ってアサインする関数
def assign_employees(positions_data, available_employees, positions_count, employee_skills, now_game_playball, total_work_time):
    assigned_employees = set() # 重複選択を防ぐためのリスト
    new_dict = {} # ポジションコードをキーとして、値にアサインされた従業員のIDが入る辞書
    
    # 割り当て順にポジションを並び替える（リーダー優先、その後はポジションコードの小さい順）
    sorted_positions_count = sorted(positions_count.items(), key=lambda x: (-int(x[0][2]), int(x[0][:2])))
    logging.debug(f'assign_employees sorted_positions_count : {sorted_positions_count}')

    # 各ポジションに必要な数だけ従業員を割り当てる
    for now_position, original_required_employees in sorted_positions_count: # now_position = 3桁の数値（上2桁=ポジションコード + 3桁目=リーダー情報）
        required_employees = int(original_required_employees)  # required_employees = "各ポジションごとの必要な従業員数"
        position_codes = get_position_codes(positions_data, now_position, now_game_playball) # now_positionに一致するポジションコードを取り出す
        
        # 必要な数に達するまで割り当て処理を繰り返す
        for position_code in position_codes:
            if required_employees <= 0: # 必要な従業員数が0になったら次のポジションへ
                break
            assigned_employee, required_employees = assign_employee_to_position(
                position_code, available_employees, employee_skills, assigned_employees, now_position, required_employees, total_work_time)
            if assigned_employee:
                new_dict[position_code] = assigned_employee # 従業員を割り当て
            else:
                new_dict[position_code] = None

    return new_dict, assigned_employees


# アサインされたリストをスプレッドシートに書き込む形に並び替える関数
def sort_new_dict(positions_data, new_dict, now_game_playball):
    sorted_new_dict = {}
    for key in sorted(positions_data[now_game_playball]['positions'].keys(), key=int):
        position_code = positions_data[now_game_playball]['positions'][key]
        sorted_new_dict[position_code] = new_dict[position_code]
    return sorted_new_dict



# =================================================================
# main.pyから呼び出されるメインの関数
# =================================================================
def assign_employees_for_game_days(game_days, positions_data, availability_employees, employee_skills, total_work_time):
    
    logging.info(f'assign_employees_for_game_days : start!')

    main_assignments = {}
    unassigned_employees_per_day = {}

    # game_daysのキー値の数だけ繰り返す
    for now_game_days, game_info in game_days.items():
        # now_game_daysに紐づくplayballTimeをnow_game_playballという変数にして管理する
        now_game_playball = game_info['playballTime']
        
        logging.info("---------------------------------------------------------------------------------------------------------")
        logging.info(f'assign_employees_for_game_days now_game_days: {now_game_days}')
        logging.debug(f'Playball Time is : {now_game_playball}')
        logging.info("---------------------------------------------------------------------------------------------------------")
        
        # その試合の出勤可能な従業員とポジションを設定する
        available_employees = availability_employees[now_game_days]
        positions_count = positions_data[now_game_playball]['counts']

        # 従業員のアサイン処理
        new_dict, assigned_employees = assign_employees(positions_data, available_employees, positions_count, employee_skills, now_game_playball, total_work_time)
        
        # 従業員の勤務時間を追跡
        for key, value in new_dict.items():
            if value is None: # 従業員がアサインされてない場合はスキップ
                continue
            work_time = int(key[5]) # キー値の6桁目の値を数値として取得
            total_work_time[value] += work_time
        logging.debug(f"{now_game_days} total_work_time :  {total_work_time}")
        
        # スプシに出力する順番に並び替える
        assigned_dict = sort_new_dict(positions_data, new_dict, now_game_playball)
        logging.debug(f' {now_game_days}のアサインリスト:{len(assigned_dict)}人 {assigned_dict}')

        # 結果をall_assignmentsに保存する
        main_assignments[now_game_days] = assigned_dict
        
        unassigned_employees = [employee for employee in available_employees if employee not in assigned_employees]
        unassigned_employees_per_day[now_game_days] = unassigned_employees # その日の未割り当て従業員を辞書に追加
        logging.debug(f' {now_game_days}で割り当てが漏れた人リスト:{len(unassigned_employees)}人 {unassigned_employees}')
        
    return main_assignments, unassigned_employees_per_day, total_work_time


# テスト実行用
if __name__ == "__main__":
    main_assignments, unassigned_employees_per_day, total_work_time = assign_employees_for_game_days(game_days, positions_data, availability_employees, employee_skills, total_work_time)
    
    logging.debug(f"main_assignments :  {main_assignments}")
    logging.debug(f"unassigned_employees_per_day :  {unassigned_employees_per_day}")
    logging.info(f"total_work_time :  {total_work_time}")
