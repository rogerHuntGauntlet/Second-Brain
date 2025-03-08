import numpy as np

# Generate a random 1536-dimensional vector
vector = np.random.normal(0, 0.1, 1536)

# Normalize the vector to have unit length (important for cosine similarity)
vector = vector / np.linalg.norm(vector)

# Convert to list and format as a comma-separated string without scientific notation
def format_number(x):
    # Format number with fixed decimal notation (no scientific notation)
    return f"{x:f}"

vector_str = ','.join(format_number(x) for x in vector)

print(f"Vector length: {len(vector)}\n")
print("First 10 values:")
print([format_number(x) for x in vector[:10]])
print("\nFormatted vector (copy this):")
print(vector_str) 