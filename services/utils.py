# =================================================================
# select_suitable_employees関数から呼び出される
# =================================================================

# 特定ポジションにアサインできる条件の設定
def is_suitable_employee(employee_id, skill, available_employees, assigned_employees, skill_index):
    has_required_skill = skill[skill_index] == '1'
    is_available = employee_id in available_employees
    is_not_assigned = employee_id not in assigned_employees
    return has_required_skill and is_available and is_not_assigned

