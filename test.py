from qiskit import *

circuit = QuantumCircuit(2,2)
quantum_register = QuantumRegister(2)
classical_resiter = ClassicalRegister(2)
circuit = QuantumCircuit(quantum_register, classical_resiter)

circuit.draw()
circuit.draw(output='mpl')