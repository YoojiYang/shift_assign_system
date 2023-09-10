import pandas as pd

def get_employee_skills(spreadsheet):
  # spreadsheet = open_spreadsheet()
  employee_master = spreadsheet.worksheet('従業員マスタ')
  employee_data = employee_master.get_all_values()
  df_employee = pd.DataFrame(employee_data)
  df_employee.columns = df_employee.iloc[1]
  df_employee = df_employee.iloc[2:]

  # 辞書を作成
  employee_skills = {row['id']: row['skills'] for index, row in df_employee.iterrows() if row['id']}

  return employee_skills

# if __name__ == "__main__":
  # employee_skills = get_employee_skills(spreadsheet)
  # print("employee_skills: ", employee_skills)