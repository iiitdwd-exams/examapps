import pandas as pd
import openpyxl as xl


df = pd.read_csv("FList_2024_05.csv")
g = df.groupby('roll_no')
chunks = [group for _, group in g]
x = chunks[1].copy()
r = x.iloc[0, 0].lower()
n = x.iloc[0, 1].lower().replace(' ', '_')
fname = f"{r}_{n}.xlsx"
x.loc[:, ['code', 'course']].to_excel(fname, index=False)

wb = xl.load_workbook(fname)
ws = wb.active

for row in ws.iter_rows():
    for cell in row:
        cell.protection = xl.styles.Protection(locked=True)
ws.protection.set_password('secret')
wb.save(fname)

