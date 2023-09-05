# エラーメッセージをログに出力する
def handle_assignment_error(position_code):
    logging.error(f"Error: Could not assign employee for position_code: {position_code}")

