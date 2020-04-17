import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
from tkinter import messagebox
from maze_window import MazeWindow


class MenuWindow(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		# Set window configuration
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.parent.title("Main Menu")
		self.parent.resizable(False, False)

		# Top frame
		self.top_frame = tk.LabelFrame(self.parent, text="Grid options")
		self.top_frame.pack(padx=5, pady=(5,0), fill="both", expand="yes")

		# Top frame – Labels
		self.rows_label = tk.Label(self.top_frame, text="Rows")
		self.columns_label = tk.Label(self.top_frame, text="Columns")
		self.width_label = tk.Label(self.top_frame, text="Width")
		self.margin_label = tk.Label(self.top_frame, text="Margin")

		# Top frame – Entries
		self.rows_entry = tk.Entry(self.top_frame, width=5)
		self.rows_entry.insert(0, 12)
		self.columns_entry = tk.Entry(self.top_frame, width=5)
		self.columns_entry.insert(0, 12)
		self.width_entry = tk.Entry(self.top_frame, width=5)
		self.width_entry.insert(0, 20)
		self.margin_entry = tk.Entry(self.top_frame, width=5)
		self.margin_entry.insert(0, 2)

		# Top frame – Positions
		self.rows_label.grid(row=0, column=0, padx=0)
		self.columns_label.grid(row=1, column=0, padx=5)
		self.width_label.grid(row=0, column=2, padx=5)
		self.margin_label.grid(row=1, column=2, padx=5)
		self.rows_entry.grid(row=0, column=1, padx=(0,5))
		self.columns_entry.grid(row=1, column=1, padx=(0,5))
		self.width_entry.grid(row=0, column=3, padx=(0,5))
		self.margin_entry.grid(row=1, column=3, padx=(0,5))

		# Grid frame
		self.grid_frame = tk.Frame(self.top_frame)
		self.grid_frame.grid(row=2, columnspan=4)

		# Grid frame – Buttons
		self.load_button = tk.Button(self.grid_frame, text="Load maze", command=self.load_maze)
		self.edit_button = tk.Button(self.grid_frame, text="Edit maze", command=self.edit_maze)
		self.save_button = tk.Button(self.grid_frame, text="Save maze", command=self.save_maze)

		# Grid frame – Positions
		self.load_button.grid(row=2, column=0, padx=(20, 5), pady=(10,10))
		self.edit_button.grid(row=2, column=1, padx=(5, 5), pady=(10,10))
		self.save_button.grid(row=2, column=3, padx=(5, 5), pady=(10,10))

		# Bottom frame
		self.bottom_frame = tk.LabelFrame(self.parent, text="Algorithm options", padx=10, pady=10)
		self.bottom_frame.pack(padx=5, pady=5, fill="both", expand="yes")

		# Bottom frame – Combobox
		self.combobox = ttk.Combobox(self.bottom_frame, width=25, state="readonly",values=["Breadth-first search (BFS)", "Dijkstra's algorithm", "Greedy best-first search (GBFS)", "A star"])
		self.combobox.current(0)
		self.combobox.grid(row=0, columnspan=2, padx=(10,0))

		# Bottom frame – Checkbox
		self.is_expansion = tk.BooleanVar()
		self.checkbox = tk.Checkbutton(self.bottom_frame, text="Hide node expansion", variable=self.is_expansion)
		self.checkbox.grid(row=1, column=0, padx=(10,10), pady=(10,0))

		# Bottom frame – Button
		self.run_button = tk.Button(self.bottom_frame, width=8, text="Run", command=self.run_algorithm)
		self.run_button.grid(row=1, column=1, pady=(10,0))

		# Get screen dimensions
		screen_width = self.parent.winfo_screenwidth()
		screen_height = self.parent.winfo_screenheight()
		window_width = self.parent.winfo_reqwidth()
		window_height = self.parent.winfo_reqheight()
		self.parent.geometry(f"+{(screen_width-window_width)//2 -50}+{(screen_height-window_height)//2-50}")

		# Initialize maze
		self.maze = MazeWindow(rows=self.rows_entry.get(), 
							   columns=self.columns_entry.get(),
							   width=self.width_entry.get(),
							   margin=self.margin_entry.get())

	def load_maze(self):
		try:
			self.parent.filename = tkinter.filedialog.askopenfilename(initialdir="./Mazes", title="Select a maze", filetypes=(("txt files", "*.txt"),))
			self.maze.load(self.parent.filename)
			messagebox.showinfo("File loaded", "File loaded successfully!", parent=self)
		except FileNotFoundError:
			messagebox.showerror("File error", "File could not be loaded!", parent=self)

	def edit_maze(self):
		# Create maze
		self.maze.edit()
		

	def save_maze(self):
		try:			
			self.parent.filename = tkinter.filedialog.asksaveasfilename(initialdir=".", title="Save maze", filetypes=(("txt files", "*.txt"),))
			self.maze.save(self.parent.filename)
			messagebox.showerror("File saved", "Maze saved as {}".format(self.parent.filename), parent=self)
		except IndexError:
			messagebox.showerror("File error", "There is no maze to save! Please, create first a maze.", parent=self)

	def run_algorithm(self):
		if any([self.maze.state_start in row for row in self.maze.grid]):
			self.maze.run(self.is_expansion.get(), self.combobox.get())
		else:
			messagebox.showerror("File error", "There is no maze available! Please, create first a maze.", parent=self)


if __name__ == "__main__":
	root = tk.Tk()
	p = tk.PhotoImage(file="images/icon.png")
	root.iconphoto(False, p)
	MenuWindow(root).pack()
	root.mainloop()
