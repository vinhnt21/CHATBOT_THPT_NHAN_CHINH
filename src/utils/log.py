def success(message: str) -> None:
    print(f"\033[92m[SUCCESS] {message}\033[0m")

def warn(message: str) -> None:
    print(f"\033[93m[WARNING] {message}\033[0m")

def error(message: str) -> None:
    print(f"\033[91m[ERROR] {message}\033[0m")
