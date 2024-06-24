from qiskit import QuantumCircuit, execute, AerSimulator
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import json

# Define the quantum circuit
qc = QuantumCircuit(6)

# Generate a random key for encryption and authentication
key = np.random.randint(0, 2, 6)

# Convert the key to binary format
bin_key = bin(int(''.join(map(str, key)), 2))[2:].zfill(6)

# Add the key to the quantum circuit
for i, bit in enumerate(bin_key):
    qc.x(i)
    qc.z(i)

# Add the message to the quantum circuit
message = "Hello World"
message_bin = bin(int(message, 2))[2:].zfill(8)
for i, bit in enumerate(message_bin):
    qc.x(i)
    qc.z(i)

# Apply teleportation gates
qc.h(0)
qc.x(1)
qc.r(0, 1, 0)
qc.p(1, 0)

# Measure the qubits
qc.measure_all()

# Run the quantum circuit with AerSimulator
backend = AerSimulator()
job = execute(qc, backend, shots=1024)
result = job.result()
counts = result.get_counts(qc)

# Extract the measurement outcome and decrypt the message
measurement_outcome = max(counts, key=counts.get)
decrypted_message = ''.join('1' if int(b) != int(key[i]) else '0' for i, b in enumerate(measurement_outcome))

print("Decrypted message:", decrypted_message)

# Generate a message authentication code (MAC) using SHA-256
import hashlib

mac = hashlib.sha256(decrypted_message.encode()).hexdigest()
print("MAC:", mac)

# Save the encrypted message and MAC to a JSON file
with open('encrypted_message.json', 'w') as f:
    json.dump({
        "message": decrypted_message,
        "key": bin_key,
        "encrypted_message": measurement_outcome,
        "mac": mac
    }, f)

# Load the JSON file and verify the MAC
with open('encrypted_message.json', 'r') as f:
    data = json.load(f)

decrypted_message_loaded = data["message"]
mac_loaded = data["mac"]

if hashlib.sha256(decrypted_message_loaded.encode()).hexdigest() == mac_loaded:
    print("The message has not been tampered with or corrupted during transmission.")
else:
    print("The message has been tampered with or corrupted during transmission.")

# Alice and Bob's confirmation process

alice_encrypted_message = qc.measure_all()[0]
bob_encrypted_message = qc.measure_all()[1]

alice_decrypted_message = ''.join('1' if int(b) != int(key[i]) else '0' for i, b in enumerate(alice_encrypted_message))
bob_decrypted_message = ''.join('1' if int(b) != int(key[i]) else '0' for i, b in enumerate(bob_encrypted_message))

print("Alice's decrypted message:", alice_decrypted_message)
print("Bob's decrypted message:", bob_decrypted_message)

# Server's confirmation process

server_encrypted_message = qc.measure_all()[2]
server_decrypted_message = ''.join('1' if int(b) != int(key[i]) else '0' for i, b in enumerate(server_encrypted_message))
print("Server's decrypted message:", server_decrypted_message)

# Confirm the security of the message and the server
if alice_decrypted_message == bob_decrypted_message == server_decrypted_message == decrypted_message:
    print("The message is secure and has been confirmed by Alice, Bob, and the server.")
else:
    print("The message has been tampered with or corrupted during transmission.")
