# テスト実行用
if __name__ == "__main__":
    main_assignments, unassigned_employees_per_day, total_work_time = assign_employees_for_game_days(work_day_data, positions_data, employee_skills, total_work_time)
    
    logging.debug(f"main_assignments :  {main_assignments}")
    logging.debug(f"unassigned_employees_per_day :  {unassigned_employees_per_day}")
    logging.info(f"total_work_time :  {total_work_time}")
