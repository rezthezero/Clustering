# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 08:09:42 2021

@author: Rishabh
"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

filterable_columns =  list()
value_columns = list()
filterable_columns_values_dict = dict()
df=pd.DataFrame()
final_list=list()
table_widgets=list()

"""
This function prompts the user for the number of clusters to be created. 
It uses the user selected segregation parameters and filter and distributes
population into clusters using KMeans algorithm. 
"""
def plot():
    count=0
    final_list.clear()
    for i in parameter_listbox.curselection():
        final_list.append(parameter_listbox.get(i))
        count+=1
        
    if count !=2 :
        tk.messagebox.showerror("Error","Error! Select two values to segregate!")
        return None
    try :
        cluster_count = int(simpledialog.askstring("Input", "Number of clusters required?", parent=window))
    except:
        tk.messagebox.showerror("Error","Error! Enter an integer for number of clusters.")
        return None

    fig = Figure(figsize = (5, 5),dpi = 100)
    
    plot1 = fig.add_subplot()
    
    # If no filter is specified ('All') then use the entire dataframe
    # as the filtered dataframe.
    if str(filter_values.get())=='All' :
        filt_df=df
    else :
        filt_df = df[df[str(filter_column.get())]==str(filter_values.get())]
    
    # Selected only the columns specified in segregration parameters
    filt_df1 = filt_df[[final_list[0],final_list[1]]]

    # Now use KMeans to segregate population into the required number of clusters
    Kmean = KMeans(n_clusters=cluster_count)
    model = Kmean.fit(filt_df1)
    label_list = Kmean.labels_
    colors=[plt.cm.gist_rainbow(float(i) /10) for i in label_list]
    colors1=list(map(matplotlib.colors.rgb2hex,colors))
    colors1=reduce_color_list(colors1,label_list,cluster_count)
    
    # placing the canvas on the Tkinter window
    plot1.scatter( filt_df[final_list[0]].tolist() , filt_df[final_list[1]].tolist(),c=colors)
    plot1.set_xlabel(final_list[0])
    plot1.set_ylabel(final_list[1])
    canvas = FigureCanvasTkAgg(fig,master = window)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=2, columnspan=5)
    
    # Generate a table displaying cluster metrics
    write_heading(final_list)
    col_1_values = filt_df1[final_list[0]].tolist()
    col_2_values = filt_df1[final_list[1]].tolist()
    (min_col_1,max_col_1,count)=findminmax(col_1_values,label_list,cluster_count)
    (min_col_2,max_col_2,count)=findminmax(col_2_values,label_list,cluster_count)
    table_data_func(cluster_count,min_col_1,min_col_2,max_col_1,max_col_2,count,colors1)


"""
Read a CSV file and return Panda Dataframe.
"""
def read_file(filename) :
    
    excel_file = filename
 
    df = pd.read_csv(excel_file, index_col=0)
    column_name_list=list(df.columns.values)

    for column_name in column_name_list:
        col_val_set = set(df[column_name].tolist())
        if len(col_val_set) <= 3:
            filterable_columns.append(column_name)
            filterable_columns_values_dict[column_name] = list(col_val_set)
        else:
            value_columns.append(column_name)
    for column_name in filterable_columns:        
        filterable_columns_values_dict[column_name].append('All')
        
    return df

"""
Write table column headings.
"""   
def write_heading(final_list) :
    label = Label( window , text = "Color",font=('Times New Roman',10, 'bold') )
    label.grid(row=4,column=0,columnspan=1,rowspan=2,padx=2)
    label = Label( window , text = "Cluster Number",font=('Times New Roman',10, 'bold') )
    label.grid(row=4,column=1,columnspan=1,rowspan=2,padx=2)
    label = Label( window , text = final_list[0],font=('Times New Roman',10, 'bold') )
    label.grid(row=4,column=2,columnspan=2,padx=2)
    label = Label( window , text = final_list[1],font=('Times New Roman',10, 'bold') )
    label.grid(row=4,column=4,columnspan=2,padx=2)
    label = Label( window , text = "Number of People",font=('Times New Roman',10, 'bold') )
    label.grid(row=4,column=6,columnspan=1,rowspan=2,padx=2)
    label = Label( window , text = "Min",font=('Times New Roman',10, 'bold') )
    label.grid(row=5,column=2,columnspan=1,padx=2)
    label = Label( window , text = "Max",font=('Times New Roman',10, 'bold') )
    label.grid(row=5,column=3,columnspan=1,padx=2)
    label = Label( window , text = "Min",font=('Times New Roman',10, 'bold') )
    label.grid(row=5,column=4,columnspan=1,padx=2)
    label = Label( window , text = "Max",font=('Times New Roman',10, 'bold') )
    label.grid(row=5,column=5,columnspan=1,padx=2)
 
"""
Display cluster metrics in tabular format.
"""
def table_data_func(cluster_count,min_col_1,min_col_2,max_col_1,max_col_2,count,colors) :
    total=sum(count)
    for widget in table_widgets :
        widget.grid_remove()
    table_widgets.clear()
    for i in range(cluster_count):
        label=Label(window,text="      ")
        table_widgets.append(label)
        
        label.config(bg=colors[i])
        label.grid(row=6+i,column=0)
        table_widgets.append(label)
        
        label=Label(window,text="Cluster " +str(i))
        label.grid(row=6+i,column=1)
        table_widgets.append(label)
        
        label=Label(window,text=str(min_col_1[i]))
        label.grid(row=6+i,column=2)
        table_widgets.append(label)
        
        label=Label(window,text=str(max_col_1[i]))
        label.grid(row=6+i,column=3)
        table_widgets.append(label)
        
        label=Label(window,text=str(min_col_2[i]))
        label.grid(row=6+i,column=4)
        table_widgets.append(label)
        
        label=Label(window,text=str(max_col_2[i]))
        label.grid(row=6+i,column=5)
        table_widgets.append(label)
        
        label=Label(window,text=str(count[i]) + " ("+str(round(count[i]*100.0/total,2))+"%)")
        label.grid(row=6+i,column=6)
        table_widgets.append(label)
    
"""
Find the minimum and maximum of both segregation parameters for each cluster.
"""
def findminmax(val_list,lab,num_clusters) :
    minimum_value=[sys.float_info.max]*num_clusters
    maximum_value=[sys.float_info.min]*num_clusters
    count=[0]*num_clusters
    
    for j in range(len(lab)):
        i = lab[j]
        count[i] += 1
        if val_list[j] < minimum_value[i] :
            minimum_value[i] = val_list[j]
        elif val_list[j] > maximum_value[i] :
            maximum_value[i] = val_list[j]
        
    return (minimum_value,maximum_value,count)

"""
Reduce list containing colors for each element into a color for each cluster.
"""
def reduce_color_list(colors, label_list,cluster_count) :
    final_colors=[None]*cluster_count
    for i in range(len(label_list)) :
        final_colors[label_list[i]]=colors[i]
        if all(final_colors) :
            return final_colors
    return final_colors
    

window = tk.Tk()
window.title('Customer Segregation')
window.geometry("800x800")

window.rowconfigure(2,minsize=300)


plot_button = Button(master = window, command = plot, height = 0, width = 10, text = "Plot")
plot_button.grid(row=3,column=3,columnspan=3,pady=10)

file_path = filedialog.askopenfilename()
df=read_file(file_path)

parameter_listbox = Listbox(window, selectmode='multiple',width=30)
for i in range(len(value_columns)) :
    parameter_listbox.insert(i+1, value_columns[i])
parameter_listbox.grid(row=1,column=0,rowspan=3,columnspan=2,sticky='nw')

filter_column = StringVar()
filter_column.set( filterable_columns[0] )

filter_column_dropdown = OptionMenu( window , filter_column, *filterable_columns)
filter_column_dropdown.grid(row=1, column=3,columnspan=2)

filter_values = StringVar()
filter_values.set(filterable_columns_values_dict[str(filter_column.get())][0])

filter_values_dropdown = OptionMenu(window,filter_values,*filterable_columns_values_dict[str(filter_column.get())])
filter_values_dropdown.grid(row=1,column=5,columnspan=2)

filter_dropdown_label = Label( window , text = "Filter :",font=('Times New Roman',10, 'bold') )
filter_dropdown_label.grid(row=0,column=2,columnspan=5)

segregation_listbox_label = Label( window , text = "Segregation Parameters :",font=('Times New Roman',10, 'bold') )
segregation_listbox_label.grid(row=0,column=0,columnspan=2)

window.mainloop()



