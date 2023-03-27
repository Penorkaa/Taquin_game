import tkinter as tk
import copy
from lib.node_class import node

# *variables
moves = 0
free_mode = True
search_option = -2
player_node = node()
SETTING_ICON = None
# -search_option==-2 mean DFS
# -search_option==-1 mean BFS
# -search_option>0 mean DFL

# *methods


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()


def start_game(event=None):
    global moves
    moves = 0
    global player_node
    player_node = node()
    player_node.mat = copy.deepcopy(node.initial_state)
    node.initialise()
    clear_window(window)
    window.configure(bg='black')
    # *title section
    title_frame = tk.Frame(master=window, bg="black", height=50, width=500)
    title = tk.Label(master=title_frame, text="Play on your own or use DFS/BFS to find the solution",
                     bg="black", fg="purple", font=("Arial", 12, 'bold'))
    title.place(anchor=tk.W, rely=0.5)
    global SETTING_ICON
    SETTING_ICON = tk.PhotoImage(file="img/settings.png")
    SETTING_ICON = SETTING_ICON.subsample(20)
    settings_button = tk.Button(title_frame, image=SETTING_ICON, bg="black")
    settings_button.place(x=460, y=10)
    settings_button.bind('<Button>', open_settings)
    # * grid section
    grid_frame = tk.Frame(master=window, bg="black", height=300, width=300)
    make_grid(grid_frame)
    # * options section
    option_frame = tk.Frame(master=window, bg="black", height=50, width=500)
    game_buttons(option_frame)
    # * final layout
    title_frame.pack()
    grid_frame.pack()
    option_frame.pack()


def open_settings(event):
    def submit(event):
        if v.get() == 0:
            try:
                result = int(input.get())
                assert (result > 0)
            except:
                input_warning.set("you need to type a positive number")
                return
            v.set(result)
        global search_option
        search_option = v.get()
        start_game()
    clear_window(window)
    v = tk.IntVar()
    global search_option
    if search_option > 0:
        v.set(0)
    else:
        v.set(search_option)  # initializing the choice
    input_warning = tk.StringVar()
    input_warning.set("")
    window.configure(bg='#d9d9d9')

    tk.Label(window, font=("Arial", 21),
             text="Choose the search algorithm:",
             justify=tk.LEFT,
             padx=20).pack()

    tk.Radiobutton(window, font=("Arial", 21), text="DFS", padx=20,
                   variable=v, value=-2).pack()
    tk.Radiobutton(window, font=("Arial", 21), text="BFS", padx=20,
                   variable=v, value=-1).pack()
    tk.Radiobutton(window, font=("Arial", 21), text="DFL", padx=20,
                   variable=v, value=0).pack()
    bt = tk.Button(text="apply", font=("Arial", 21))
    other = tk.Frame()
    tk.Label(other, font=("Arial", 21), text="DFL's Limit:").grid(row=0)
    input = tk.Entry(other, font=("Arial", 21), width=5)
    input.grid(row=0, column=1)
    other.pack()
    tk.Label(window, font=("Arial", 21), fg="red",
             textvariable=input_warning).pack()
    bt.pack()
    bt.bind('<Button>', submit)


def make_grid(frame):
    global moves

    def switch_cell(event):
        global moves
        if not free_mode:
            return
        info = event.widget.grid_info()
        i = info["row"]
        j = info["column"]
        index = i*3+j
        b = player_node.empty_cell_location()
        if (abs(index-b) == 3 or (abs(index-b) == 1 and index//3 == b//3)):
            player_node.swap(b, index)
            moves += 1
            if player_node.is_final_state():
                victory_screen()
                return
            make_grid(frame)
    clear_window(frame)
    i = 0
    j = 0
    mat = player_node.mat
    for row in mat:
        for cell in row:
            grid_cell = tk.Frame(master=frame, height=80,
                                 width=80, bg="purple")
            grid_cell.bind("<Button-1>", switch_cell)
            grid_cell.grid(row=i, column=j, padx=10, pady=10)
            if cell != 0:
                tk.Label(master=grid_cell, text=str(cell), bg="purple", font=(
                    "Arial", 30)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                grid_cell.destroy()
            j += 1
        i += 1
        j = 0


def victory_screen():
    clear_window(window)
    initial_node = node()
    initial_node.mat = copy.deepcopy(node.initial_state)
    solution, nb = initial_node.solution(BFS=True)
    optimal_moves = len(solution)-1
    if moves == optimal_moves:
        victory_statement = "you played perfectly \n you found the solution in " + \
            str(moves)+" moves!!!"
    else:
        victory_statement = "you found the solution in " + \
            str(moves)+" moves,\n you could've done better honestly.\n it's not a compitition but I did it in " + \
            str(optimal_moves)+" moves."
    tk.Label(window, text=victory_statement, bg="black", fg="purple",
             font=("Arial", 20)).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    tk.Button(window, text="RESTART", fg="purple", font=("Arial", 10, "bold"),
              command=start_game).place(relx=0.5, rely=0.75, anchor=tk.CENTER)


def game_buttons(frame):
    clear_window(frame)
    restart_button = tk.Button(frame, text="restart", bg="purple")
    restart_button.grid(
        row=0, column=0, padx=10)
    tk.Button(frame, text="edit start", bg="purple").grid(
        row=0, column=1, padx=10)
    tk.Button(frame, text="edit end", bg="purple").grid(
        row=0, column=2, padx=10)
    tk.Button(frame, text="solution", bg="purple").grid(
        row=0, column=3, padx=10)
    restart_button.bind("<Button>",start_game)

# -open main window
window = tk.Tk()
window.geometry("500x400")
window.resizable(False, False)
start_game()
window.mainloop()
