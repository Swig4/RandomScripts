import tkinter as tk
def press(key): 
    if key == "C": entry.delete(0, tk.END)
    elif key == "=": 
        try: result = eval(entry.get()); entry.delete(0, tk.END); entry.insert(tk.END, str(result))
        except: entry.delete(0, tk.END); entry.insert(tk.END, "Error")
    else: entry.insert(tk.END, key)
root = tk.Tk(); root.title("Calculator"); buttons = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', 'C', '0', '=', '+']; entry = tk.Entry(root, width=16, font=('Arial', 18), justify='right'); entry.grid(row=0, column=0, columnspan=4)
for i, btn in enumerate(buttons): tk.Button(root, text=btn, width=5, height=2, font=('Arial', 14), command=lambda key=btn: press(key)).grid(row=(i//4)+1, column=i%4)
root.mainloop()