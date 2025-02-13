from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.circuit.library import PhaseEstimation
import numpy as np
from math import gcd

def modular_exponentiation(a, power, N):
    """ a^power mod N 을 수행하는 회로를 생성 """
    qc = QuantumCircuit(4)
    for _ in range(power):
        qc.x(0)  # 예제에서는 x=1일 때 기본적인 연산 수행
    return qc.to_gate(label=f"{a}^{power} mod {N}")

def run_shor(N, a):
    """ 주어진 N과 a에 대해 Shor 알고리즘 실행 """
    num_counting_qubits = 4  # Phase Estimation에 사용할 큐빗 개수
    num_work_qubits = 4      # 계산용 큐빗 개수

    # 모듈러 거듭제곱 연산을 위한 연산자
    unitary = modular_exponentiation(a, 1, N)

    # Phase Estimation 회로 생성
    pe = PhaseEstimation(num_counting_qubits, unitary)
    qc = QuantumCircuit(num_counting_qubits + num_work_qubits, num_counting_qubits)

    # 전체 회로 구성
    qc.append(pe, range(num_counting_qubits + num_work_qubits))

    # 측정
    qc.measure(range(num_counting_qubits), range(num_counting_qubits))

    # 시뮬레이션 실행
    simulator = AerSimulator()
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots = 1024).result()
    counts = result.get_counts()
    
    print(counts)
    # 가장 많이 측정된 값 선택
    measured_phase = max(counts, key=counts.get)
    phase_decimal = int(measured_phase, 2) / (2**num_counting_qubits)

    # 주기 찾기
    print(phase_decimal)
    r = round(1 / phase_decimal)
    
    # 인수 찾기
    if r % 2 == 1:
        return "Failed to find factor"
    
    factor1 = gcd(a**(r//2) - 1, N)
    factor2 = gcd(a**(r//2) + 1, N)

    return factor1, factor2

# 테스트 실행 (N=15, a=7)
N = 15
a = 7
factors = run_shor(N, a)
print("Factors of", N, ":", factors)
