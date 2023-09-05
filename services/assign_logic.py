
# =================================================================
# assign_employees関数から呼び出される
# =================================================================


# 次に割り当てを行う対象のポジションを取り出す
def get_position_codes(positions_data, current_position, current_game_time):
    position_code = [position_code for _, position_code in positions_data[current_game_time]['positions'].items()
                    if position_code[:3] == current_position
                    ]
    return position_code

# 指定されたポジションコードに従業員を割り当てて、必要な従業員の数を更新する
def assign_employee_to_position(position_code, available_employees, employee_skills, assigned_employees, current_position, required_employees, total_work_time, leader_count):
    
    # 条件なしでアサインできるポジションに従業員をアサインする処理
    # 20238/18時点ではエントランスとスタンドが条件のないポジション
    if current_position[:2] not in must_have_skills_positions:
        assigned_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
        logging.debug(f'from assign_sub_positions : {assigned_employee}')
    else:
        # その他のポジションは条件に従って、ベストな従業員をアサインする
        assigned_employee = assign_main_positions(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count)
        logging.debug(f'from assign_main_positions : {assigned_employee}')
        if not assigned_employee:
            # 階段上か階段下の場合は誰でもOK
            if current_position[:2] not in must_have_skills_positions: # skip_additional_employee_positions = "階段上" と "Lounge受付"
                assigned_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
                logging.debug(f'from skip_additional_employee_positions : {assigned_employee}')
            else:
                # メインポジションの人が足りなかった場合は、サブポジションの人を優先に割り当てる
                assigned_employee = assign_main_positions_additional_employee(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count)
                logging.debug(f'from assign_additional_positions : {assigned_employee}')

    if assigned_employee:
        required_employees -= 1
    else:
        handle_assignment_error(position_code)
        return None, required_employees
    return assigned_employee, required_employees # assigned_employee = "この処理でアサインされた従業員のID"

# =================================================================
# メイン関数であるassign_employees_for_game_days関数から呼び出される
# =================================================================

# 従業員を条件に従ってアサインする関数
def assign_employees(positions_data, available_employees, positions_count, employee_skills, current_game_time, total_work_time, leader_count):
    assigned_employees = set() # 重複選択を防ぐためのリスト
    new_dict = {} # ポジションコードをキーとして、値にアサインされた従業員のIDが入る辞書
    
    # 割り当て順にポジションを並び替える（リーダー優先、その後はポジションコードの小さい順）
    sorted_positions_count = sorted(positions_count.items(), key=lambda x: (-int(x[0][2]), int(x[0][:2])))
    logging.debug(f'assign_employees sorted_positions_count : {sorted_positions_count}')

    # 各ポジションに必要な数だけ従業員を割り当てる
    for current_position, original_required_employees in sorted_positions_count: # current_position = 3桁の数値（上2桁=ポジションコード + 3桁目=リーダー情報）
        required_employees = int(original_required_employees)  # required_employees = "各ポジションごとの必要な従業員数"
        position_codes = get_position_codes(positions_data, current_position, current_game_time) # current_positionに一致するポジションコードを取り出す
        
        # 必要な数に達するまで割り当て処理を繰り返す
        for position_code in position_codes:
            if required_employees <= 0: # 必要な従業員数が0になったら次のポジションへ
                break
            assigned_employee, required_employees = assign_employee_to_position(
                position_code, available_employees, employee_skills, assigned_employees, current_position, required_employees, total_work_time, leader_count)
            if assigned_employee:
                new_dict[position_code] = assigned_employee # 従業員を割り当て
                # アサインするポジションがリーダーの場合、leader_countを+1する
                if current_position[2] == '1':
                    
                    logging.info(f'current_position : {current_position}')
                    logging.info(f'assigned_leader : {assigned_employee}')
                    leader_count[assigned_employee] += 1
                    logging.info(f'leader_count : {leader_count[assigned_employee]}')

            else:
                new_dict[position_code] = None

    return new_dict, assigned_employees


# アサインされたリストをスプレッドシートに書き込む形に並び替える関数
def sort_new_dict(positions_data, new_dict, current_game_time):
    sorted_new_dict = {}
    for key in sorted(positions_data[current_game_time]['positions'].keys(), key=int):
        position_code = positions_data[current_game_time]['positions'][key]
        sorted_new_dict[position_code] = new_dict[position_code]
    return sorted_new_dict
