# FFCalc
**FFCalc** is a Python program with a simple GUI for obtaining electric properties using the results of calculations performed using the finite-field method. **FFCalc** is able to calculate the dipole moment μ, the dipole polarizability α, the first-order hyperpolarizability β, and the second-order hyperpolarizability γ. As of now, the program can provide only the diagonal terms of the mentioned properties using either single (1F), double (2F), or triple (3F) values of the electric field.

The **FFCalc** program is designed as a mere calculator for use with already obtained energy results using a different software. It does not have any capabilities to obtain the energies; see the Background section for more information.

## Background

For some computational chemistry methods, the analytical calculations of electric properties are too expensive or even might not yet be available. In such situations, the numerical finite-field approach can be useful.

The finite-field approach was presented in [Bartlett, R. J., & Purvis, G. D. (1979), Phys. Rev. A, 20(4), 1313–1322](https://doi.org/10.1103/PhysRevA.20.1313). It is based on the idea that the molecule's energy changes while perturbed by a static external electric field; thus, it provides information about the molecule's response to its presence. 

Below is an example of the calculations you need to perform, explained in the 4 steps below:

1. Calculate the energy of H<sub>2</sub>O using your favorite method, basis set, and computational chemistry software, e.g., `Orca`, `Gaussian`, `Dalton`, `Dirac`, `QChem`, `Psi4`, etc.
2. Now perform the same calculations but with the presence of an external electric field for the X vector direction. Most computational chemistry software packages have this feature. For example, in `Orca`, you need to add the following lines:
    ```sh
    %scf
       EField  0.0001, 0.0, 0.0
    end
    ```
    The value of F should be small, e.g., `0.0001 a.u.`
3. Perform the calculations again but with the negative value of an external electric field, i.e., if you started with `0.0001 a.u.`, change it to `-0.0001 a.u.`
4. Now repeat the same calculations for the Y and Z vector directions
5. Finally, paste the obtained energy values into **FFCalc**. You will be able to obtain the dipole moment μ and the dipole polarizability α

There is a set of formulas for calculating the higher-order electric properties using double (2F), triple (3F), etc., values of an external electric field. If you want to calculate the first-order hyperpolarizability β and the second-order hyperpolarizability γ, you need to repeat the calculations using `0.0002 a.u.` and/or `0.0003 a.u.`. Also, the lower-order electric properties will be more accurate.

An important reminder: to obtain accurate results of electric properties, one should choose the method that includes the electron correlation and the basis set with diffuse functions.

## Program requirements

The program requires `matplotlib` and `tkinter` packages to work. 

The `matplotlib` package can be installed through `pip`:
```bash
pip install matplotlib
```

`tkinter` can be installed using the system package manager. For example:

* Ubuntu/Debian
```bash
sudo apt install python3-tk
```

* Fedora
```bash
sudo dnf install python3-tkinter
```

* MacOS
```bash
brew install python-tk
```

## Usage

Simply execute the program using:
```bash
python FFCalc.py
```

The GUI should appear. You can paste your input data (calculated using different software) and then click `Calculate properties` and `Save results`.
