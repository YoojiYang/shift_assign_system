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
        if is_suitable_leader(skill) and is_suitable_employee(employee_id, skill, available_employees, assigned_employees, skill_index):
            suitable_employees.append((employee_id, int(skill[skill_index + 1])))

    suitable_employees.sort(key=lambda x: (leader_count[x[0]], x[1]))
    return suitable_employees