from pp_api_wrapper import PPApi

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


def make_header(parent, caption, pady, **options):
    photo = tk.PhotoImage(file="projectplace.gif")
    w = tk.Label(parent, image=photo)
    w.photo = photo
    w.pack(pady=pady)


def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=tk.TOP, padx=40, fill=tk.BOTH)
    return entry


def enter(event):
    check_password()


def list_view(project_json):
    parent.destroy()
    new_parent = tk.Frame(root, padx=20, pady=20)
    make_header(new_parent, "Select Project", 30)
    new_parent.pack(fill=tk.BOTH, expand=True)
    Lb1 = tk.Listbox(new_parent, width=40, height=14)
    for i in range(len(project_json)):
        Lb1.insert(i + 1, project_json[i]['name'])
    Lb1.pack()
    sync = tk.Button(new_parent, borderwidth=4, text="Sync Project!", pady=8, command=download_project)
    sync.pack(side=tk.BOTTOM)


def check_password():
    pp_email = user.get()
    pp_password = password.get()
    try:
        api = PPApi(pp_email, pp_password)
        project_json = api.get_user_projects()
        list_view(project_json)
        # parent.destroy()
    except Exception:
        root.title('Credentials incorrect! Try again!')
        user.delete(0, tk.END)
        password.delete(0, tk.END)


def download_project():
    pass

root = tk.Tk()
root.geometry('640x550')
root.title('Projectplace Sync')

# frame for window margin
parent = tk.Frame(root, padx=20, pady=20)
parent.pack(fill=tk.BOTH, expand=True)

# entrys with not shown text
make_header(parent, "Login to Projectplace", 50)
user = make_entry(parent, "Email Address:", 16)
password = make_entry(parent, "Password:", 16, show="*")

# button to attempt to login
b = tk.Button(parent, borderwidth=4, text="Login", width=10, height=10, pady=8, command=check_password)
b.pack(side=tk.BOTTOM)
password.bind('<Return>', enter)
user.focus_set()
parent.mainloop()
