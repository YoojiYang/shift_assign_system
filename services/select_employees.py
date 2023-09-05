# =================================================================
# assign_xxxxxx_position関数から呼び出される
# =================================================================

# 従業員をポジションにアサインする
def select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index, position_code, leader_count):
    suitable_employees = []
    # リーダーポジションの場合
    if position_code[2] == '1':
        select_suitable_leader(suitable_employees, leader_count, available_employees, assigned_employees, skill_index)
    # リーダー以外のポジションの場合
    else:
        for employee_id, skill in employee_skills.items():
            if is_suitable_employee(employee_id, skill, available_employees, assigned_employees, skill_index):
                suitable_employees.append((employee_id, int(skill[skill_index + 1])))
    return suitable_employees

# 条件に一致する従業員の中から、最も優先順位の高い従業員を選択する（勤務時間が少ない > スキルランクが高い）
def assign_best_employee(suitable_employees, assigned_employees, total_work_time):
    if suitable_employees:
        suitable_employees.sort(key=lambda x: (total_work_time[x[0]], x[1]))
        best_employee = suitable_employees[0][0]
        assigned_employees.add(best_employee)
        return best_employee
    return None
