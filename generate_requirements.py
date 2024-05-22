import subprocess

# List of specific packages you want to include in requirements.txt
packages = [
    "flask",
    "python-dotenv",
    "openai",
    "aiohttp",
    "requests"
]

# Get the output of `pip freeze`
result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
installed_packages = result.stdout.splitlines()

# Filter only the specified packages
filtered_packages = [pkg for pkg in installed_packages if any(pkg.startswith(package) for package in packages)]

# Write the filtered packages to requirements.txt
with open("requirements.txt", "w") as file:
    file.write("\n".join(filtered_packages))

print("requirements.txt has been updated with the specified packages.")
