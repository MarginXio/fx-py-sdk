from fx_py_sdk.grpc_client import GRPCClient
from fx_py_sdk.codec.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
import xlrd
import xlwt
from xlutils.copy import copy

USDT = "USDT"

def write_excel_xls(path, sheet_name, value):
    try:
        workbook = xlrd.open_workbook(path)
        index = len(value)
        new_workbook = copy(workbook)
        sheet = new_workbook.add_sheet(sheet_name)
        for i in range(0, index):
            for j in range(0, len(value[i])):
                sheet.write(i, j, value[i][j])
        new_workbook.save(path)

    except Exception as e:
        index = len(value)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(sheet_name)
        for i in range(0, index):
            for j in range(0, len(value[i])):
                sheet.write(i, j, value[i][j])
        workbook.save(path)

def write_excel_xls_append(path, sheet, value):
    index = len(value)
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    rows_old = worksheet.nrows
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(sheet)
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])
    new_workbook.save(path)


def main():
    pair_list = ["AAPL", "AMZN", "BTC", "FB", "FX", "GOOG", "IWM", "NFLX", "SPY", "TQQQ", "TSLA"]
    for pair in pair_list:
        client = GRPCClient(f"https://testnet-${pair.lower()}-grpc.marginx.io:9090")
        # client = GRPCClient(f"127.0.0.1:9090")

        book_name_xls = pair + ".xls"
        sheet_balance = "balance"
        sheet_position = "position"

        title_balance = [["accounts", "balance"]]
        write_excel_xls(book_name_xls, sheet_balance, title_balance)

        title_position = [["accounts", "balance", "position_id", "pair_id", "direction", "entry_price", "base_quantity", "leverage", "margin", "liquidation_price"]]
        write_excel_xls(book_name_xls, sheet_position, title_position)

        record_balances = []
        record_positions = []

        accounts = client.query_accounts(0)
        pair_id = pair + ":" + USDT
        for account_any in accounts:
            account = BaseAccount()
            if account_any.Is(account.DESCRIPTOR):
                account_any.Unpack(account)
                balance = client.query_balance(account.address, USDT)

                balance_acc = [account.address,
                               balance[USDT],
                               ]

                record_balances.append(balance_acc)
                positions = client.query_positions(account.address, pair_id)
                if len(positions) > 0:
                    for position in positions:
                        record_position = [account.address,
                                       balance[USDT],
                                       position.Id,
                                       position.PairId,
                                       position.Direction,
                                       position.EntryPrice,
                                       position.BaseQuantity,
                                       position.Leverage,
                                       position.Margin,
                                       position.LiquidationPrice,
                                       ]
                        record_positions.append(record_position)

        if len(record_positions) > 0:
            write_excel_xls_append(book_name_xls, sheet_position, record_positions)
        if len(record_balances) > 0:
            write_excel_xls_append(book_name_xls, sheet_balance, record_balances)

if __name__ == "__main__":
    main()


