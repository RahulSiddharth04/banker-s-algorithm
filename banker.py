import tkinter as tk
from tkinter import messagebox

class BankersAlgorithmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm Simulation")
        self.root.geometry("800x800")

        self.num_processes = 0
        self.num_resources = 0
        self.allocation_entries = []
        self.max_entries = []
        self.available_entries = []
        self.allocation = []
        self.maximum = []
        self.available = []
        self.need = []

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Banker's Algorithm Simulation", font=("Helvetica", 18))
        title.grid(row=0, column=0, columnspan=6, pady=10)

        # Number of processes and resources inputs
        tk.Label(self.root, text="Number of Processes:").grid(row=1, column=0, padx=5, pady=5)
        self.num_processes_entry = tk.Entry(self.root)
        self.num_processes_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Number of Resources:").grid(row=1, column=2, padx=5, pady=5)
        self.num_resources_entry = tk.Entry(self.root)
        self.num_resources_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(self.root, text="Set", command=self.set_processes_resources).grid(row=1, column=4, padx=5, pady=5)

    def set_processes_resources(self):
        try:
            self.num_processes = int(self.num_processes_entry.get())
            self.num_resources = int(self.num_resources_entry.get())

            if self.num_processes <= 0 or self.num_resources <= 0:
                raise ValueError("Numbers must be positive integers")

            self.create_matrix_inputs()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def create_matrix_inputs(self):
        # Allocation Matrix
        tk.Label(self.root, text="Allocation Matrix").grid(row=2, column=0, columnspan=2, pady=5)
        self.allocation_entries = [[tk.Entry(self.root, width=5) for _ in range(self.num_resources)] for _ in range(self.num_processes)]
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                self.allocation_entries[i][j].grid(row=3+i, column=j)

        # Max Matrix
        tk.Label(self.root, text="Max Matrix").grid(row=2, column=2, columnspan=2, pady=5)
        self.max_entries = [[tk.Entry(self.root, width=5) for _ in range(self.num_resources)] for _ in range(self.num_processes)]
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                self.max_entries[i][j].grid(row=3+i, column=2+j)

        # Available Resources
        tk.Label(self.root, text="Available Resources").grid(row=2, column=4, columnspan=2, pady=5)
        self.available_entries = [tk.Entry(self.root, width=5) for _ in range(self.num_resources)]
        for j in range(self.num_resources):
            self.available_entries[j].grid(row=3, column=4+j)

        # Calculate Button
        tk.Button(self.root, text="Calculate Safe Sequence", command=self.calculate_safe_sequence).grid(row=4+self.num_processes, column=0, columnspan=6, pady=10)

    def calculate_safe_sequence(self):
        try:
            self.allocation = [[int(self.allocation_entries[i][j].get()) for j in range(self.num_resources)] for i in range(self.num_processes)]
            self.maximum = [[int(self.max_entries[i][j].get()) for j in range(self.num_resources)] for i in range(self.num_processes)]
            self.available = [int(self.available_entries[j].get()) for j in range(self.num_resources)]

            self.need = [[self.maximum[i][j] - self.allocation[i][j] for j in range(self.num_resources)] for i in range(self.num_processes)]

            safe_sequence = self.is_safe_state()
            if safe_sequence:
                messagebox.showinfo("Safe Sequence", "The system is in a safe state.\nSafe Sequence: " + ' -> '.join(safe_sequence))
            else:
                messagebox.showwarning("No Safe Sequence", "The system is not in a safe state.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for matrices.")

    def is_safe_state(self):
        work = self.available[:]
        finish = [False] * self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            allocated = False
            for i in range(self.num_processes):
                if not finish[i]:
                    if all(self.need[i][j] <= work[j] for j in range(self.num_resources)):
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(f"P{i+1}")
                        allocated = True
            if not allocated:
                return None
        return safe_sequence

if __name__ == "__main__":
    root = tk.Tk()
    app = BankersAlgorithmApp(root)
    root.mainloop()
