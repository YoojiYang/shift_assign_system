import sys
sys.path.append('/Users/yoojiyang/Desktop/dev/ESCON/esconShiftAsignProject')
import gspread


from component import open_spreadsheet
from component.get_data.employee_skills_data import get_employee_skills
from component.get_data.positions_data import get_positions_data
from component.get_data.work_day_data import get_work_day_data
from component.assign_employees.assign_employees import assign_employees_for_game_days

employee_skills = get_employee_skills()
positions_data = get_positions_data()
availability_employees, late_Start_or_leave_early = get_employees_availability()
work_day_data = get_work_day_data()

main_assignments, unassigned_employees_per_day, total_work_time = assign_employees_for_game_days(work_day_data, positions_data, employee_skills, total_work_time)

def write_to_spreadsheet(main_assignments, unassigned_employees_per_day, late_Start_or_leave_early):
    # スプレッドシートを開く
    spreadsheet = open_spreadsheet()

    # 各セクションの出力開始と終了のセル位置を指定
    sections = [
        (main_assignments, 'B7', 'B36'),
        (unassigned_employees_per_day, 'B40', 'B49'),
        (late_Start_or_leave_early, 'B44', 'B49'),
    ]

    # 各セクションに対してデータを書き込み
    for section_data, start_cell, end_cell in sections:
        if isinstance(section_data, dict):
            for date, assignments in section_data.items():
                # 出力先のシート名を指定
                worksheet = spreadsheet.worksheet(date)
                if isinstance(assignments, dict):  # 辞書の入れ子構造の場合
                    values_to_write = [[value] for value in assignments.values()]
                else:  # 辞書の値がリストの場合
                    values_to_write = [[value] for value in assignments]
                worksheet.update(f'{start_cell}:{end_cell}', values_to_write)


    print("All assignments have been written to the Google Spreadsheet")


write_to_spreadsheet(main_assignments, unassigned_employees_per_day, late_Start_or_leave_early)
