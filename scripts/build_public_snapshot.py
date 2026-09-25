"""Rebuild fixed public snapshot from current collection inputs."""
import subprocess,sys
subprocess.run([sys.executable,'pipeline/run_pipeline.py'],check=True)
