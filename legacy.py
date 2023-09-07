# import sys
# sys.path.append('/Users/yoojiyang/Desktop/dev/ESCON/esconShiftAsignProject/component')
# import logging
# logging.basicConfig(level=logging.INFO)

# from get_data.positions_details import positions_details, must_have_skills_positions
# from get_data.employee_skills_data import get_employee_skills
# from get_data.positions_data import get_positions_data
# from get_data.work_history_data import get_work_history
# from get_data.work_day_data import get_work_day_data

# # 関数の中身を展開
# employee_skills = get_employee_skills()
# positions_data = get_positions_data()
# leader_count, total_work_time = get_work_history()
# work_day_data = get_work_day_data()

# # work_day_dataの中身を展開
# availability_employees = work_day_data["availability_data"]["availability"]
# late_start_employees = work_day_data["availability_data"]["late_start"]
# leave_early_employees = work_day_data["availability_data"]["leave_early"]
# game_days_data = work_day_data["game_days_data"]


# # =================================================================
# # select_suitable_employees関数から呼び出される
# # =================================================================

# # 特定ポジションにアサインできる条件の設定
# def is_suitable_employee(employee_id, skill, available_employees, assigned_employees, skill_index):
#     has_required_skill = skill[skill_index] == '1'
#     is_available = employee_id in available_employees
#     is_not_assigned = employee_id not in assigned_employees
#     return has_required_skill and is_available and is_not_assigned

# # =================================================================
# # リーダーを選ぶ条件
# # =================================================================

# # skillsの1桁目が1である
# def is_suitable_leader(skill):
#     is_leader = skill[0] == '1'
#     return is_leader

# # リーダー候補者を、リーダーへのアサイン回数が少ない順に並べる
# def get_min_leader_count(suitable_employees, leader_count):
#     return min(leader_count[employee[0]] for employee in suitable_employees)

# # リーダー候補者を、リーダーへのアサイン回数が最も少ない人だけに絞る
# def filter_by_min_leader_count(suitable_employees, leader_count):
#     min_leader_count = get_min_leader_count(suitable_employees, leader_count)
#     return [employee for employee in suitable_employees if leader_count[employee[0]] == min_leader_count]

# # リーダーを選ぶ処理を行う関数
# def select_suitable_leader(suitable_employees, leader_count, available_employees, assigned_employees, skill_index):
#     for employee_id, skill in employee_skills.items():
#         if is_suitable_leader(skill) and is_suitable_employee(employee_id, skill, available_employees, assigned_employees, skill_index):
#             suitable_employees.append((employee_id, int(skill[skill_index + 1])))

#     suitable_employees.sort(key=lambda x: (leader_count[x[0]], x[1]))
#     return suitable_employees


# # =================================================================
# # assign_xxxxxx_position関数から呼び出される
# # =================================================================

# # 従業員をポジションにアサインする
# def select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index, position_code, leader_count):
#     suitable_employees = []
#     # リーダーポジションの場合
#     if position_code[2] == '1':
#         select_suitable_leader(suitable_employees, leader_count, available_employees, assigned_employees, skill_index)
#     # リーダー以外のポジションの場合
#     else:
#         for employee_id, skill in employee_skills.items():
#             if is_suitable_employee(employee_id, skill, available_employees, assigned_employees, skill_index):
#                 suitable_employees.append((employee_id, int(skill[skill_index + 1])))
#     return suitable_employees

# # 条件に一致する従業員の中から、最も優先順位の高い従業員を選択する（勤務時間が少ない > スキルランクが高い）
# def assign_best_employee(suitable_employees, assigned_employees, total_work_time):
#     if suitable_employees:
#         suitable_employees.sort(key=lambda x: (total_work_time[x[0]], x[1]))
#         best_employee = suitable_employees[0][0]
#         assigned_employees.add(best_employee)
#         return best_employee
#     return None

# # =================================================================
# # assign_employees_to_position関数から呼び出される
# # =================================================================

# # 特定ポジションへの割り当て処理
# def assign_main_positions(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count):
#     # ポジションコードの上2桁を取得
#     # position_type = position_code[:2]
#     # ポジションコードに対応するskillsの開始桁数を取得する
#     skill_index = positions_details[position_code[:2]]['skills_index'] # スキルインデックスを取得
#     # 従業員をリストアップ
#     suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index, position_code, leader_count)
#     # 従業員をアサイン
#     return assign_best_employee(suitable_employees, assigned_employees, total_work_time)



# # 特定ポジションへの割り当てが足りなかった時の処理
# def assign_main_positions_additional_employee(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count):

#     # ポジションコードの上2桁を取得
#     position_type = str(position_code)[:2]
#     # ポジションコードに対応するskillsの開始桁数を取得する
#     skill_index = positions_details[position_type]['skills_index'] # スキルインデックスを取得
#     suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index + 2, position_code, leader_count)
#     return assign_best_employee(suitable_employees, assigned_employees, total_work_time)


# # スキルが関係ないポジションへの割り当て処理
# def assign_sub_positions(available_employees, assigned_employees, total_work_time):
#     suitable_employees = [
#         employee_id for employee_id in available_employees
#         if employee_id not in assigned_employees
#     ]
    
#     # total_work_timeの値が低い順にソート
#     suitable_employees.sort(key=lambda employee_id: total_work_time[employee_id])

#     if suitable_employees:
#         best_employee = suitable_employees[0] # 最初の適切な従業員を選ぶ
#         assigned_employees.add(best_employee)
#         return best_employee





# # =================================================================
# # assign_employees関数から呼び出される
# # =================================================================


# # 次に割り当てを行う対象のポジションを取り出す
# def get_position_codes(positions_data, current_position, current_game_time):
#     position_code = [position_code for _, position_code in positions_data[current_game_time]['positions'].items()
#                     if position_code[:3] == current_position
#                     ]
#     return position_code

# # 指定されたポジションコードに従業員を割り当てて、必要な従業員の数を更新する
# def assign_employee_to_position(position_code, available_employees, employee_skills, assigned_employees, current_position, required_employees, total_work_time, leader_count):
    
#     # 条件なしでアサインできるポジションに従業員をアサインする処理
#     # 20238/18時点ではエントランスとスタンドが条件のないポジション
#     if current_position[:2] not in must_have_skills_positions:
#         assigned_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
#         logging.debug(f'from assign_sub_positions : {assigned_employee}')
#     else:
#         # その他のポジションは条件に従って、ベストな従業員をアサインする
#         assigned_employee = assign_main_positions(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count)
#         logging.debug(f'from assign_main_positions : {assigned_employee}')
#         if not assigned_employee:
#             # 階段上か階段下の場合は誰でもOK
#             if current_position[:2] not in must_have_skills_positions: # skip_additional_employee_positions = "階段上" と "Lounge受付"
#                 assigned_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
#                 logging.debug(f'from skip_additional_employee_positions : {assigned_employee}')
#             else:
#                 # メインポジションの人が足りなかった場合は、サブポジションの人を優先に割り当てる
#                 assigned_employee = assign_main_positions_additional_employee(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count)
#                 logging.debug(f'from assign_additional_positions : {assigned_employee}')

#     if assigned_employee:
#         required_employees -= 1
#     else:
#         handle_assignment_error(position_code)
#         return None, required_employees
#     return assigned_employee, required_employees # assigned_employee = "この処理でアサインされた従業員のID"

# # エラーメッセージをログに出力する
# def handle_assignment_error(position_code):
#     logging.error(f"Error: Could not assign employee for position_code: {position_code}")


# # =================================================================
# # メイン関数であるassign_employees_for_game_days関数から呼び出される
# # =================================================================

# # 従業員を条件に従ってアサインする関数
# def assign_employees(positions_data, available_employees, positions_count, employee_skills, current_game_time, total_work_time, leader_count):
#     assigned_employees = set() # 重複選択を防ぐためのリスト
#     new_dict = {} # ポジションコードをキーとして、値にアサインされた従業員のIDが入る辞書
    
#     # 割り当て順にポジションを並び替える（リーダー優先、その後はポジションコードの小さい順）
#     sorted_positions_count = sorted(positions_count.items(), key=lambda x: (-int(x[0][2]), int(x[0][:2])))
#     logging.debug(f'assign_employees sorted_positions_count : {sorted_positions_count}')

#     # 各ポジションに必要な数だけ従業員を割り当てる
#     for current_position, original_required_employees in sorted_positions_count: # current_position = 3桁の数値（上2桁=ポジションコード + 3桁目=リーダー情報）
#         required_employees = int(original_required_employees)  # required_employees = "各ポジションごとの必要な従業員数"
#         position_codes = get_position_codes(positions_data, current_position, current_game_time) # current_positionに一致するポジションコードを取り出す
        
#         # 必要な数に達するまで割り当て処理を繰り返す
#         for position_code in position_codes:
#             if required_employees <= 0: # 必要な従業員数が0になったら次のポジションへ
#                 break
#             assigned_employee, required_employees = assign_employee_to_position(
#                 position_code, available_employees, employee_skills, assigned_employees, current_position, required_employees, total_work_time, leader_count)
#             if assigned_employee:
#                 new_dict[position_code] = assigned_employee # 従業員を割り当て
#                 # アサインするポジションがリーダーの場合、leader_countを+1する
#                 if current_position[2] == '1':
                    
#                     logging.info(f'current_position : {current_position}')
#                     logging.info(f'assigned_leader : {assigned_employee}')
#                     leader_count[assigned_employee] += 1
#                     logging.info(f'leader_count : {leader_count[assigned_employee]}')

#             else:
#                 new_dict[position_code] = None

#     return new_dict, assigned_employees


# # アサインされたリストをスプレッドシートに書き込む形に並び替える関数
# def sort_new_dict(positions_data, new_dict, current_game_time):
#     sorted_new_dict = {}
#     for key in sorted(positions_data[current_game_time]['positions'].keys(), key=int):
#         position_code = positions_data[current_game_time]['positions'][key]
#         sorted_new_dict[position_code] = new_dict[position_code]
#     return sorted_new_dict



# # =================================================================
# # main.pyから呼び出されるメインの関数
# # =================================================================
# def assign_employees_for_game_days(work_day_data, positions_data, employee_skills, total_work_time):
    
#     logging.info(f'assign_employees_for_game_days : start!')

#     main_assignments = {}
#     unassigned_employees_per_day = {}

#     # game_daysのキー値の数だけ繰り返す
#     for current_game_day, game_info in work_day_data['game_days'].items():
#         # current_game_dayに紐づくplayballTimeをcurrent_game_timeという変数にして管理する
#         current_game_time = game_info['playballTime']
        
#         logging.info("---------------------------------------------------------------------------------------------------------")
#         logging.info(f'current_game_day: {current_game_day}')
#         logging.info(f'leader_count: {leader_count}')
#         logging.info(f'total_work_time: {total_work_time}')
#         logging.debug(f'Playball Time is : {current_game_time}')
#         logging.info("---------------------------------------------------------------------------------------------------------")
        
#         # その試合の出勤可能な従業員とポジションを設定する
#         available_employees = work_day_data['availability_employees'][current_game_day]
#         positions_count = positions_data[current_game_time]['counts']
#         print(f'positions_count{positions_count}')

#         # 従業員のアサイン処理
#         new_dict, assigned_employees = assign_employees(positions_data, available_employees, positions_count, employee_skills, current_game_time, total_work_time, leader_count)
        
#         # 従業員の勤務時間を追跡
#         for key, value in new_dict.items():
#             if value is None: # 従業員がアサインされてない場合はスキップ
#                 continue
#             work_time = int(key[5]) # キー値の6桁目の値を数値として取得
#             total_work_time[value] += work_time
#         logging.debug(f"{current_game_day} total_work_time :  {total_work_time}")
        
#         # スプシに出力する順番に並び替える
#         assigned_dict = sort_new_dict(positions_data, new_dict, current_game_time)
#         logging.debug(f' {current_game_day}のアサインリスト:{len(assigned_dict)}人 {assigned_dict}')

#         # 結果をall_assignmentsに保存する
#         main_assignments[current_game_day] = assigned_dict
        
#         unassigned_employees = [employee for employee in available_employees if employee not in assigned_employees]
#         unassigned_employees_per_day[current_game_day] = unassigned_employees # その日の未割り当て従業員を辞書に追加
#         logging.debug(f' {current_game_day}で割り当てが漏れた人リスト:{len(unassigned_employees)}人 {unassigned_employees}')
        
#     return main_assignments, unassigned_employees_per_day, total_work_time


# # テスト実行用
# if __name__ == "__main__":
#     main_assignments, unassigned_employees_per_day, total_work_time = assign_employees_for_game_days(work_day_data, positions_data, employee_skills, total_work_time)
    
#     logging.debug(f"main_assignments :  {main_assignments}")
#     logging.debug(f"unassigned_employees_per_day :  {unassigned_employees_per_day}")
#     logging.info(f"total_work_time :  {total_work_time}")
