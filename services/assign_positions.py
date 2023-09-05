# =================================================================
# assign_employees_to_position関数から呼び出される
# =================================================================

# 特定ポジションへの割り当て処理
def assign_main_positions(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count):
    # ポジションコードの上2桁を取得
    # position_type = position_code[:2]
    # ポジションコードに対応するskillsの開始桁数を取得する
    skill_index = positions_details[position_code[:2]]['skills_index'] # スキルインデックスを取得
    # 従業員をリストアップ
    suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index, position_code, leader_count)
    # 従業員をアサイン
    return assign_best_employee(suitable_employees, assigned_employees, total_work_time)



# 特定ポジションへの割り当てが足りなかった時の処理
def assign_main_positions_additional_employee(position_code, available_employees, employee_skills, assigned_employees, total_work_time, leader_count):

    # ポジションコードの上2桁を取得
    position_type = str(position_code)[:2]
    # ポジションコードに対応するskillsの開始桁数を取得する
    skill_index = positions_details[position_type]['skills_index'] # スキルインデックスを取得
    suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index + 2, position_code, leader_count)
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


