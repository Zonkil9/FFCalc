from tkinter import *
from tkinter import messagebox as tk_mb
import tkinter as tk
from tkinter import ttk
import numpy as np


class Romberg(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.label_field = None
        self.field = None
        self.label_a = None
        self.entry_a = None
        self.table_button = None
        self.results = []
        self.master = master
        self.parent = master
        self.pack()
        self.rb_var = tk.StringVar(value="5")
        self.entries = []
        self.entries_zero = []
        self.create_widgets()
        self.update_entries_state()

    def update_entries_state(self):
        num_pairs = int(self.rb_var.get())
        for i, entry in enumerate(self.entries):
            if i < num_pairs * 2:
                entry.configure(state=NORMAL)
            else:
                entry.configure(state="readonly")

    def generalized_romberg_compute(self):
        # Main routine: computes derivatives using the generalized Romberg method
        # - Reads parameters and energies from the GUI
        # - Builds the energy dictionary for only ACTIVE pairs selected in GUI
        # - Calculates finite difference sequences for derivatives
        # - Performs Romberg extrapolation
        # - Returns the computed derivatives (mu, alpha, beta, gamma)
        try:
            h = float(self.field.get())
            a = float(self.entry_a.get())
            if not (a > 1.0):
                tk_mb.showerror("Parameter a", "Parameter a must be > 1.", parent=self.parent)
                return None
        except Exception as exc:
            tk_mb.showerror("Input error", f"Couldn't parse h or a: {exc}", parent=self.parent)
            return None

        try:
            e0 = float(self.entries_zero[0].get())
        except Exception:
            tk_mb.showerror("Input error", "Invalid E(0)", parent=self.parent)
            return None

        # Determine how many pairs are ACTIVE (selected by the user)
        n_pairs_to_use = int(self.rb_var.get())
        n_pairs_total = len(self.entries) // 2
        n_pairs_to_use = max(0, min(n_pairs_to_use, n_pairs_total))

        # Build energies dict ONLY from active pairs E(±a^k h) and E(0)
        energies = {0.0: e0}
        for i in range(n_pairs_to_use):
            idx_pos = 2 * i
            idx_neg = 2 * i + 1
            try:
                ep = float(self.entries[idx_pos].get())
                em = float(self.entries[idx_neg].get())
            except Exception:
                tk_mb.showerror("Input error", f"Invalid energy at pair {i + 1}", parent=self.parent)
                return None
            x = (a ** i) * h
            energies[round(x, 15)] = ep
            energies[round(-x, 15)] = em

        # Fornberg weights for arbitrary grids
        def finite_diff_weights(x_new, x0, m):
            n = len(x_new)
            w = np.zeros((n, m + 1))
            c1 = 1.0
            c4 = x_new[0] - x0
            w[0, 0] = 1.0
            for i in range(1, n):
                mn = min(i, m)
                c2 = 1.0
                c5 = c4
                c4 = x_new[i] - x0
                for j in range(i):
                    c3 = x_new[i] - x_new[j]
                    c2 *= c3
                    if j == i - 1:
                        for k in range(mn, 0, -1):
                            w[i, k] = c1 * (k * w[i - 1, k - 1] - c5 * w[i - 1, k]) / c2
                        w[i, 0] = -c1 * c5 * w[i - 1, 0] / c2
                    for k in range(mn, 0, -1):
                        w[j, k] = (c4 * w[j, k] - k * w[j, k - 1]) / c3
                    w[j, 0] = c4 * w[j, 0] / c3
                c1 = c2
            return w

        def derivative_from_points(points):
            # points: list of (x, f(x)), returns [f'(0), f''(0), f'''(0), f''''(0)]
            xs = np.array([p[0] for p in points], dtype=float)
            ys = np.array([p[1] for p in points], dtype=float)
            # Ensure increasing order for numerical stability
            sort_idx = np.argsort(xs)
            xs = xs[sort_idx]
            ys = ys[sort_idx]
            w = finite_diff_weights(xs, 0.0, 4)
            return [float(np.dot(w[:, m], ys)) for m in range(1, 5)]

        # Build sequences for Romberg:
        # - for m=1,2 use triads [0, ±x_k]
        # - for m=3,4 use 5 points [0, ±x_k, ±x_{k+1}]
        seqs = {1: [], 2: [], 3: [], 4: []}

        # helper to fetch energy
        def energy_at(x):
            return energies.get(round(x, 15), None)

        # m=1,2 from 3-point central stencils
        for k in range(n_pairs_to_use):
            xk = (a ** k) * h
            ep = energy_at(xk)
            em = energy_at(-xk)
            if ep is None or em is None:
                continue
            pts3 = [(0.0, e0), (round(-xk, 15), em), (round(xk, 15), ep)]
            d1, d2, _, _ = derivative_from_points(pts3)
            seqs[1].append(d1)
            seqs[2].append(d2)

        # m=3,4 from 5-point central stencils (need k and k+1)
        for k in range(n_pairs_to_use - 1):
            xk = (a ** k) * h
            xk1 = (a ** (k + 1)) * h
            epk = energy_at(xk)
            emk = energy_at(-xk)
            epk1 = energy_at(xk1)
            emk1 = energy_at(-xk1)
            if None in (epk, emk, epk1, emk1):
                continue
            pts5 = [
                (0.0, e0),
                (round(-xk, 15), emk),
                (round(xk, 15), epk),
                (round(-xk1, 15), emk1),
                (round(xk1, 15), epk1),
            ]
            _, _, d3, d4 = derivative_from_points(pts5)
            seqs[3].append(d3)
            seqs[4].append(d4)

        if len(seqs[1]) == 0:
            tk_mb.showerror("Not enough data", "Not enough points to compute derivatives.", parent=self.parent)
            return None

        # Romberg (Richardson) extrapolation with ratio a and powers a^(2j)
        def romberg_extrapolate(sequence, ratio):
            if len(sequence) == 1:
                return sequence[0]
            R = [list(sequence)]
            l = len(sequence)
            for j in range(1, l):
                prev = R[j - 1]
                cur = []
                factor = (ratio ** (2 * j))
                for w_ in range(0, l - j):
                    # Correct Richardson: (factor * T(h) - T(ah)) / (factor - 1)
                    cur.append((factor * prev[w_] - prev[w_ + 1]) / (factor - 1.0))
                R.append(cur)
            return R[-1][0] if R[-1] else R[0][0]

        results = {}
        for m in (1, 2, 3, 4):
            seq = seqs[m]
            if len(seq) == 0:
                results[m] = 0.0
            else:
                results[m] = romberg_extrapolate(seq, a)

        # Convention for energy derivatives with respect to field F
        mu = -results[1]
        alpha = -results[2]
        beta = -results[3]
        gamma = -results[4]

        return [mu, alpha, beta, gamma]

    def compute_table_results(self, h_values, a_values):
        results_data = {}
        orig_h = self.field.get()
        orig_a = self.entry_a.get()
        orig_entries = [e.get() for e in self.entries]
        orig_e0 = self.entries_zero[0].get()
        for h in h_values:
            self.field.delete(0, tk.END)
            self.field.insert(0, str(h))
            for a in a_values:
                self.entry_a.delete(0, tk.END)
                self.entry_a.insert(0, str(a))
                outs = self.generalized_romberg_compute()
                if outs is None:
                    mu = alpha = beta = gamma = ""
                else:
                    mu, alpha, beta, gamma = outs
                results_data[(h, a)] = (mu, alpha, beta, gamma)
        self.field.delete(0, tk.END)
        self.field.insert(0, orig_h)
        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, orig_a)
        for e, val in zip(self.entries, orig_entries):
            e.delete(0, tk.END)
            e.insert(0, val)
        self.entries_zero[0].delete(0, tk.END)
        self.entries_zero[0].insert(0, orig_e0)
        return results_data

    def open_results_table(self):
        # Build a table with only Romberg-extrapolated values per x_k
        try:
            h = float(self.field.get())
            a = float(self.entry_a.get())
            if not (a > 1.0):
                tk_mb.showerror("Parameter a", "Parameter a must be > 1.", parent=self.parent)
                return
        except Exception:
            tk_mb.showerror("Input error", "Couldn't parse h or a.", parent=self.parent)
            return

        n_pairs = int(self.rb_var.get())
        try:
            e0 = float(self.entries_zero[0].get())
        except Exception:
            tk_mb.showerror("Input error", "Invalid E(0)", parent=self.parent)
            return

        # Collect energies
        energies = {0.0: e0}
        for i in range(n_pairs):
            try:
                ep = float(self.entries[2 * i].get())
                em = float(self.entries[2 * i + 1].get())
            except Exception:
                tk_mb.showerror("Input error", f"Invalid energy at pair {i + 1}", parent=self.parent)
                return
            x = (a ** i) * h
            energies[round(x, 15)] = ep
            energies[round(-x, 15)] = em

        def energy_at(x):
            return energies.get(round(x, 15), None)

        # local Fornberg helpers
        def finite_diff_weights(x_new, x0, m):
            n = len(x_new)
            w = np.zeros((n, m + 1))
            c1 = 1.0
            c4 = x_new[0] - x0
            w[0, 0] = 1.0
            for i in range(1, n):
                mn = min(i, m)
                c2 = 1.0
                c5 = c4
                c4 = x_new[i] - x0
                for j in range(i):
                    c3 = x_new[i] - x_new[j]
                    c2 *= c3
                    if j == i - 1:
                        for k in range(mn, 0, -1):
                            w[i, k] = c1 * (k * w[i - 1, k - 1] - c5 * w[i - 1, k]) / c2
                        w[i, 0] = -c1 * c5 * w[i - 1, 0] / c2
                    for k in range(mn, 0, -1):
                        w[j, k] = (c4 * w[j, k] - k * w[j, k - 1]) / c3
                    w[j, 0] = c4 * w[j, 0] / c3
                c1 = c2
            return w

        def derivative_from_points(points):
            xs = np.array([p[0] for p in points], dtype=float)
            ys = np.array([p[1] for p in points], dtype=float)
            sort_idx = np.argsort(xs)
            xs = xs[sort_idx]
            ys = ys[sort_idx]
            w = finite_diff_weights(xs, 0.0, 4)
            return [float(np.dot(w[:, m], ys)) for m in range(1, 5)]

        def romberg_extrapolate(sequence, ratio):
            if len(sequence) == 0:
                return None
            if len(sequence) == 1:
                return sequence[0]
            r = [list(sequence)]
            l = len(sequence)
            for j in range(1, l):
                prev = r[j - 1]
                cur = []
                factor = (ratio ** (2 * j))
                for w_ in range(0, l - j):
                    cur.append((factor * prev[w_] - prev[w_ + 1]) / (factor - 1.0))
                r.append(cur)
            return r[-1][0] if r[-1] else r[0][0]

        # Build rows and running sequences (only Romberg values)
        rows = []
        seq1 = []
        seq2 = []
        seq3 = []
        seq4 = []
        for k in range(n_pairs):
            xk = (a ** k) * h
            ep = energy_at(xk)
            em = energy_at(-xk)
            if ep is None or em is None:
                continue
            pts3 = [(0.0, e0), (round(-xk, 15), em), (round(xk, 15), ep)]
            d1, d2, _, _ = derivative_from_points(pts3)
            seq1.append(d1)
            seq2.append(d2)
            mu_r = -(romberg_extrapolate(seq1, a)) if len(seq1) else ""
            alpha_r = -(romberg_extrapolate(seq2, a)) if len(seq2) else ""

            # Append new 5-point estimate if next pair exists
            if k + 1 < n_pairs:
                xk1 = (a ** (k + 1)) * h
                ep1 = energy_at(xk1)
                em1 = energy_at(-xk1)
                if ep1 is not None and em1 is not None:
                    pts5 = pts3 + [(round(-xk1, 15), em1), (round(xk1, 15), ep1)]
                    _, _, d3, d4 = derivative_from_points(pts5)
                    seq3.append(d3)
                    seq4.append(d4)

            # Display policy: use only estimates fully available up to this row
            # First row -> zeros; for row k>0 use Romberg on first min(k, len(seq)) elements
            length_to_use = min(k, len(seq3))
            if k == 0 or length_to_use == 0:
                beta_r = 0
            else:
                beta_r = -(romberg_extrapolate(seq3[:length_to_use], a))

            length_to_use_g = min(k, len(seq4))
            if k == 0 or length_to_use_g == 0:
                gamma_r = 0
            else:
                gamma_r = -(romberg_extrapolate(seq4[:length_to_use_g], a))

            rows.append((round(xk, 10), mu_r, alpha_r, beta_r, gamma_r))

        win = tk.Toplevel(self)
        win.title("Generalized Romberg Results")
        tree = ttk.Treeview(win)
        columns = ["F", "μ_R", "α_R", "β_R", "γ_R"]
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        tree["show"] = "headings"
        for r in rows:
            tree.insert("", "end", values=r)
        tree.pack(expand=True, fill="both")

    def create_widgets(self):
        self.label_field = tk.Label(self, text="Enter electric field [a.u.]:")
        self.label_field.grid(row=0, column=0, sticky="e")
        self.field = tk.Entry(self)
        self.field.grid(row=0, column=1)
        self.field.insert(END, "0.001")

        self.label_a = tk.Label(self, text="Parameter a (>1):")
        self.label_a.grid(row=1, column=0, sticky="e")
        self.entry_a = tk.Entry(self)
        self.entry_a.grid(row=1, column=1)
        self.entry_a.insert(END, "1.4")

        iter_frame = tk.Frame(self)
        iter_frame.grid(row=2, column=2, rowspan=3, sticky="n")

        self.table_button = tk.Button(self, text="Show Results Table", command=self.open_results_table)
        self.table_button.grid(row=18, column=0, columnspan=2)

        tk.Label(iter_frame, text="Number of pairs (k):").pack(anchor="w")
        for val, txt in [("1", "1 pair"), ("2", "2 pairs"), ("3", "3 pairs"), ("4", "4 pairs"), ("5", "5 pairs")]:
            tk.Radiobutton(iter_frame, text=txt, variable=self.rb_var, value=val,
                           command=self.update_entries_state).pack(anchor="w")

        self.entries = []
        self.entries_zero = []

        labels = [
            "E(+h)", "E(-h)",
            "E(+a*h)", "E(-a*h)",
            "E(+a^2*h)", "E(-a^2*h)",
            "E(+a^3*h)", "E(-a^3*h)",
            "E(+a^4*h)", "E(-a^4*h)",
        ]

        tk.Label(self, text="E(0):").grid(row=2, column=0, sticky="e")
        entry_zero = tk.Entry(self)
        entry_zero.grid(row=2, column=1)
        self.entries_zero.append(entry_zero)
        self.entries_zero[0].insert(END, "0")

        for i, label in enumerate(labels):
            tk.Label(self, text=label + ":").grid(row=3 + i, column=0, sticky="e")
            entry = tk.Entry(self)
            entry.grid(row=3 + i, column=1)
            self.entries.append(entry)
            entry.insert(END, "0")


def romberg_window():
    win = tk.Toplevel()
    app = Romberg(master=win)
    app.master.title("Generalized Romberg Procedure")
    app.master.geometry("800x600")
    app.grab_set()
