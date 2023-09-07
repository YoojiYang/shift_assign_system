import logging
logging.basicConfig(level=logging.INFO)


# エラーメッセージをログに出力する
def handle_assignment_error(position_code):
    logging.error(f"Error: Could not assign employee for position_code: {position_code}")




# 指定されたポジションコードに従業員を割り当てて、必要な従業員の数を更新する
def get_best_employee(current_target_work_code7, available_employees, assigned_employees, current_position_code3, required_count, total_work_time, leader_count):
    """
    この関数は、現在のアサイン対象となっているポジションに対して、最適な従業員を選択する関数です。
    （ここにパラメータと戻り値の説明を追加）
    """
    # 条件なしでアサインできるポジションに従業員をアサインする処理
    # # アサイン条件のないポジション（スタンドとエントランス）
    # if current_position_code3[:2] not in must_have_skills_positions:
    #     best_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
    #     # logging.debug(f'from assign_sub_positions : {best_employee}')
    # else:
    
    
    # その他のポジションは条件に従って、ベストな従業員をアサインする
    best_employee = assign_main_positions(current_target_work_code7, available_employees, assigned_employees, total_work_time, leader_count)
    # logging.debug(f'from assign_main_positions : {best_employee}')
    if not best_employee:
        # 階段上か階段下の場合は誰でもOK
        if current_position_code3[:2] not in must_have_skills_positions: # skip_additional_employee_positions = "階段上" と "Lounge受付"
            best_employee = assign_sub_positions(available_employees, assigned_employees, total_work_time)
            # logging.debug(f'from skip_additional_employee_positions : {best_employee}')
        else:
            # メインポジションの人が足りなかった場合は、サブポジションの人を優先に割り当てる
            best_employee = assign_main_positions_additional_employee(current_target_work_code7, available_employees, assigned_employees, total_work_time, leader_count)
            # logging.debug(f'from assign_additional_positions : {best_employee}')

    if best_employee:
        required_count -= 1
    else:
        handle_assignment_error(current_position_code3)
        return None, required_count
    return best_employee, required_count


