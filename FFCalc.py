from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd
from tkinter import simpledialog as tksd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.main()

    def mode(self):
        if int(self.rb_var.get()) == 1:
            for i in range(0,2):
                self.entries_x[i].configure(state=NORMAL)
                self.entries_y[i].configure(state=NORMAL)
                self.entries_z[i].configure(state=NORMAL)
            for i in range(2,6):
                self.entries_x[i].configure(state="readonly")
                self.entries_y[i].configure(state="readonly")
                self.entries_z[i].configure(state="readonly")

        if int(self.rb_var.get()) == 2:
            for i in range(0,4):
                self.entries_x[i].configure(state=NORMAL)
                self.entries_y[i].configure(state=NORMAL)
                self.entries_z[i].configure(state=NORMAL)
            for i in range(4,6):
                self.entries_x[i].configure(state="readonly")
                self.entries_y[i].configure(state="readonly")
                self.entries_z[i].configure(state="readonly")

        if int(self.rb_var.get()) == 3:
            for i in range(0,6):
                self.entries_x[i].configure(state=NORMAL)
                self.entries_y[i].configure(state=NORMAL)
                self.entries_z[i].configure(state=NORMAL)

    def exit():
        quit()

    def calc(self):
        mu = [0, 0, 0]
        alpha = [0, 0, 0]
        beta = [0, 0, 0]
        gamma = [0, 0, 0]

        if float(self.field.get()) == 0:
            tkmb.showerror("Error", "The field value must be different than 0.")
            return 0

        if int(self.rb_var.get()) == 1:
            mu[0] = (-1 * (float(self.entries_x[0].get()) - float(self.entries_x[1].get())) / (2 * float(self.field.get())))
            mu[1] = (-1 * (float(self.entries_y[0].get()) - float(self.entries_y[1].get())) / (2 * float(self.field.get())))
            mu[2] = (-1 * (float(self.entries_z[0].get()) - float(self.entries_z[1].get())) / (2 * float(self.field.get())))
            alpha[0] = (-1 * (((float(self.entries_x[0].get()) + float(self.entries_x[1].get())) - (2 * float(self.entries_zero[0].get()))) / (float(self.field.get())**2)))
            alpha[1] = (-1 * (((float(self.entries_y[0].get()) + float(self.entries_y[1].get())) - (2 * float(self.entries_zero[0].get()))) / (float(self.field.get())**2)))
            alpha[2] = (-1 * (((float(self.entries_z[0].get()) + float(self.entries_z[1].get())) - (2 * float(self.entries_zero[0].get()))) / (float(self.field.get())**2)))
            for i in range(0,3):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(mu[i]))
                self.results[i].configure(state="readonly")
            for i in range(3,6):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(alpha[i-3]))
                self.results[i].configure(state="readonly")
            for i in range(6,12):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, "Change mode to 2F or 3F!") #Tu można coś zrobić z długością napisu
                self.results[i].configure(state="readonly")

        if int(self.rb_var.get()) == 2:
            mu[0] = (-1 * (8 * (float(self.entries_x[0].get()) - float(self.entries_x[1].get())) - (float(self.entries_x[2].get()) - float(self.entries_x[3].get())))/(12 * float(self.field.get())))
            mu[1] = (-1 * (8 * (float(self.entries_y[0].get()) - float(self.entries_y[1].get())) - (float(self.entries_y[2].get()) - float(self.entries_y[3].get())))/(12 * float(self.field.get())))
            mu[2] = (-1 * (8 * (float(self.entries_z[0].get()) - float(self.entries_z[1].get())) - (float(self.entries_z[2].get()) - float(self.entries_z[3].get())))/(12 * float(self.field.get())))
            alpha[0] = (-1 * (((16 * (float(self.entries_x[0].get()) + float(self.entries_x[1].get()))) - (float(self.entries_x[2].get()) + float(self.entries_x[3].get())) - (30 * float(self.entries_zero[0].get()))) / (12 * float(self.field.get())**2)))
            alpha[1] = (-1 * (((16 * (float(self.entries_y[0].get()) + float(self.entries_y[1].get()))) - (float(self.entries_y[2].get()) + float(self.entries_y[3].get())) - (30 * float(self.entries_zero[0].get()))) / (12 * float(self.field.get())**2)))
            alpha[2] = (-1 * (((16 * (float(self.entries_z[0].get()) + float(self.entries_z[1].get()))) - (float(self.entries_z[2].get()) + float(self.entries_z[3].get())) - (30 * float(self.entries_zero[0].get()))) / (12 * float(self.field.get())**2)))
            beta[0] = (((2 * (float(self.entries_x[0].get()) - float(self.entries_x[1].get()))) - (float(self.entries_x[2].get()) - float(self.entries_x[3].get()))) / (2 * float(self.field.get())**3))
            beta[1] = (((2 * (float(self.entries_y[0].get()) - float(self.entries_y[1].get()))) - (float(self.entries_y[2].get()) - float(self.entries_y[3].get()))) / (2 * float(self.field.get())**3))
            beta[2] = (((2 * (float(self.entries_z[0].get()) - float(self.entries_z[1].get()))) - (float(self.entries_z[2].get()) - float(self.entries_z[3].get()))) / (2 * float(self.field.get())**3))
            gamma[0] = (((4 * (float(self.entries_x[0].get()) + float(self.entries_x[1].get()))) - (float(self.entries_x[2].get()) + float(self.entries_x[3].get())) - (6 * float(self.entries_zero[0].get()))) / (float(self.field.get())**4))
            gamma[1] = (((4 * (float(self.entries_y[0].get()) + float(self.entries_y[1].get()))) - (float(self.entries_y[2].get()) + float(self.entries_y[3].get())) - (6 * float(self.entries_zero[0].get()))) / (float(self.field.get())**4))
            gamma[2] = (((4 * (float(self.entries_z[0].get()) + float(self.entries_z[1].get()))) - (float(self.entries_z[2].get()) + float(self.entries_z[3].get())) - (6 * float(self.entries_zero[0].get()))) / (float(self.field.get())**4))
            for i in range(0,3):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(mu[i]))
                self.results[i].configure(state="readonly")
            for i in range(3,6):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(alpha[i-3]))
                self.results[i].configure(state="readonly")
            for i in range(6,9):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(beta[i-6]))
                self.results[i].configure(state="readonly")
            for i in range(9,12):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(gamma[i-9]))
                self.results[i].configure(state="readonly")


        if int(self.rb_var.get()) == 3:
            mu[0] = (-1 * (8 * (float(self.entries_x[0].get()) - float(self.entries_x[1].get())) - (float(self.entries_x[2].get()) - float(self.entries_x[3].get())))/(12 * float(self.field.get())))
            mu[1] = (-1 * (8 * (float(self.entries_y[0].get()) - float(self.entries_y[1].get())) - (float(self.entries_y[2].get()) - float(self.entries_y[3].get())))/(12 * float(self.field.get())))
            mu[2] = (-1 * (8 * (float(self.entries_z[0].get()) - float(self.entries_z[1].get())) - (float(self.entries_z[2].get()) - float(self.entries_z[3].get())))/(12 * float(self.field.get())))
            alpha[0] = (-1 * (((16 * (float(self.entries_x[0].get()) + float(self.entries_x[1].get()))) - (float(self.entries_x[2].get()) + float(self.entries_x[3].get())) - (30 * float(self.entries_zero[0].get()))) / (12 * float(self.field.get())**2)))
            alpha[1] = (-1 * (((16 * (float(self.entries_y[0].get()) + float(self.entries_y[1].get()))) - (float(self.entries_y[2].get()) + float(self.entries_y[3].get())) - (30 * float(self.entries_zero[0].get()))) / (12 * float(self.field.get())**2)))
            alpha[2] = (-1 * (((16 * (float(self.entries_z[0].get()) + float(self.entries_z[1].get()))) - (float(self.entries_z[2].get()) + float(self.entries_z[3].get())) - (30 * float(self.entries_zero[0].get()))) / (12 * float(self.field.get())**2))) #alfy i mu są takie same jak w 2F. To dobrze?
            beta[0] = ((-1 * ((float(self.entries_x[2].get()) - float(self.entries_x[3].get())) - ((float(self.entries_x[4].get()) - float(self.entries_x[5].get())) / 8) - (13 * (float(self.entries_x[0].get()) - float(self.entries_x[1].get())) / 8))) / (float(self.field.get())**3))
            beta[1] = ((-1 * ((float(self.entries_y[2].get()) - float(self.entries_y[3].get())) - ((float(self.entries_y[4].get()) - float(self.entries_y[5].get())) / 8) - (13 * (float(self.entries_y[0].get()) - float(self.entries_y[1].get())) / 8))) / (float(self.field.get())**3))
            beta[2] = ((-1 * ((float(self.entries_z[2].get()) - float(self.entries_z[3].get())) - ((float(self.entries_z[4].get()) - float(self.entries_z[5].get())) / 8) - (13 * (float(self.entries_z[0].get()) - float(self.entries_z[1].get())) / 8))) / (float(self.field.get())**3))
            gamma[0] = (-1 * ((-1 * 2 * (float(self.entries_x[2].get()) + float(self.entries_x[3].get()))) + ((float(self.entries_x[4].get()) + float(self.entries_x[5].get())) / 6) + (13 * (float(self.entries_x[0].get()) + float(self.entries_x[1].get())) / 2) - ((28 * float(self.entries_zero[0].get())) / 3)) / (float(self.field.get())**4))
            gamma[1] = (-1 * ((-1 * 2 * (float(self.entries_y[2].get()) + float(self.entries_y[3].get()))) + ((float(self.entries_y[4].get()) + float(self.entries_y[5].get())) / 6) + (13 * (float(self.entries_y[0].get()) + float(self.entries_y[1].get())) / 2) - ((28 * float(self.entries_zero[0].get())) / 3)) / (float(self.field.get())**4))
            gamma[2] = (-1 * ((-1 * 2 * (float(self.entries_z[2].get()) + float(self.entries_z[3].get()))) + ((float(self.entries_z[4].get()) + float(self.entries_z[5].get())) / 6) + (13 * (float(self.entries_z[0].get()) + float(self.entries_z[1].get())) / 2) - ((28 * float(self.entries_zero[0].get())) / 3)) / (float(self.field.get())**4))
            for i in range(0,3):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(mu[i]))
                self.results[i].configure(state="readonly")
            for i in range(3,6):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(alpha[i-3]))
                self.results[i].configure(state="readonly")
            for i in range(6,9):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(beta[i-6]))
                self.results[i].configure(state="readonly")
            for i in range(9,12):
                self.results[i].configure(state=NORMAL)
                self.results[i].delete(0,END)
                self.results[i].insert(END, str(gamma[i-9]))
                self.results[i].configure(state="readonly")
 
    def save(self):
        self.filename = filedialog.asksaveasfilename(initialdir = ".",title = "Save output",filetypes = (("output files","*.out"),("all files","*.*")))
        f = open(self.filename, "w")
        for i in range(12):
            f.write(self.results_label_names[i] + "		")
            f.write(str(self.results[i].get()) + "\n")
        f.close()
        tkmb.showinfo('Information', 'File Saved!')

    def main(self):

        self.master.title("FFCalc") #tytuł okna

        leftside_one = Frame(root) #frejmy, ogólny układ
        leftside_one.grid(row=0, column=0)
        leftside_two = Frame(root)
        leftside_two.grid(row=1, column=0)
        leftside_three = Frame(root)
        leftside_three.grid(row=2, column=0)
        leftside_four = Frame(root)
        leftside_four.grid(row=3, column=0)
        middleside_one = Frame(root)
        middleside_one.grid(row=0, column=1)
        middleside_two = Frame(root)
        middleside_two.grid(row=1, column=1)
        middleside_three = Frame(root)
        middleside_three.grid(row=2, column=1)
        middleside_four = Frame(root)
        middleside_four.grid(row=3, column=1)
        rightside_one = Frame(root)
        rightside_one.grid(row=0, column=2)
        rightside_two = Frame(root)
        rightside_two.grid(row=1, column=2)
        rightside_three = Frame(root)
        rightside_three.grid(row=2, column=2)
        rightside_four = Frame(root)
        rightside_four.grid(row=3, column=2)

        self.rb_var = tk.StringVar() # wybór, z ilu pól korzystamy
        self.rb_var.set(3)
        rb_onefield = tk.Radiobutton(middleside_one, variable = self.rb_var, value = 1, text = "1F", command=lambda: self.mode())
        rb_twofield = tk.Radiobutton(middleside_one, variable = self.rb_var, value = 2, text = "2F", command=lambda: self.mode())
        rb_threefield = tk.Radiobutton(middleside_one, variable = self.rb_var, value = 3, text = "3F", command=lambda: self.mode())
        rb_onefield.grid(row=0, column=0)
        rb_twofield.grid(row=0, column=1)
        rb_threefield.grid(row=0, column=2)

        k = 1
        self.results = []
        self.entries_zero = []
        self.entries_x = []
        self.entries_y = []
        self.entries_z = []
        energy_labels_zero = []
        energy_labels_x = []
        energy_labels_y = []
        energy_labels_z = []
        energy_labels_zero = tk.Label(leftside_one, text="Enter energies below [a.u.]: ")
        energy_labels_zero.grid(row=0, column=0, columnspan=2)
 
        field_label = tk.Label(rightside_one, text="Enter electric field [a.u.]: ") #tu podajemy pole elektryczne
        field_label.grid(row=0, column=0, columnspan=3)
        self.field = tk.Entry(rightside_one)
        self.field.grid(row=1, column=0)
        self.field.insert(END, "0")

        energy_labels = tk.Label(leftside_one, text="E(F0): ")
        energy_labels.grid(row=1, column=0)
        for i in range(6):
            if i % 2 == 0:
               energy_labels = tk.Label(leftside_two, text="E(F+" + str(k) + ")_x: ")
               energy_labels.grid(row=i, column=0)
               energy_labels = tk.Label(leftside_three, text="E(F+" + str(k) + ")_y: ")
               energy_labels.grid(row=i, column=0)
               energy_labels = tk.Label(leftside_four, text="E(F+" + str(k) + ")_z: ")
               energy_labels.grid(row=i, column=0)
            else:
               energy_labels = tk.Label(leftside_two, text="E(F-" + str(k) + ")_x: ")
               energy_labels.grid(row=i, column=0)
               energy_labels = tk.Label(leftside_three, text="E(F-" + str(k) + ")_y: ")
               energy_labels.grid(row=i, column=0)
               energy_labels = tk.Label(leftside_four, text="E(F-" + str(k) + ")_z: ")
               energy_labels.grid(row=i, column=0)
               k = k + 1

        self.entries_zero.append(tk.Entry(leftside_one))
        self.entries_zero[0].grid(row=1, column=1)
        self.entries_zero[0].insert(END, "0")

        for i in range(6):
            self.entries_x.append(tk.Entry(leftside_two))
            self.entries_x[i].grid(row=i, column=1)
            self.entries_x[i].insert(END, "0")
            self.entries_y.append(tk.Entry(leftside_three))
            self.entries_y[i].grid(row=i, column=1)
            self.entries_y[i].insert(END, "0")
            self.entries_z.append(tk.Entry(leftside_four))
            self.entries_z[i].grid(row=i, column=1)
            self.entries_z[i].insert(END, "0")

        self.results_label_names = ["μ_x", "μ_y", "μ_z", "α_xx", "α_yy", "α_zz", "β_xxx", "β_yyy", "β_zzz", "γ_xxxx", "γ_yyyy", "γ_zzzz"]
        computation_results = tk.Label(rightside_one, text="Computation results [a.u.]: ")
        computation_results.grid(row=2, column=0, columnspan=2)

        for i in range(12):
            results_labels = tk.Label(rightside_two, text=self.results_label_names[i])
            results_labels.grid(row=i+1, column=0)

        for i in range(12):
            self.results.append(tk.Entry(rightside_two))
            self.results[i].grid(row=i+1, column=1)
            self.results[i].insert(END, "0")
            self.results[i].configure(state="readonly")

        calc = Button(rightside_three, text="Calculate properties",command=lambda: self.calc())
        calc.grid(row=14, column=1)

        saving = Button(rightside_three, text="Save results",command=lambda: self.save())
        saving.grid(row=14, column=2)

        exit = Button(rightside_four, text="End",command=window.exit)
        exit.grid(row=14, column=0)

root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width,height))
display = window(root)
root.mainloop()

