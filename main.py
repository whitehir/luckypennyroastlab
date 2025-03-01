import multiprocessing

def run_max31865_display():
  import subprocess
  subprocess.run(["python", "max31865_display.py"], check=True)

def run_guiLauncher():
  import subprocess
  subprocess.run(["python", "guiLauncher.py"])

if __name__ == "__main__":
	run_max31865_display()
	run_guiLauncher()

