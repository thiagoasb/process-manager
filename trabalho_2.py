import psutil
import tkinter as tk
import tkinter.ttk as ttk
import os, signal
from time import sleep
from operator import itemgetter
from pprint import pprint as pp
import getpass

process_name = []
process_id = []
process_status = []
process_nice = []
cpu_percent = []
janela = tk.Tk()
t_view = ttk.Treeview(janela, columns=('PID', 'Nome', 'Status', 'Prioridade', '%CPU'), show='headings', height=31)
modo = 'PID'
filtroPID = 0
flag = False

def recover_pid(a):
    #selected = pid_input.get()
    global pid
    selected = t_view.focus()
    dic = t_view.item(selected)
    pid = dic['values'][0]
    return dic['values'][0]

def selected_value():
    #Limpar campo
    pid_input.delete(0,tk.END)

    selected = t_view.focus()
    print(selected)
    values = t_view.item(selected, 'values') #selectiona os valores
    print(values)
    pid_input.insert(0, values[0]) # seleciona o primeiro item da tupla e coloca no input

def kill_process():
    #print(pid)
    os.kill(pid, signal.SIGKILL)

def suspend_process():
    os.kill(pid, signal.SIGSTOP)

def continue_process():
    os.kill(pid, signal.SIGCONT)

def change_priority():
    n = int(prior_input.get())
    print(n)
    p = psutil.Process(pid)
    p.nice(n)

def change_core():
    n = newCore_input.get()
    print(n)
    os.system("taskset -pc " + str(n) + " " + str(pid))

def mudar_flag():
    #global flag
    #global filtroPID = -1

    filtroPID = int(pid_input.get())
    print(filtroPID)

    if (flag == False):
        flag = True
    else:
        flag = False
    

def get_values():    
    data_matrix = []

    processes = psutil.process_iter(['pid', 'nice', 'name', 'status', 'cpu_percent'])


    for proc in processes:   #laço para colocar todas as informações em uma lista individual
        if ((proc.info['pid'] == filtroPID) and (flag == True)):
            print('ENTROU AQUI')
            data_matrix = []
            data_matrix.append([proc.info['pid'], proc.info['name'], proc.info['status'], proc.info['nice'], proc.info['cpu_percent']])
            return data_matrix
        '''p_id.append(proc.info['pid'])         
        p_name.append(proc.info['name'])
        p_nice.append(proc.info['nice'])      #prioridade do processo
        p_status.append(proc.info['status'])
        cpu_perc.append(proc.info['cpu_percent'])'''
        data_matrix.append([proc.info['pid'], proc.info['name'], proc.info['status'], proc.info['nice'], proc.info['cpu_percent']])
    
    return data_matrix

def att_grid(data_att, mode="PID"):
    for i in t_view.get_children():
        t_view.delete(i)

    for (p_id, p_name, p_status, p_nice, cpu_perc) in data_att:
        t_view.insert('', tk.END, values=(p_id, p_name, p_status, p_nice, cpu_perc))


dados = get_values()


print(janela.winfo_screenheight())
janela.title('Gerenciador de Processos')
janela.geometry('1100x768+400+100')




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

'''for i in range(len(process_id)):
    t_view.insert("", tk.END, values=(process_id[i], process_name[i], process_status[i], process_nice[i], cpu_percent[i]))
    #t_view.update("", tk.END, values =(process_id, process_name, process_status, process_nice, cpu_percent))
    #t_view.
'''
#t_view.insert('', tk.END, values=data_info)

t_view.place(x=10, y=115)

add_frame = tk.Frame(janela)
add_frame.pack(pady=20)

#Labels
pid_label = tk.Label(add_frame, text="PID selecionado")
pid_label.grid(row=0, column=1)

temp_label = tk.Label(add_frame,text="")
temp_label.grid(row=1,column=0)

#Inputs
pid_input = tk.Entry(add_frame)
pid_input.grid(row=0, column=2)

prior_input = tk.Entry(add_frame)
prior_input.grid(row=3, column=1)

newCore_input = tk.Entry(add_frame)
newCore_input.grid(row=3, column=3)


#Button
button_pid = tk.Button(add_frame, text="Selecionar", command=mudar_flag)
button_pid.grid(row=0, column=3)

button_kill = tk.Button(add_frame, text="Matar", command=kill_process)
button_kill.grid(row=1, column=1)

button_stop = tk.Button(add_frame, text="Parar", command=suspend_process)
button_stop.grid(row=1, column=2)

button_continue = tk.Button(add_frame, text="Continuar", command=continue_process)
button_continue.grid(row=1, column=3)

button_priority = tk.Button(add_frame, text="Setar Prioridade", command=change_priority)
button_priority.grid(row=3, column=2)

button_newcore = tk.Button(add_frame, text="Mudar core", command=change_core)
button_newcore.grid(row=3, column=4)

t_view.bind('<ButtonRelease-1>', recover_pid)

aux = 0
#filter()
while True:   
    if aux == 599:
        dados = get_values()
        att_grid(dados, modo)
        aux = 0
        #filter(None, dados)
    janela.update()
    
    aux += 1

    sleep(0.002)
    