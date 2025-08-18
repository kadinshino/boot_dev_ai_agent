import sys
import os
import shutil
from pkg.calculator import evaluate
from pkg.render import render


def clean_pycache():
    """Clean up Python cache directories."""
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)

def main():
    """Main function for the calculator application."""
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return
    
    expr = sys.argv[1]
    try:
        result = evaluate(expr)
        fancy_output = render(expr, result)  # Create the box!
        print(fancy_output)  # Print the box instead of raw result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up cache files after execution
        clean_pycache()

if __name__ == "__main__":
    main()