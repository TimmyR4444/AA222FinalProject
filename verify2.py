import subprocess

# Replace 'python' with 'python3' or 'python2' depending on your Python version
python_executable = 'python'

# Path to your Python script
script_path = 'test.py'

# Number of times to run the script
num_runs = 10

# Run the script num_runs times
for i in range(num_runs):
    print(f"Running {i+1}/{num_runs}")
    subprocess.run([python_executable, script_path], check=True)