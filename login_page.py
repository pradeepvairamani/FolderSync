from pp_api_wrapper import PPApi

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


def make_header(parent, caption, width=None, **options):
    photo = tk.PhotoImage(file="projectplace.gif")
    w = tk.Label(parent, image=photo)
    w.photo = photo
    w.pack(pady=50)


def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=tk.TOP, padx=40, fill=tk.BOTH)
    return entry


def enter(event):
    check_password()


def check_password():
    pp_email = user.get()
    pp_password = password.get()
    try:
        api = PPApi(pp_email, pp_password)
        print api.get_user_info()[0]
        parent.destroy()
    except Exception:
        root.title('Credentials incorrect! Try again!')
        user.delete(0, tk.END)
        password.delete(0, tk.END)

root = tk.Tk()
root.geometry('640x550')
root.title('Projectplace Sync')

# frame for window margin
parent = tk.Frame(root, padx=20, pady=20)
parent.pack(fill=tk.BOTH, expand=True)

# entrys with not shown text
make_header(parent, "Login to Projectplace", 20)
user = make_entry(parent, "Email Address:", 16)
password = make_entry(parent, "Password:", 16, show="*")

# button to attempt to login
b = tk.Button(parent, borderwidth=4, text="Login", width=10, height=10, pady=8, command=check_password)
b.pack(side=tk.BOTTOM)
password.bind('<Return>', enter)
user.focus_set()
parent.mainloop()
