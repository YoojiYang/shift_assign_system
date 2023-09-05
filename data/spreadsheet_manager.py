# スプレッドシートから情報を取得する処理
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

def get_spreadsheet_client():
  # Google Spread Sheetに接続するための設定
  scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
  
  # 現在のスクリプトのディレクトリを取得
  current_dir = os.path.dirname(os.path.abspath(__file__))

  # JSONファイルへのパスを生成
  path_to_json = os.path.join(current_dir, 'ana-shift-assignment-07cb8be7f0b3.json')
  
  creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scope) # type: ignore
  client = gspread.authorize(creds)
  
  return client

def open_spreadsheet():
  client = get_spreadsheet_client()
  return  client.open_by_key('1d9rgXAdueB4AKwHLmORO5vMBCi4RQrK7BLuTqSFTJu4')
