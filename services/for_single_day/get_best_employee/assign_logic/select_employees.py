import logging
logging.basicConfig(level=logging.INFO)

from ......models import (
    positions_details,
    
)


# =================================================================
# assign_employees_to_position関数から呼び出される
# =================================================================

# 特定ポジションへの割り当て処理
def assign_main_positions(current_target_work_code7, available_employees, employee_skills, assigned_employees, total_work_time, leader_count):
    # ポジションコードの上2桁を取得
    # position_type = current_target_work_code7[:2]
    # ポジションコードに対応するskillsの開始桁数を取得する
    skill_index = positions_details[current_target_work_code7[:2]]['skills_index'] # スキルインデックスを取得
    # 従業員をリストアップ
    suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index)
    # 従業員をアサイン
    return assign_best_employee(suitable_employees, assigned_employees, total_work_time)



# 特定ポジションへの割り当てが足りなかった時の処理
def assign_main_positions_additional_employee(current_target_work_code7, available_employees, employee_skills, assigned_employees, total_work_time, leader_count):

    # ポジションコードの上2桁を取得
    position_type = str(current_target_work_code7)[:2]
    # ポジションコードに対応するskillsの開始桁数を取得する
    skill_index = positions_details[position_type]['skills_index'] # スキルインデックスを取得
    suitable_employees = select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index + 2, current_target_work_code7, leader_count)
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


# 条件に一致する従業員の中から、最も優先順位の高い従業員を選択する（勤務時間が少ない > スキルランクが高い）
def assign_best_employee(suitable_employees, assigned_employees, total_work_time):
    if suitable_employees:
        suitable_employees.sort(key=lambda x: (total_work_time[x[0]], x[1]))
        best_employee = suitable_employees[0][0]
        assigned_employees.add(best_employee)
        return best_employee
    return None




# 特定ポジションにアサインできる条件の設定
def is_suitable_employee(employee_id, skill, available_employees, assigned_employees, skill_index):
    """
    この関数は、従業員が特定のポジションに適しているかどうかを判断します。
    （ここにパラメータと戻り値の説明を追加）
    """
    has_required_skill = skill[skill_index] == '1'
    is_available = employee_id in available_employees
    is_not_assigned = employee_id not in assigned_employees
    is_leader = skill[0] == '1'
    return has_required_skill, is_available, is_not_assigned, is_leader


# =================================================================
# assign_xxxxxx_position関数から呼び出される
# =================================================================

# 従業員をポジションにアサインする
def select_suitable_employees(available_employees, employee_skills, assigned_employees, skill_index):
    suitable_employees = []
    for employee_id, skill in employee_skills.items():
        if is_suitable_employee( employee_id, skill, available_employees, assigned_employees, skill_index):
            suitable_employees.append((employee_id, int(skill[skill_index + 1])))
    return suitable_employees

# =================================================================
# リーダーを選ぶ条件
# =================================================================

# skillsの1桁目が1である
def is_suitable_leader(skill):
    is_leader = skill[0] == '1'
    return is_leader

# リーダー候補者を、リーダーへのアサイン回数が少ない順に並べる
def get_min_leader_count(suitable_employees, leader_count):
    return min(leader_count[employee[0]] for employee in suitable_employees)

# リーダー候補者を、リーダーへのアサイン回数が最も少ない人だけに絞る
def filter_by_min_leader_count(suitable_employees, leader_count):
    min_leader_count = get_min_leader_count(suitable_employees, leader_count)
    return [employee for employee in suitable_employees if leader_count[employee[0]] == min_leader_count]

# リーダーを選ぶ処理を行う関数
def select_suitable_leader(suitable_employees, leader_count, available_employees, assigned_employees, skill_index):
    for employee_id, skill in employee_skills.items():
        if is_suitable_leader(skill) and is_suitable_employee( employee_id, skill, available_employees, assigned_employees, skill_index):
            suitable_employees.append((employee_id, int(skill[skill_index + 1])))

    suitable_employees.sort(key=lambda x: (leader_count[x[0]], x[1]))
    return suitable_employees