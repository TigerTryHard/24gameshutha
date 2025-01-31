import tkinter as tk
from tkinter import messagebox
import random
import itertools

class Game24:
    def __init__(self, root):
        self.root = root
        self.root.title("Math 24 Game")
        self.root.geometry("400x500")
        self.root.config(bg="#FFFFFF")  # Background in white
        
        self.target = 24
        self.generate_numbers()
        
        # Title
        tk.Label(self.root, text="🎯 Math 24 Game 🎲", font=("Arial", 24, "bold"), bg="#FFFFFF", fg="#333333").pack(pady=10)
        
        # Numbers display
        self.numbers_label = tk.Label(self.root, text=self.format_numbers(), font=("Arial", 16), bg="#FFFFFF", fg="#333333")
        self.numbers_label.pack(pady=10)
        
        # Input field
        tk.Label(self.root, text="🖋️ Enter your expression:", font=("Arial", 14), bg="#FFFFFF", fg="#333333").pack(pady=5)
        self.input_field = tk.Entry(self.root, font=("Arial", 14), width=20)
        self.input_field.pack(pady=5)
        
        # Buttons
        tk.Button(self.root, text="✔️ Submit", font=("Arial", 14), bg="#ADD8E6", fg="#333333", command=self.check_answer).pack(pady=10)
        tk.Button(self.root, text="🔄 Random Numbers", font=("Arial", 14), bg="#FFD700", fg="#333333", command=self.randomize_numbers).pack(pady=10)
        tk.Button(self.root, text="📖 Show Solutions", font=("Arial", 14), bg="#90EE90", fg="#333333", command=self.show_solutions).pack(pady=10)

    def generate_numbers(self):
        """Generate a random set of 4 numbers."""
        self.numbers = [random.randint(1, 9) for _ in range(4)]

    def format_numbers(self):
        """Format numbers as a string."""
        return "Numbers: " + ", ".join(map(str, self.numbers))

    def randomize_numbers(self):
        """Randomize numbers and update the display."""
        self.generate_numbers()
        self.numbers_label.config(text=self.format_numbers())
        self.input_field.delete(0, tk.END)

    def check_answer(self):
        """Check the player's answer."""
        expression = self.input_field.get()
        try:
            # Validate the expression
            if not all(str(num) in expression for num in self.numbers):
                self.show_result("Incorrect", "Incorrect ❌ ")
                return
            
            # Calculate answer from left to right (ignoring order of operations)
            result = self.evaluate_expression(expression)
            
            if result == self.target:
                self.show_result("Correct", "🎉 Your answer is correct!")
            else:
                self.show_result("Incorrect", "😞 Oops! Your answer does not equal 24.")
        except Exception as e:
            self.show_result("Error", "⚠️ Invalid expression! Please try again.")

    def evaluate_expression(self, expression):
        """Evaluate the expression from left to right."""
        tokens = expression.split()  # Split the expression by spaces (assuming the format is a1 op1 a2 op2 a3 ...)
        
        while len(tokens) > 1:
            # Take the first two numbers and the first operator
            num1 = float(tokens.pop(0))
            operator = tokens.pop(0)
            num2 = float(tokens.pop(0))
            
            # Perform the operation and put the result back
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                if num2 == 0:
                    raise ValueError("Cannot divide by zero.")
                result = num1 / num2
            
            # Put the result back into the list
            tokens.insert(0, str(result))
        
        return float(tokens[0])

    def show_solutions(self):
        """Show example solutions."""
        solutions = self.find_solutions()
        if solutions:
            solution_window = tk.Toplevel(self.root)
            solution_window.title("Solutions")
            solution_window.geometry("400x300")
            solution_window.config(bg="#F0F0F0")  # Light gray background
            
            tk.Label(solution_window, text="📖 Here are some solutions:", font=("Arial", 14), bg="#F0F0F0", fg="#333333").pack(pady=10)
            for solution in solutions[:5]:  # Show only the first 5 solutions
                tk.Label(solution_window, text=solution, font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=2)
            
            tk.Button(solution_window, text="Close", font=("Arial", 12), bg="#D3D3D3", fg="#333333", 
                      command=solution_window.destroy).pack(pady=10)
        else:
            messagebox.showinfo("No Solutions", "No solutions found for the current numbers.")

    def find_solutions(self):
        """Find all possible solutions for the given numbers."""
        ops = ['+', '-', '*', '/']
        solutions = []
        for perm in itertools.permutations(self.numbers):
            for op1 in ops:
                for op2 in ops:
                    for op3 in ops:
                        exprs = [
                            f"(({perm[0]} {op1} {perm[1]}) {op2} {perm[2]}) {op3} {perm[3]}",
                            f"({perm[0]} {op1} ({perm[1]} {op2} {perm[2]})) {op3} {perm[3]}",
                            f"{perm[0]} {op1} (({perm[1]} {op2} {perm[2]}) {op3} {perm[3]})",
                            f"{perm[0]} {op1} ({perm[1]} {op2} ({perm[2]} {op3} {perm[3]}))",
                            f"({perm[0]} {op1} {perm[1]}) {op2} ({perm[2]} {op3} {perm[3]})"
                        ]
                        for expr in exprs:
                            try:
                                if abs(eval(expr) - 24) < 1e-6:  # Avoid floating-point issues
                                    solutions.append(expr)
                            except ZeroDivisionError:
                                continue
        return solutions

    def show_result(self, title, message):
        """Show a styled message window."""
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("300x200")
        result_window.config(bg="#FFFFFF")  # White background
        
        # Message
        tk.Label(result_window, text=message, font=("Arial", 14, "bold"), 
                 fg="#4CAF50" if title == "Correct" else "#F44336", bg=result_window["bg"]).pack(pady=30)
        
        # Close button
        tk.Button(result_window, text="Close", font=("Arial", 12), bg="#D3D3D3", fg="#333333", 
                  command=result_window.destroy).pack(pady=10)


class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Math 24 Game")
        self.root.geometry("400x500")
        self.root.config(bg="#FFFFFF")  # White background
        
        # Title
        tk.Label(self.root, text="🎯 Welcome to Math 24 🎲", font=("Arial", 20, "bold"), bg="#FFFFFF", fg="#333333").pack(pady=50)
        
        # Subtitle
        tk.Label(self.root, text="Can you make 24 using 4 numbers?\nLet's find out!", font=("Arial", 14), bg="#FFFFFF", fg="#333333").pack(pady=20)
        
        # Start button
        tk.Button(self.root, text="Start", font=("Arial", 16), bg="#2E8B57", fg="#FFFFFF", 
                  command=self.start_game).pack(pady=30)

    def start_game(self):
        """Start the main game."""
        self.root.destroy()
        main_root = tk.Tk()
        Game24(main_root)
        main_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    StartScreen(root)
    root.mainloop()
