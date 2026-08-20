from datetime import date, timedelta

from warehouse import load_usage_rows, save_checkpoint
from finance import upload_csv


def run(day=None):
    target_day = day or date.today() - timedelta(days=1)
    rows = load_usage_rows(target_day)
    totals = {}
    for row in rows:
        account = row["account_id"]
        totals[account] = totals.get(account, 0) + int(row["units"])
    upload_csv(target_day, totals)
    save_checkpoint("daily_usage_export", target_day)
