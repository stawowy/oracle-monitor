from menu_module import Menu
import subprocess

print("Welcome to the database monitoring application.")

if __name__ == "__main__":
    print("Initializing target, might take a while.")
    subprocess.call(['sh', '/home/oracle-monitor/ip_finder.sh'])
    menu_instance = Menu()  # Instantiate the menu class
    menu_instance.run()