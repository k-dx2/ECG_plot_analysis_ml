import bioread
import matplotlib.pyplot as plt
import numpy as np
from Tkinter import * 

total=0
ref_size= 0
peaks=[]
rr=[]

def estimate_coef(x, y): 
	n = np.size(x)
	m_x, m_y = np.mean(x), np.mean(y)
	SS_xy = np.sum(y*x) - n*m_y*m_x
	SS_xx = np.sum(x*x) - n*m_x*m_x
	b_1 = SS_xy / SS_xx
	b_0 = m_y - b_1*m_x
	return(b_0, b_1) 
  
def plot_regression_line(x, y, b):
	plt.scatter(x, y, color = "y",marker = "o", s = 30)
	y_pred = b[0] + b[1]*x
	plt.plot(x, y_pred, color = "r")
	plt.xlabel('Time(ms)')
	plt.ylabel('RR interval(ms)')
	





def isPeak(arr,n, num, i, j):
    
    if arr[i]>2.0: 
  
	    if (i >= 0 and arr[i] >num): 
        	return False
  
    
	    if (j < n and arr[j] >num ): 
	        return False
	    return True	


def printPeaks(arr, n): 
  
    
  
    for i in range(n): 
  
        if (isPeak(arr, n, arr[i], i - 1, i + 1)):
            peaks.append(i)
    

def read():
	name=e1.get()
	data=bioread.read_file(name)
        total=len(data.channels[0].data)
        equation.set(str(total))
	
	
	  
def call():
 	 file_name=e1.get()
         file_length=e2.get()
         data=bioread.read_file(file_name)
         n=len(data.channels)
         
         for i in range (n):
		print('The name of the Channel',data.channels[i].name)
		a=data.channels[i].name
		print('Samples per second',data.channels[i].samples_per_second)
		print('Total number of data',len(data.channels[i].data))
		
		ref_size=int(file_length)
		print('Data',data.channels[i].data)
		
		plt.figure()
		plt.plot(data.channels[i].data[0:ref_size])
		plt.title(a, fontdict=None, loc='center')
		plt.xlabel("Time (ms)")
		plt.ylabel("Voltage(mV)")
		
		
				
		printPeaks(data.channels[i].data[0:ref_size], ref_size) 
		
	
		length=len(peaks)
		rr.append(0)
	
		for i in range(length-1):
			rr.append(peaks[i+1]-peaks[i])

		print("Peaks :\n") 
		print(peaks)
		print("\n")
		print("The RR interval for the given ECG is\n")
		print(rr)
		print("\n")
	
	
		#x and y are the cleaned version of  peaks and rr
		x=[]
		y=[]
		
	
		for k in range(1,length-1):
			if rr[k]==1:
				k=k+1
		
			x.append(peaks[k])
			y.append(rr[k])
		
		print(x)
		print("\n")
		print(y)
		print("\n")
		
		plt.figure()
		plt.plot(x,y,'ro')
	    	plt.title("RR Interval plot", fontdict=None, loc='center')
	    	plt.xlabel("Time(ms)")
	    	plt.ylabel("RR interval(ms)")
	    	plt.show(block=False)
	
		new_x=np.array(x)
		new_y=np.array(y)
	
		b = estimate_coef(new_x,new_y)
		plt.figure()
		plt.title("Plots over interval Single interval", fontdict=None, loc='center') 
    		print("Estimated coefficients:\nb_0 = {} \nb_1 = {}".format(b[0], b[1])) 
	        plot_regression_line(new_x, new_y, b)
	        plt.show(block=False)
	    	
	    	for k in range(50,201,50):
	    		
		    	interval=k
			loop=len(new_x)/interval
			i=0
		    	val=0
		    	plt.figure()
		    	
		    	for i in range(loop-1):
		    		
			   	b = estimate_coef(new_x[val:val+k], new_y[val:val+k]) 
				print("Estimated coefficients:\nb_0 = {}\nb_1 = {}".format(b[0], b[1])) 
				plot_regression_line(new_x[val:val+k], new_y[val:val+k], b)
				val=val+interval
				
		
			b = estimate_coef(new_x[val:len(new_x)],new_y[val:len(new_y)])
			plt.title("Plots over interval %i" %k, fontdict=None, loc='center') 
			print("Estimated coefficients:\nb_0 = {}\nb_1 = {}".format(b[0], b[1])) 
			plot_regression_line(new_x[val:len(new_x)], new_y[val:len(new_y)], b)
			plt.show(block=False)
	                
	         
		
		

 



gui= Tk()
gui.geometry("300x300")
bg="PaleTurquoise3"
gui['bg']=bg
gui.title("ECG PLOT ANALYSIS")


equation = StringVar() 

Label(gui, text='File Name :',font=('Comic Sans MS', 12),background=bg,padx=15, pady=5).grid(row=0)

read = Button(gui, text=' Read File',command=read) 
read.place(height=30, x=100, y=100)

Label(gui, text='Total Length',background=bg,padx=15, pady=5).grid(row=1)

Label(gui,textvariable=equation ,background='white', padx=25, pady=5).grid(row=2)


l1=Label(gui, text='Length :',font=('Comic Sans MS', 12),background=bg,padx=5, pady=5)
l1.place(x=10, y=150)

generate = Button(gui, text='View Plots',command=call) 
generate.place(height=30, x=100, y=250)
 
e1 = Entry(gui) 
e2 = Entry(gui)
e1.grid(row=0, column=1) 
e2.place(x=120, y=155) 
	
        



gui.mainloop() 
	
		
	
