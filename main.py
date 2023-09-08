from models import (
    get_work_day_data,
)

from services.create_all_periods_lists import create_all_periods_lists
from services.write_spreadsheet import write_to_spreadsheet

work_day_data = get_work_day_data()


# 従業員のアサインリストを作成
regular_position_dict, reserve_position_dict = create_all_periods_lists(work_day_data)

# 作成したアサインリストをスプレッドシートに書き込む
write_to_spreadsheet(regular_position_dict, reserve_position_dict, work_day_data)

# print(f'regular_position_dict: {regular_position_dict}')
# print(f'reserve_position_dict: {reserve_position_dict}')