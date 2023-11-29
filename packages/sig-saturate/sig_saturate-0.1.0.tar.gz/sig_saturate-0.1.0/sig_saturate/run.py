"""run the steamlit app through this python file"""

import os
import subprocess
import argparse


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8501,
                        help="Port number for the Streamlit app")
    args = parser.parse_args()

    # Get absolute path to the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths for app.py, images, and saved_model directories
    app_path = os.path.join(script_dir, "app.py")

    # Run the Streamlit app defined at app_path
    cmd = ["python", "-m", "streamlit", "run", "--server.port", str(args.port), app_path]
    subprocess.call(cmd)

if __name__ == "__main__":
    run()