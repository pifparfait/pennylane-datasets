$$
J_{xy}\sum_{\langle i,j\rangle}(\sigma_i^x\sigma_j^x+\sigma_i^y\sigma_j^y) + J_z\sum_{\langle i,j\rangle} \sigma_i^z \sigma_j^z
$$

Hamiltonians for the spin systems (under the Jordan-Wigner transformation for the Fermi Hubbard model and [Binary Bosonic mapping](https://arxiv.org/abs/2105.12563) for the Bose Hubbard Model).

| Name            | Type              | Description                                                    |
|-----------------|-------------------|----------------------------------------------------------------|
| `hamiltonian`     | list[`Hamiltonian`] | Hamiltonian of the system in the Pauli basis                   |
| `ground_energies` | `numpy.ndarray`     | Ground state energies of each configuration of the spin system |
| `ground_states`   | `numpy.ndarray`     | Ground state of each configuration of the spin system          |