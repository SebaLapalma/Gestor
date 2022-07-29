from tkinter import *
import sqlite3

colorbgroot= 'lightblue'
root = Tk()
root.title('Gestor de tareas')
root.geometry('500x500')

root.configure(
    background=colorbgroot
)

conn = sqlite3.connect('todo.db')

c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      description TEXT NOT NULL,
      completed BOOLEAN NOT NULL
    );
""")

conn.commit()

def complete(id):
    def _complete():
        todo = c.execute('SELECT * from todo WHERE id = ?',(id, )).fetchone()
        c.execute('UPDATE todo SET completed = ? WHERE id = ?', (not todo[3], id))
        conn.commit()
        render_todos()
        
        print(id)
        
    return _complete

def remove(id):
    def _remove():
        c.execute('DELETE FROM todo WHERE id = ?', (id, ))
        conn.commit()
        render_todos()
    return _remove

def render_todos():
    rows = c.execute('SELECT * from todo').fetchall()
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = 'grey' if completed else 'black'
        colorbg = 'lightblue'
        l = Checkbutton(frame, text=description,bg=colorbg, fg=color, width=42, anchor='w', command=complete(id))
        l.grid(row=i, column=0, sticky='w')
        delete_btn = Button(frame, text='Eliminar', command=remove(id))
        delete_btn.grid(row=i, column=1)
        l.select() if completed else l.deselect()
        
def add_todo():
    todo = e.get()
    if todo:
        c.execute("""
        INSERT INTO todo (description, completed) VALUES (?, ?)    
    """, (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass

l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=add_todo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe',padx=5)

e.focus()

root.bind('<Return>', lambda x: add_todo())

render_todos()

root.mainloop()