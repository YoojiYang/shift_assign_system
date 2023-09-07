import sys
sys.path.append('/Users/yoojiyang/Desktop/shift/shift_assign_system')

from models import (
    get_work_day_data,
)

from services.for_single_day import (
    create_all_periods_lists,
    write_to_spreadsheet
)
work_day_data = get_work_day_data()


# 従業員のアサインリストを作成
regular_position_dict, reserve_position_dict = create_all_periods_lists()

# 作成したアサインリストをスプレッドシートに書き込む
write_to_spreadsheet(regular_position_dict, reserve_position_dict, work_day_data)
