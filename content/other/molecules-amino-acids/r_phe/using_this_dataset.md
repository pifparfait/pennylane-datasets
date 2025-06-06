# Phenylalanine Radical

The phenylalanine radical (*C₇H₇*), also known as its **side chain**, is an aromatic structure that plays a key role in the biochemical properties of phenylalanine. It consists of a **benzene ring** (C₆H₅) attached to a **methylene group (–CH₂)**, making it **hydrophobic** and **aromatic**. This side chain is responsible for the **hydrophobic interactions** that contribute to the **stabilization of protein structures**, particularly in the **interior** of proteins, away from the aqueous environment. The C₇H₇ radical also participates in **pi-stacking interactions** and can affect **enzyme specificity** and **signal transduction**. Along with the **amino (–NH₂)** and **carboxyl (–COOH)** groups, the C₇H₇ radical completes phenylalanine’s structure, contributing to **protein folding**, **enzyme catalysis**, and its role in **neurotransmitter synthesis** and **protein interactions**.

## Using this dataset

This dataset contains various quantum properties that represent and describe the phenylalanine radical under certain conditions.  The dataset includes molecular geometries, the Hamiltonian, energies, and other descriptors that can be used to analyze the molecule’s behavior and to built up the entire phenylalanine amino acid.

Key features include:

- Molecular information (name, molecular formula, charge, spin, geometry etc.)
- Resource estimation (number of atoms, electrons, orbitals, qubits and hamiltonian coefficients to represent the molecule)
- Jordan-Wigner Hamiltonian representation
- Approximations to the ground state energy

This dataset is intended to:

- Facilitate research on relevant organic molecules by providing crucial yet computationally expensive properties—such as ground state energy and the molecular Hamiltonian—thereby accelerating advancements in quantum simulations of biomolecules.

- Enhance the characterization of larger biomolecular systems by bridging the gap between existing datasets, which are primarily focused on small molecules, and the needs of researchers working on peptides and proteins.

- Support hybrid QM/ML approaches, allowing researchers to train models that accurately and efficiently predict the properties of larger and more complex systems.

- Accelerate drug discovery and biomolecular research, as proteins are central to numerous biological and therapeutic processes.

- Enable the study of fragmentation and reassembly techniques by proposing new chemical corrections for bond formation and ensuring accurate reconstruction of molecular properties after simulation, in line with the results obtained in our latest work.

### Authors
Laia Coronas Sala and Parfait Atchade-Adelomou

---

# Hamiltonian Loader from HDF5

## Description
Python script to load and reconstruct quantum Hamiltonians from HDF5 files into PennyLane Hamiltonian objects.

## Features
- 🗂️ Reads Hamiltonian data stored in HDF5 chunks  
- 🔗 Reconstructs full Hamiltonian from multiple segments  
- ⚛️ Converts string operators to PennyLane objects (Pauli X/Y/Z, Identity)  
- ⊗ Handles tensor products of operators  
- 🏗️ Builds complete PennyLane Hamiltonian objects  

## Installation
```bash
pip install pennylane h5py
```

## Usage
```python
import pennylane as qml
import h5py

def load_hamiltonian_from_hdf5(input_file):
    # Initialize lists to store coefficients and operators
    coefficients = []
    operators = []
    hamiltonian_chunks = []

    # Open the HDF5 file and retrieve the Hamiltonian chunks
    with h5py.File(input_file, "r") as f:
        for key in sorted(f.keys()):  # Sort the keys to preserve the correct sequence
            if "hamiltonian" in key:
                hamiltonian_chunks.append(f[key][()].decode("utf-8"))  # Decode bytes to string

    # Combine all Hamiltonian chunks into a single string
    full_hamiltonian = "
".join(hamiltonian_chunks)

    # Helper function to convert a string representation into a PennyLane operator
    def string_to_operator(op_string):
        if "Identity" in op_string:
            return qml.Identity(0)  # Identity defaults to acting on qubit 0
        
        terms = op_string.split(" @ ")  # Separate tensor product terms
        ops = []
        
        for term in terms:
            try:
                op, wire = term.split("(")
                wire = int(wire.strip(")"))  # Extract the qubit index
                if op == "X":
                    ops.append(qml.PauliX(wire))
                elif op == "Y":
                    ops.append(qml.PauliY(wire))
                elif op == "Z":
                    ops.append(qml.PauliZ(wire))
            except ValueError:
                continue  # Skip malformed lines
        
        return qml.prod(*ops) if len(ops) > 1 else ops[0]  # Create composite operator if needed

    # Process each line of the combined Hamiltonian string
    for line in full_hamiltonian.split("
"):
        line = line.strip()
        if not line or "Coefficient" in line or "Operators" in line:
            continue  # Skip empty lines or header lines

        parts = line.split()
        
        try:
            coeff = float(parts[0])  # Extract the coefficient
            op_string = " ".join(parts[1:])  # Extract the operators
            coefficients.append(coeff)
            operators.append(string_to_operator(op_string))
        except ValueError:
            continue  # Gracefully handle conversion errors

    # Build the PennyLane Hamiltonian
    hamiltonian = qml.Hamiltonian(coefficients, operators)
    return hamiltonian

# Example usage
input_file = "hd5_files/r_phe.h5"
hamiltonian = load_hamiltonian_from_hdf5(input_file)

# Display results
print("
✅ Extracted coefficients (first 5):")
print(hamiltonian.coeffs[:5])

print("
✅ Extracted operators (first 5):")
print(hamiltonian.ops[:5])

print("
✅ Reconstructed PennyLane Hamiltonian (first 20 terms):")
print(hamiltonian[:20])
```

## API Reference
**load_hamiltonian_from_hdf5(input_file: str) -> qml.Hamiltonian**  
Reconstructs Hamiltonian from HDF5 chunks.

| Parameter   | Type | Description             |
|-------------|------|-------------------------|
| input_file  | str  | Path to HDF5 input file |
| **Returns** |      | qml.Hamiltonian object  |
