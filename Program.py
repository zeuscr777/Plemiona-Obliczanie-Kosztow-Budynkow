import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup

def pobierz_dane_o_budynku(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    if "Tartak" in filepath or "Cegielnia" in filepath or "Huta_Zelaza" in filepath:
        table = soup.find('table', class_='wikitable')
    else:
        tables = soup.find_all('table', class_='wikitable')
        table = tables[0]

    if table is None:
        return {}

    data = {}
    rows = table.findAll('tr')[1:]

    for row in rows:
        columns = row.findAll('td')
        try:
            level = int(columns[0].text.strip())
        except ValueError:
            continue

        costs = [
            int(columns[1].text.split()[-1].replace('.', '').replace(',', '')),
            int(columns[2].text.split()[-1].replace('.', '').replace(',', '')),
            int(columns[3].text.split()[-1].replace('.', '').replace(',', '')),
        ]

        data[level] = costs
        
    return data

def wyswietl_dane():
    budynek = budynek_var.get()
    aktualny_poziom = int(poziom_var.get())
    docelowy_poziom = int(docelowy_poziom_var.get())
    
    filepath = f"{budynek}.html"
    budynek_data = pobierz_dane_o_budynku(filepath)

    if not budynek_data:
        result_var.set("Nie można pobrać danych dla tego budynku.")
        return

    drewno, glina, zelazo = 0, 0, 0

    for lvl in range(aktualny_poziom+1, docelowy_poziom+1):
        if lvl in budynek_data:
            drewno += budynek_data[lvl][0]
            glina += budynek_data[lvl][1]
            zelazo += budynek_data[lvl][2]
            
    result_var.set(f"Drewno: {drewno}, Glina: {glina}, Żelazo: {zelazo}")

root = tk.Tk()
root.title("Koszty budynków w Plemionach")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

budynek_var = tk.StringVar()
poziom_var = tk.StringVar()
docelowy_poziom_var = tk.StringVar()
result_var = tk.StringVar()

budynek_label = ttk.Label(frame, text="Wybierz budynek:")
budynek_label.grid(column=0, row=0, sticky=tk.W)
budynek_dropdown = ttk.Combobox(frame, textvariable=budynek_var)
budynek_dropdown['values'] = ('Rynek', 'Tartak', 'Cegielnia', 'Huta_Zelaza', 'Spichlerz', 'Zagroda', 'Kosciol', 'Pierwszy_Kosciol', 'Koszary', 'Kuznia', 'Mur_Obronny', 'Palac', 'Piedestal', 'Plac', 'Ratusz', 'Schowek', 'Stajnia', 'Warsztat', 'Wieza_Straznicza')
budynek_dropdown.grid(column=1, row=0, sticky=tk.W)

poziom_label = ttk.Label(frame, text="Aktualny poziom:")
poziom_label.grid(column=0, row=1, sticky=tk.W)
poziom_entry = ttk.Entry(frame, textvariable=poziom_var)
poziom_entry.grid(column=1, row=1, sticky=tk.W)

docelowy_poziom_label = ttk.Label(frame, text="Docelowy poziom:")
docelowy_poziom_label.grid(column=0, row=2, sticky=tk.W)
docelowy_poziom_entry = ttk.Entry(frame, textvariable=docelowy_poziom_var)
docelowy_poziom_entry.grid(column=1, row=2, sticky=tk.W)

sprawdz_button = ttk.Button(frame, text="Sprawdź koszty", command=wyswietl_dane)
sprawdz_button.grid(column=0, row=3, columnspan=2, pady=10)

result_label = ttk.Label(frame, textvariable=result_var)
result_label.grid(column=0, row=4, columnspan=2, pady=10)

root.mainloop()
