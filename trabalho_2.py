import psutil
import tkinter as tk
import tkinter.ttk as ttk

def selected_value():
    #Limpar campo
    pid_input.delete(0,tk.END)

    selected = t_view.focus()
    values = t_view.item(selected, 'values') #selectiona os valores
    pid_input.insert(0, values[0]) # seleciona o primeiro item da tupla e coloca no input

#def recover_pid():
#    selected = pid_input.get()
 #   print(selected)
      

process_name = []
process_id = []
process_status = []
process_nice = []
cpu_percent = []

processes = psutil.process_iter(['pid', 'nice', 'name', 'status', 'cpu_percent'])


for proc in processes:                          #laço para colocar todas as informações em uma lista individual
    process_id.append(proc.info['pid'])         
    process_name.append(proc.info['name'])
    process_nice.append(proc.info['nice'])      #prioridade do processo
    process_status.append(proc.info['status'])
    cpu_percent.append(proc.info['cpu_percent'])


janela = tk.Tk()
janela.title('Gerenciador de Processos')
janela.geometry('1100x768+400+100')

t_view = ttk.Treeview(janela, columns=('PID', 'Nome', 'Status', 'Prioridade', '%CPU'), show='headings', height=31)


t_view.column('PID', minwidth=0, width=212)
t_view.column('Nome', minwidth=0, width=212)
t_view.column('Status', minwidth=0, width=212)
t_view.column('Prioridade', minwidth=0, width=212)
t_view.column('%CPU', minwidth=0, width=212)

t_view.heading('PID', text='PID')
t_view.heading('Nome', text='Nome')
t_view.heading('Status', text='Status')
t_view.heading('Prioridade', text='Prioridade')
t_view.heading('%CPU', text='% CPU')

for i in range(len(process_id)):
    t_view.insert("", tk.END, values=(process_id[i], process_name[i], process_status[i], process_nice[i], cpu_percent[i]))


t_view.place(x=10, y=115)

add_frame = tk.Frame(janela)
add_frame.pack(pady=20)

#Labels
pid_label = tk.Label(add_frame, text="PID selecionado")
pid_label.grid(row=0, column=0)

temp_label = tk.Label(add_frame,text="")
temp_label.grid(row=1,column=0)

#Inputs
pid_input = tk.Entry(add_frame)
pid_input.grid(row=0, column=1)

#Button
button_pid = tk.Button(add_frame, text="Selecionar", command=selected_value)
button_pid.grid(row=1, column=1)

janela.mainloop()