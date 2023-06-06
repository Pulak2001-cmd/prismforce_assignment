import json, os
from datetime import datetime
import operator

def generate_balance_sheet(data):
    balance_sheet = {}

    if 'revenueData' in data:
        for entry in data['revenueData']:
            if 'startDate' in entry and 'amount' in entry:
                date = datetime.strptime(entry['startDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                month_key = date.strftime('%Y-%m')

                if month_key not in balance_sheet:
                    balance_sheet[month_key] = {'revenue': 0, 'expense': 0}

                balance_sheet[month_key]['revenue'] += entry['amount']

    if 'expenseData' in data:
        for entry in data['expenseData']:
            if 'startDate' in entry and 'amount' in entry:
                date = datetime.strptime(entry['startDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                month_key = date.strftime('%Y-%m')

                if month_key not in balance_sheet:
                    balance_sheet[month_key] = {'revenue': 0, 'expense': 0}

                balance_sheet[month_key]['expense'] += entry['amount']

    min_date = min(balance_sheet.keys()) if balance_sheet else None
    max_date = max(balance_sheet.keys()) if balance_sheet else None

    if min_date and max_date:
        start_date = datetime.strptime(min_date, '%Y-%m')
        end_date = datetime.strptime(max_date, '%Y-%m')

        current_date = start_date
        while current_date <= end_date:
            month_key = current_date.strftime('%Y-%m')
            if month_key not in balance_sheet:
                balance_sheet[month_key] = {'revenue': 0, 'expense': 0}
            current_date = current_date.replace(month=current_date.month + 1)

    for month_key, month_data in balance_sheet.items():
        balance_sheet[month_key]['balance'] = month_data['revenue'] - month_data['expense']

    sorted_balance_sheet = sorted(balance_sheet.items(), key=operator.itemgetter(0))

    output = {
        "balance": [
            {
                "amount": month_data['balance'],
                "startDate": f"{month_key}-01T00:00:00.000Z"
            }
            for month_key, month_data in sorted_balance_sheet
        ]
    }

    print(json.dumps(output, indent=2))
    
    with open('output.json', 'w') as w:
        json.dump(output, w, indent=4)

# Taking input json file
with open('2-input.json') as f:
    json_data = json.load(f)

generate_balance_sheet(json_data)