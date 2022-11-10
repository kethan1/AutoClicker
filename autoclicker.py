import pynput
import time
import threading
import tkinter as tk

mouse_controller = pynput.mouse.Controller()
enabled = False
autoclicker_on = False
pos = None
cps = 10
e = threading.Event()


class ToggleButton(tk.Canvas):
    def __init__(self, root, command=None, fg="black", bg="gray", width=100, height=50, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(width=width, height=height, borderwidth=0, highlightthickness=0)
        self.root = root

        self.back_ground = self.create_arc(
            (0, 0, 0, 0), start=90, extent=180, fill="green", outline=""
        )
        self.back_ground1 = self.create_arc(
            (0, 0, 0, 0), start=-90, extent=180, fill="red", outline=""
        )
        self.rect = self.create_rectangle(0, 0, 0, 0, fill="red", outline="")

        self.btn = self.create_oval(0, 0, 0, 0, fill=fg, outline="")

        self.bind("<Configure>", self._resize)
        self.bind("<Button>", self._animate, add="+")
        self.bind("<Button>", command, add="+")

        self.state = 0

    def _resize(self, event):

        self.coords(self.back_ground, 5, 5, event.height - 5, event.height - 5)
        self.coords(self.back_ground1, 5, 5, event.height, event.height - 5)

        factor = (
            event.width
            - (self.coords(self.back_ground1)[2] - self.coords(self.back_ground1)[0])
            - 10
        )
        self.move(self.back_ground1, factor, 0)

        self.coords(
            self.rect,
            self.bbox(self.back_ground)[2] - 2,
            5,
            self.bbox(self.back_ground1)[0] + 2,
            event.height - 5,
        )

        self.coords(self.btn, 5, 5, event.height - 5, event.height - 5)

        if self.state:
            self.moveto(self.btn, self.coords(self.back_ground1)[0] + 4, 4)

    def _animate(self, event):
        self.itemconfig(self.rect, fill="red" if self.itemcget(self.rect, "fill") == "green" else "green")
        x, y, w, h = self.coords(self.btn)
        x = int(x - 1)
        y = int(y - 1)

        if x == self.coords(self.back_ground1)[0] + 4:
            self.moveto(self.btn, 4, 4)
            self.state = 0

        else:
            self.moveto(self.btn, self.coords(self.back_ground1)[0] + 4, 4)
            self.state = 1

    def get_state(self):
        return self.state


def on_click(x, y, button, pressed):
    global autoclicker_on, pos

    if pos != (x, y) and enabled:
        autoclicker_on = not autoclicker_on

        pos = (x, y)


def autoclicker():
    while True:
        if autoclicker_on and enabled:
            mouse_controller.click(pynput.mouse.Button.left, 1)
            time.sleep(1 / cps)
        else:
            e.wait()


def start(event, animate=False):
    global enabled
    time.sleep(0.5)
    enabled = not enabled
    if not enabled:
        e.clear()
    else:
        e.set()
    if animate:
        toggle._animate(event)


def on_press(key):
    if any(key in COMBO for COMBO in COMBINATIONS):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            start(1, animate=True)


def on_release(key):
    if any(key in COMBO for COMBO in COMBINATIONS):
        current.remove(key)


def change_cps(event):
    global cps
    if sv.get().isdigit():
        cps = int(sv.get())


COMBINATIONS = [
    {pynput.keyboard.Key.alt, pynput.keyboard.KeyCode(char='q')},
    {pynput.keyboard.Key.alt, pynput.keyboard.KeyCode(char='Q')},
    {pynput.keyboard.Key.alt_l, pynput.keyboard.KeyCode(char='q')},
    {pynput.keyboard.Key.alt_l, pynput.keyboard.KeyCode(char='Q')},
    {pynput.keyboard.Key.alt_gr, pynput.keyboard.KeyCode(char='q')},
    {pynput.keyboard.Key.alt_gr, pynput.keyboard.KeyCode(char='Q')}
]

mouse_listener = pynput.mouse.Listener(on_click=on_click)
keyboard_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
thread = threading.Thread(target=autoclicker, daemon=True)
mouse_listener.start()
thread.start()
keyboard_listener.start()
current = set()

root = tk.Tk()
sv = tk.StringVar()
sv.set(10)
sv.trace("w", lambda name, index, mode, sv=sv: change_cps(sv))
text = tk.Label(root, text="Toggle the Button the Start the Autoclicker")
text.grid(row=0, column=0)
toggle = ToggleButton(root, width=50, height=25, command=start)
toggle.grid(row=0, column=1)
text = tk.Label(root, text="CPS:", )
text.grid(row=1, column=0)
cps_input = tk.Entry(root, textvariable=sv)
cps_input.grid(row=1, column=1)
instructions = tk.Label(root, text="Instructions:\nTo enable the autoclicker, toggle the toggle button. \nThen, position your cursor where you want the autoclicker to click. \nAfter that, click to start the autoclicker. \nTo stop the autoclicker, move your mouse. To disable the autoclicker from turning on, press Alt-Q or use the toggle button.")
instructions.grid(row=2, column=0, columnspan=2)
root.mainloop()
