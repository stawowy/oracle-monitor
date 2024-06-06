from onetime import start_monitoring


class Menu:
    def __init__(self):
        self.state = 'main_menu'

    def run(self):
        while True:
            if self.state == 'main_menu':
                self.main_menu()
            elif self.state == 'add_monitor':
                self.add_monitor()
            elif self.state == 'delete_monitor':
                self.delete_monitor()
            elif self.state == 'one_time_monitoring':
                self.one_time_monitoring()
            elif self.state == 'exit':
                print("Exiting program.")
                break
            else:
                print("Invalid state.")
                break

    def main_menu(self):
        print("Main Menu:")
        print("1. Add Monitoring Process")
        print("2. Delete Monitoring Process")
        print("3. Perform One-Time Monitoring")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            self.state = 'add_monitor'
        elif choice == '2':
            self.state = 'delete_monitor'
        elif choice == '3':
            self.state = 'one_time_monitoring'
        elif choice == '4':
            self.state = 'exit'
        else:
            print("Invalid choice. Please try again.")

    def add_monitor(self):
        print("Adding Monitoring Process.")
        interval = input("Specify the frequency of monitoring (how many hours apart each check should be): ")
        to_email = input("Provide an email address to receive the report: ")

        

        self.state = 'main_menu'

    def delete_monitor(self):
        confirm = input(f"Are you sure you want to delete {self.monitoring.get_name()}? (yes/no): ").strip().lower()



        self.state = 'main_menu'

    def one_time_monitoring(self):
        print("Performing One-Time Monitoring:")
        to_email = input("Provide an email address to receive the report: ")
        start_monitoring(to_email)
        print("Process started. Expect an email in a few minutes.")
        self.state = 'main_menu'

    def get_monitoring(self):
        return self.monitoring
