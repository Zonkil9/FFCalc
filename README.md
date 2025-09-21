# FFCalc

**FFCalc** is a Python program with a simple GUI for obtaining electric properties using the results of calculations
performed using the finite-field method. **FFCalc** is able to calculate the dipole moment μ, the dipole polarizability
α, the first-order hyperpolarizability β, and the second-order hyperpolarizability γ. As of now, the program can provide
only the diagonal terms of the mentioned properties using either single (1F), double (2F), or triple (3F) values of the
electric field.

The **FFCalc** program is designed as a calculator for use with already obtained energy results using a different
software. It does not have any capabilities to obtain the energies; see the Background section for more information.

## Background

For some computational chemistry methods, the analytical calculations of electric properties are too expensive or even
might not yet be available. In such situations, the numerical finite-field approach can be useful.

The finite-field approach was presented
in [Bartlett, R. J., & Purvis, G. D. (1979), Phys. Rev. A, 20(4), 1313–1322](https://doi.org/10.1103/PhysRevA.20.1313).
It is based on the idea that the molecule's energy changes while perturbed by a static external electric field; thus, it
provides information about the molecule's response to its presence.

Below is an example of the calculations you need to perform, explained in the 4 steps below:

1. Calculate the energy of H<sub>2</sub>O using your favorite method, basis set, and computational chemistry software,
   e.g., `Orca`, `Gaussian`, `Dalton`, `Dirac`, `QChem`, `Psi4`, etc.
2. Now perform the same calculations but with the presence of an external electric field for the X vector direction.
   Most computational chemistry software packages have this feature. For example, in `Orca`, you need to add the
   following lines:
    ```sh
    %scf
       EField  0.0001, 0.0, 0.0
    end
    ```
   The value of F should be small, e.g., `0.0001 a.u.`
3. Perform the calculations again but with the negative value of an external electric field, i.e., if you started with
   `0.0001 a.u.`, change it to `-0.0001 a.u.`
4. Now repeat the same calculations for the Y and Z vector directions
5. Finally, paste the obtained energy values into **FFCalc**. You will be able to obtain the dipole moment μ and the
   dipole polarizability α

There is a set of formulas for calculating the higher-order electric properties using double (2F), triple (3F), etc.,
values of an external electric field. If you want to calculate the first-order hyperpolarizability β and the
second-order hyperpolarizability γ, you need to repeat the calculations using `0.0002 a.u.` and/or `0.0003 a.u.`. Also,
the lower-order electric properties will be more accurate.

An important reminder: to obtain accurate results of electric properties, one should choose the method that includes the
electron correlation and the basis set with diffuse functions.

## Generalized Romberg Procedure (GR)

The `romberg.py` module adds a dedicated GUI window (opened from the main app via the “GR Procedure” button) that
implements the generalized Romberg differentiation procedure to obtain derivatives of the energy at F = 0 using energy
values computed at geometrically spaced fields ±a^k h (k = 0, 1, …). For details,
see: [Medved', M. et al. (2007), J. Mol. Struct. THEOCHEM, 847, 39-46](https://doi.org/10.1016/j.theochem.2007.08.028).

Implementation details:

- Local derivative estimates at F = 0 are evaluated from symmetric sets of points using Fornberg’s finite-difference
  weights for nonuniform grids,
- Romberg extrapolation is performed with ratio a and powers a^(2j) appropriate for central stencils,
- Typical choices are h ≈ 0.001-0.003 a.u. and a in the range 1.2–1.6; ensure the field remains within your method’s
  linear response regime.

## Program requirements

The base program requires the `tkinter` package to work. It usually comes pre-installed with Python. If you do not have
it, it can be installed using the system package manager. For example:

* Ubuntu/Debian

```bash
sudo apt install python3-tk
```

* Fedora

```bash
sudo dnf install python3-tkinter
```

* macOS (Homebrew)

```bash
brew install python-tk
```

For the GR Procedure window (`romberg.py`), the program also requires `numpy`:

```bash
pip install numpy
```

## Usage

Start the main GUI:

```bash
python FFCalc.py
```

Classic finite-field workflow (1F/2F/3F):

- Select 1F, 2F or 3F in the main window, paste energies for X, Y, Z directions and E(F0),
- Enter the field value F,
- Click `Calculate properties` and optionally `Save results`.

Generalized Romberg Procedure (GR):

- In the main window, click `GR Procedure` to open the Romberg GUI,
- In the GR window set the base field h and the ratio a (> 1),
- Select the number of pairs (k); only enabled inputs are read (inactive ones are ignored),
- Enter E(0) and energies for enabled pairs: E(±h), E(±a h), E(±a^2 h), …,
- Click `Show Results Table` to inspect the Romberg-extrapolated sequences μ_R, α_R, β_R, γ_R as k increases.
