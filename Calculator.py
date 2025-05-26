import tkinter as tk
import math
from tkinter import ttk

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("550x600")
        self.root.configure(bg="#f0f0f0")
        
        #?Making Icons and Themes
        self.root.iconbitmap(default=None)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        #!Variables
        self.current_expression = ""
        self.total_expression = ""
        self.stored_variables = {}
        self.history = []
        
        #!Creating Frames
        self.create_frames()
        
        #!Creating Displays
        self.create_display()
        self.create_history_display()
        self.create_variable_display()
        
        #!Making the buttons
        self.create_buttons()
        
        #!Allowing the program to use the keyboard
        self.bind_keys()
        
    def create_frames(self):
        self.display_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.display_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.history_frame = tk.LabelFrame(self.root, text="History", bg="#f0f0f0", font=("Arial", 10, "bold"))
        self.history_frame.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.variables_frame = tk.LabelFrame(self.root, text="Variables", bg="#f0f0f0", font=("Arial", 10, "bold"))
        self.variables_frame.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
    def create_display(self):
        #\Label to display the total expression
        self.total_expression_label = tk.Label(
            self.display_frame, 
            text="", 
            anchor="e", 
            bg="#f0f0f0", 
            fg="#5e5e5e", 
            font=("Arial", 12)
        )
        self.total_expression_label.pack(expand=True, fill="both")
        
        #\Entry to display the current expression
        self.current_expression_entry = tk.Entry(
            self.display_frame, 
            font=("Arial", 20, "bold"), 
            justify="right", 
            bd=5, 
            relief=tk.RIDGE,
            bg="white"
        )
        self.current_expression_entry.pack(expand=True, fill="both", pady=5)
        self.current_expression_entry.focus_set()
        
    def create_history_display(self):
        self.history_listbox = tk.Listbox(
            self.history_frame, 
            height=5, 
            font=("Arial", 10), 
            bg="white", 
            selectbackground="#a6a6a6"
        )
        self.history_listbox.pack(expand=True, fill="both", padx=5, pady=5)
        self.history_listbox.bind("<Double-Button-1>", self.use_history_item)
        
    def create_variable_display(self):
        self.variables_frame.columnconfigure(0, weight=1)
        self.variables_frame.columnconfigure(1, weight=2)
        self.variables_frame.columnconfigure(2, weight=1)
        
        #\Variable name label
        tk.Label(self.variables_frame, text="Name:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        #\Variable name entry
        self.var_name_entry = tk.Entry(self.variables_frame, width=10)
        self.var_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        
        #\Store button
        tk.Button(
            self.variables_frame, 
            text="Store", 
            bg="#4285f4", 
            fg="white", 
            activebackground="#5a95f5", 
            font=("Arial", 10), 
            command=self.store_variable
        ).grid(row=0, column=2, sticky="e", padx=5, pady=2)
        
        #\Variables listbox
        self.variables_listbox = tk.Listbox(
            self.variables_frame, 
            height=4, 
            font=("Arial", 10), 
            bg="white", 
            selectbackground="#a6a6a6"
        )
        self.variables_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.variables_listbox.bind("<Double-Button-1>", self.use_variable)
        
    def create_buttons(self):
        self.buttons_frame.columnconfigure(tuple(range(6)), weight=1)
        self.buttons_frame.rowconfigure(tuple(range(5)), weight=1)

        #\Define button details: text, row, column, color
        button_data = [
            #\Scientific functions row
            ("sin", 0, 0, "#ff9500"), ("cos", 0, 1, "#ff9500"), ("tan", 0, 2, "#ff9500"), 
            ("π", 0, 3, "#ff9500"), ("e", 0, 4, "#ff9500"), ("log", 0, 5, "#ff9500"),
            
            #\Numbers and operations
            ("7", 1, 0, "white"), ("8", 1, 1, "white"), ("9", 1, 2, "white"), 
            ("÷", 1, 3, "#ff9500"), ("√", 1, 4, "#ff9500"), ("x²", 1, 5, "#ff9500"),
            
            ("4", 2, 0, "white"), ("5", 2, 1, "white"), ("6", 2, 2, "white"), 
            ("×", 2, 3, "#ff9500"), ("(", 2, 4, "#ff9500"), (")", 2, 5, "#ff9500"),
            
            ("1", 3, 0, "white"), ("2", 3, 1, "white"), ("3", 3, 2, "white"), 
            ("-", 3, 3, "#ff9500"), ("^", 3, 4, "#ff9500"), ("mod", 3, 5, "#ff9500"),
            
            ("0", 4, 0, "white"), (".", 4, 1, "white"), ("AC", 4, 2, "#e8eaed"), 
            ("+", 4, 3, "#ff9500"), ("=", 4, 4, "#4285f4", 2)  # span 2 columns
        ]

        #\Create and place buttons
        for data in button_data:
            if len(data) == 5:
                text, row, col, color, columnspan = data
                self.create_button(text, row, col, bg_color=color, columnspan=columnspan)
            else:
                text, row, col, color = data
                self.create_button(text, row, col, bg_color=color)
                
    def create_button(self, text, row, col, bg_color, columnspan=1):
        button = tk.Button(
            self.buttons_frame,
            text=text,
            bg=bg_color,
            fg="black" if bg_color in ["white", "#e8eaed"] else "white",
            font=("Arial", 14),
            borderwidth=0,
            relief="raised",
            activebackground="#e0e0e0" if bg_color in ["white", "#e8eaed"] else "#a0a0a0",
            command=lambda: self.button_click(text)
        )
        button.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=2, pady=2)
        
    def bind_keys(self):
        #\Bind keyboard inputs
        self.root.bind("<Return>", lambda event: self.evaluate())
        self.root.bind("<BackSpace>", lambda event: self.backspace())
        self.root.bind("<Escape>", lambda event: self.clear())
        
        #\Bind digits and operators
        for key in "0123456789":
            self.root.bind(key, lambda event, digit=key: self.button_click(digit))
            
        #\Bind operators
        self.root.bind("+", lambda event: self.button_click("+"))
        self.root.bind("-", lambda event: self.button_click("-"))
        self.root.bind("*", lambda event: self.button_click("×"))
        self.root.bind("/", lambda event: self.button_click("÷"))
        self.root.bind("^", lambda event: self.button_click("^"))
        self.root.bind(".", lambda event: self.button_click("."))
        self.root.bind("(", lambda event: self.button_click("("))
        self.root.bind(")", lambda event: self.button_click(")"))
        
    def button_click(self, text):
        #\Handle different button clicks
        if text == "=":
            self.evaluate()
        elif text == "AC":
            self.clear()
        elif text == "π":
            self.current_expression += "π"
        elif text == "e":
            self.current_expression += "e"
        elif text == "sin":
            self.current_expression += "sin("
        elif text == "cos":
            self.current_expression += "cos("
        elif text == "tan":
            self.current_expression += "tan("
        elif text == "log":
            self.current_expression += "log("
        elif text == "√":
            self.current_expression += "sqrt("
        elif text == "x²":
            self.current_expression += "^2"
        elif text == "mod":
            self.current_expression += "%"
        else:
            self.current_expression += text
        self.update_display()
    
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_display()
    
    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_display()
        
    def update_display(self):
        self.total_expression_label.config(text=self.total_expression)
        self.current_expression_entry.delete(0, tk.END)
        self.current_expression_entry.insert(0, self.current_expression)
    
    def update_history(self):
        #\Keep only the last 10 calculations
        if len(self.history) > 10:
            self.history.pop(0)
        
        #\Update the history listbox
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, item)
    
    def update_variables_display(self):
        self.variables_listbox.delete(0, tk.END)
        for name, value in self.stored_variables.items():
            self.variables_listbox.insert(tk.END, f"{name} = {value}")
    
    def store_variable(self):
        var_name = self.var_name_entry.get().strip()
        if not var_name:
            return
        
        try:
            value = self.evaluate_expression(self.current_expression)
            self.stored_variables[var_name] = value
            self.update_variables_display()
            self.var_name_entry.delete(0, tk.END)
        except Exception as e:
            self.current_expression_entry.delete(0, tk.END)
            self.current_expression_entry.insert(0, f"Error: {str(e)}")
            self.current_expression = ""
    
    def use_variable(self, event):
        if not self.variables_listbox.curselection():
            return
        
        selected_item = self.variables_listbox.get(self.variables_listbox.curselection())
        var_name = selected_item.split(" = ")[0]
        self.current_expression += var_name
        self.update_display()
    
    def use_history_item(self, event):
        if not self.history_listbox.curselection():
            return
            
        selected_item = self.history_listbox.get(self.history_listbox.curselection())
        expression = selected_item.split(" = ")[0]
        self.current_expression = expression
        self.update_display()
    
    def evaluate_expression(self, expression):
        #\Replace special constants and functions
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))
        
        #\Replace custom functions
        expression = expression.replace("sin(", "math.sin(")
        expression = expression.replace("cos(", "math.cos(")
        expression = expression.replace("tan(", "math.tan(")
        expression = expression.replace("log(", "math.log10(")
        expression = expression.replace("sqrt(", "math.sqrt(")
        expression = expression.replace("^", "**")
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        
        #\Replace stored variables with their values
        for var_name, value in self.stored_variables.items():
            expression = expression.replace(var_name, str(value))
            
        # \Evaluate the expression
        try:
            return eval(expression)
        except Exception as e:
            raise ValueError(str(e))
    
    def evaluate(self):
        if not self.current_expression:
            return
            
        try:
            result = self.evaluate_expression(self.current_expression)
            
            #\Format result for display
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    #\Limit to 10 decimal places if needed
                    result = round(result, 10)
                    #\Remove extra zeros
                    result = str(result).rstrip('0').rstrip('.') if '.' in str(result) else str(result)
            
            #\Add to history
            history_item = f"{self.current_expression} = {result}"
            self.history.append(history_item)
            self.update_history()
            
            #\Update display
            self.total_expression = self.current_expression
            self.current_expression = str(result)
            self.update_display()
            
        except Exception as e:
            self.current_expression_entry.delete(0, tk.END)
            self.current_expression_entry.insert(0, f"Error: {str(e)}")
            self.current_expression = ""


root = tk.Tk()
calculator = ScientificCalculator(root)
root.minsize(550, 600)
root.mainloop()
