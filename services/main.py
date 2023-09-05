# =================================================================
# main.pyから呼び出されるメインの関数
# =================================================================
def assign_employees_for_game_days(work_day_data, positions_data, employee_skills, total_work_time):
    
    logging.info(f'assign_employees_for_game_days : start!')

    main_assignments = {}
    unassigned_employees_per_day = {}

    # game_daysのキー値の数だけ繰り返す
    for current_game_day, game_info in work_day_data['game_days'].items():
        # current_game_dayに紐づくplayballTimeをcurrent_game_timeという変数にして管理する
        current_game_time = game_info['playballTime']
        
        logging.info("---------------------------------------------------------------------------------------------------------")
        logging.info(f'current_game_day: {current_game_day}')
        logging.info(f'leader_count: {leader_count}')
        logging.info(f'total_work_time: {total_work_time}')
        logging.debug(f'Playball Time is : {current_game_time}')
        logging.info("---------------------------------------------------------------------------------------------------------")
        
        # その試合の出勤可能な従業員とポジションを設定する
        available_employees = work_day_data['availability_employees'][current_game_day]
        positions_count = positions_data[current_game_time]['counts']
        print(f'positions_count{positions_count}')

        # 従業員のアサイン処理
        new_dict, assigned_employees = assign_employees(positions_data, available_employees, positions_count, employee_skills, current_game_time, total_work_time, leader_count)
        
        # 従業員の勤務時間を追跡
        for key, value in new_dict.items():
            if value is None: # 従業員がアサインされてない場合はスキップ
                continue
            work_time = int(key[5]) # キー値の6桁目の値を数値として取得
            total_work_time[value] += work_time
        logging.debug(f"{current_game_day} total_work_time :  {total_work_time}")
        
        # スプシに出力する順番に並び替える
        assigned_dict = sort_new_dict(positions_data, new_dict, current_game_time)
        logging.debug(f' {current_game_day}のアサインリスト:{len(assigned_dict)}人 {assigned_dict}')

        # 結果をall_assignmentsに保存する
        main_assignments[current_game_day] = assigned_dict
        
        unassigned_employees = [employee for employee in available_employees if employee not in assigned_employees]
        unassigned_employees_per_day[current_game_day] = unassigned_employees # その日の未割り当て従業員を辞書に追加
        logging.debug(f' {current_game_day}で割り当てが漏れた人リスト:{len(unassigned_employees)}人 {unassigned_employees}')
        
    return main_assignments, unassigned_employees_per_day, total_work_time