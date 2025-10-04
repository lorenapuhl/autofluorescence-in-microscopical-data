"""Script to determine the average intensity over xlength of picture"""
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from statsmodels import robust

"""insert parameters"""
#insert data
names_01Feb = ["01Feb_W01_tail_Gre","01Feb_W02_tail_Gre","01Feb_W03_tail_Gre","01Feb_W04_tail_Gre","01Feb_W05_tail_Gre","01Feb_W06_tail_Gre","01Feb_W07_tail_Gre","01Feb_W08_tail_Gre","01Feb_W09_tail_Gre","01Feb_W10_tail_Gre","01Feb_W11_tail_Gre","01Feb_W12_tail_Gre","01Feb_W13_tail_Gre"] #INSERT names of images to be processed
names_02Feb = ["02Feb_W01_tail_Gre","02Feb_W02_tail_Gre","02Feb_W03_tail_Gre","02Feb_W04_tail_Gre","02Feb_W05_tail_Gre","02Feb_W06_tail_Gre","02Feb_W07_tail_Gre","02Feb_W08_tail_Gre","02Feb_W09_tail_Gre","02Feb_W10_tail_Gre","02Feb_W11_tail_Gre","02Feb_W12_tail_Gre","02Feb_W13_tail_Gre"] #INSERT names of images to be processed
names_04Feb = ["04Feb_W01_tail_Gre","04Feb_W02_tail_Gre","04Feb_W03_tail_Gre","04Feb_W04_tail_Gre","04Feb_W05_tail_Gre","04Feb_W06_tail_Gre","04Feb_W07_tail_Gre","04Feb_W08_tail_Gre","04Feb_W09_tail_Gre","04Feb_W10_tail_Gre","04Feb_W11_tail_Gre","04Feb_W12_tail_Gre","04Feb_W13_tail_Gre"] #INSERT names of images to be processed
names_05Feb = ["05Feb_W01_tail_Gre","05Feb_W02_tail_Gre","05Feb_W03_tail_Gre","05Feb_W04_tail_Gre","05Feb_W05_tail_Gre","05Feb_W06_tail_Gre","05Feb_W07_tail_Gre","05Feb_W08_tail_Gre","05Feb_W09_tail_Gre","05Feb_W10_tail_Gre","05Feb_W11_tail_Gre","05Feb_W12_tail_Gre","05Feb_W13_tail_Gre"] #INSERT names of images to be processed
names_08Feb = ["08Feb_W01_tail_Gre","08Feb_W02_tail_Gre","08Feb_W03_tail_Gre","08Feb_W04_tail_Gre","08Feb_W05_tail_Gre","08Feb_W06_tail_Gre","08Feb_W07_tail_Gre","08Feb_W08_tail_Gre","08Feb_W09_tail_Gre","08Feb_W10_tail_Gre"] #INSERT names of images to be processed
names_12Feb = ["12Feb_W01_tail_Gre","12Feb_W02_tail_Gre","12Feb_W03_tail_Gre","12Feb_W05_tail_Gre","12Feb_W06_tail_Gre","12Feb_W07_tail_Gre","12Feb_W08_tail_Gre","12Feb_W09_tail_Gre","12Feb_W10_tail_Gre","12Feb_W11_tail_Gre","12Feb_W12_tail_Gre"] #INSERT names of images to be processed


#NO OUTLIERS

name_sets = [names_01Feb,names_02Feb,names_04Feb,names_05Feb, names_08Feb, names_12Feb] #INSERT aquisition sets

#enter time of image acquisition
time_01Feb = list(np.ones(len(names_01Feb))*72) #INSERT time data
time_02Feb = list(np.ones(len(names_02Feb))*93) #INSERT time data
time_04Feb = list(np.ones(len(names_04Feb))*48) #INSERT time data
time_05Feb = list(np.ones(len(names_05Feb))*167.5) #INSERT time data
time_08Feb = list(np.ones(len(names_08Feb))*238) #INSERT time data
time_12Feb = list(np.ones(len(names_12Feb))*338) #INSERT time data



time_sets = [time_01Feb,time_02Feb,time_04Feb,time_05Feb, time_08Feb, time_12Feb] #INSERT acquisition times-sets

"""Prepare  time and names list for processing"""

##add times to single list
time_01Feb = [str(t) for t in time_01Feb] #INSERT acquisition set
time_02Feb = [str(t) for t in time_02Feb] #INSERT acquisition set
time_04Feb = [str(t) for t in time_04Feb] #INSERT acquisition set
time_05Feb = [str(t) for t in time_05Feb] #INSERT acquisition set
time_08Feb = [str(t) for t in time_08Feb] #INSERT acquisition set
time_12Feb = [str(t) for t in time_12Feb] #INSERT acquisition set



time = time_01Feb + time_02Feb + time_04Feb + time_05Feb + time_08Feb + time_12Feb #INSERT acuisition set time+time+...

#convert elements back into floats
time = [np.float(t) for t in time]

"""y spatial intensity distribution"""
#Plot intensity profiles?
plot_y_inten=False
fig_y_inten_distr = 1
#Plot intensity profiles in same graph?
same_graph_y = False #If false, graphs are plotted individually

"""Gaussian fit for background and worm position"""
#Plot Gaussian on y spatial intensity distribution?
plotgauss= False

"""x spatial intensity distribution"""
#Plot intensity profiles?
plot_x_inten=False
fig_x_inten_distr = 2
#Plot intensity profiles in same graph?
same_graph_x = False #If false, graphs are plotted individually


"""total intensity over time"""
#Plot each data point?
plot_points = True
fig_tot_inten_points = 3
#Plot statistics?
plot_stats= True
fig_tot_inten_stats = 4
#Plot both in same graph?
plot_both = True
fig_tot_inten = 5


"""Processing function"""
def process(imname,index_acquisitionset):
    """open image"""
    im = Image.open(imname+".tif")
    #im.show()
    impixels=np.array(im)
    
    """basic facts"""
    #get shape of picture
    #eg [[1,2,3],[4,5,6]] is (2,3)
    xsize= int(impixels.shape[1])
    ysize= int(impixels.shape[0])
    print("xsize", xsize, "ysize",ysize)

    #get pixel-type
    print("type", impixels.dtype)
    #eg float32 floating point number ranging from -3.39x1038 to +3.39x1038

    #maximum pixel-value
    print("maximum", np.max(impixels))

    #minimum pixel-value
    print("minimum", np.min(impixels))

    """get columns"""
    columns= []
    #set the amount of lines by defining stepsize in range(0,xsize, xsize/XXX)
    for i in range(0,xsize):
        columns.append(impixels[:,i])
            
    columns=np.array(columns)

    #columns.shape yields (x,y) means I have x columns of a length of y
    amount_columns = int(columns.shape[0]) #lines earlier
    length_columns = int(columns.shape[1]) #length earlier
    print("amount of columns", amount_columns)
    print("length of columns", length_columns)
    #[[1 2 3 4] [1 2 3 4]] is columns with 2 lines of length 4


    """calculating background"""
    ##ignore columns with black spots due to straightening

    #create new columns-list
    x = []

    #check if line contains 0 value, and delete line if so
    for i in range(0,amount_columns):
        for j in range(0,length_columns):
            if columns[i,j] == 0:
                break
            elif j == length_columns -1:
                x.append(columns[i])
            else:
                continue
    cropped_columns = np.array(x)

    #dimensions of cropped picture:
    cropped_amount_columns = int(cropped_columns.shape[0])
    length_columns = int(cropped_columns.shape[1])
    #print("cropped amount of columns", amount_columns)
    #[[1 2 3 4] [1 2 3 4]] is columns with 2 lines of length 4
              

    ##Average over all columns

    #summing pixels of every column
    sum = [] # gives single column with sum of all lines
    for j in range(0,length_columns):
        x = cropped_columns[0,j]
        for i in range(1,cropped_amount_columns-1):
            x = x + cropped_columns[i,j]
        sum.append(x)

    sum = np.array(sum)

    #dividing by amount of lines
    cropped_avercolumn = sum/cropped_amount_columns
    #print("average line", averline)

    ##Gaussian fit on intensity distribution
    #intensity data
    x = np.arange(0,length_columns)
    y = cropped_avercolumn

    #fitting function and parameters
    def Gauss(x,a,x0,sigma,c):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))+c

    a = np.max(y)
    x0=length_columns/2
    sigma = 100
    c = np.min(y)

    popt,pcov = curve_fit(Gauss, x, y, p0=[a, x0, sigma, c])
    
    #Plotting
    if plotgauss == True:
        plt.figure()
        plt.plot(x, y, 'b-', label='aver y-inten')
        plt.plot(x,Gauss(x, *popt), 'r-', label='fit')
        plt.legend()
        plt.title('Fit of worm position')
        plt.xlabel('height of image from top to bottom')
        plt.ylabel('Intensity')
        plt.savefig(str(imname)+"_average_intensity_gaussian")
        plt.close()
    else:
        pass

    ##determine backrground as Gauss-baseline
    bg = popt[3]

    """Setting black spots to background value"""
    #check if line contains 0 value
    for i in range(0,amount_columns):
        for j in range(0,length_columns):
            if columns[i,j] == 0:
                columns[i,j] = bg
    
                         
    """Average over all columns"""
    #summing pixels of every column
    sum = [] # gives single column with sum of all lines
    for j in range(0,length_columns):
        x = columns[0,j]
        for i in range(1,amount_columns-1):
            x = x + columns[i,j]
        sum.append(x)

    sum = np.array(sum)

    #dividing by amount of columns
    avercolumn = sum/amount_columns
    #print("averaged column", avercolumn)


    """background subtraction"""
    avercolumn = (avercolumn - bg)/bg

    #set negative pixels to zero
    for i in range(0,length_columns):
        if avercolumn[i]<0:
            avercolumn[i]=0    

    """Illustration of spatial intensity distribution in y"""
    if plot_y_inten==True:
    
        if same_graph_y == True:
            plt.figure(fig_y_inten_distr)
            x = np.arange(0,length_columns)
            y = avercolumn
            plt.plot(x,y,label=imname[6:9]+" bg= "+str(int(bg)))
            plt.xlabel("ypixel from top to bottom of image")
            plt.ylabel("average intensity")
            plt.title("average intensity over y-axis for "+imname[0:5]+imname[9:22])
            plt.legend()
            plt.savefig("y_intensity_distribution"+imname[0:4]+imname[9:22])
            if imname == name_sets[index_acquisitionset][-1]:
                plt.close(fig_y_inten_distr)
            else:
                pass
            
        else:
            fig = plt.figure()
            x = np.arange(0,length_columns)
            y = avercolumn
            plt.plot(x,y,label=imname[6:8])
            plt.xlabel("ypixel from top to bottom of image")
            plt.ylabel("average intensity")
            plt.title("average intensity over y-axis of "+imname)
            plt.figtext(.7, .8, "bg= "+str(int(bg)))
            plt.savefig(str(imname)+"_y_intensity_distribution")
            plt.close (fig)
            
    else:
        pass
        
  
    """Illsutration of spatial intensity distribution in x"""
    ##get lines
    lines= []
    #set the amount of lines by defining stepsize in range(0,xsize, xsize/XXX)
    for i in range(0,ysize):
        lines.append(impixels[i,:])
            
    lines=np.array(lines)

    #lines.shape yields (x,y) means I have x lines of a length of y
    amount_lines = int(lines.shape[0])
    length_lines = int(lines.shape[1])
    print("amount of lines", amount_lines)
    print("length of lines", length_lines)
    #[[1 2 3 4] [1 2 3 4]] is 2 lines of length 4
    
    
    ##cropping lines to those that contain worm: [x0-3sigma, x0+3sigma]
    lines = lines[int(popt[1]-3*popt[2]):int(popt[1]+popt[2])]
    amount_lines = int(lines.shape[0])
    length_lines = int(lines.shape[1])

    ##Average over all lines
    
    #summing pixels of every line
    sum = [] # gives single line with sum of all lines
    for j in range(0,length_lines):
        x = lines[0,j]
        for i in range(1,amount_lines-1):
            x = x + lines[i,j]
        sum.append(x)

    sum = np.array(sum)

    #dividing by amount of lines
    averline = sum/amount_lines
    #print("average line", averline)

    ##background subtraction
    averline = (averline - bg)/bg

    #set negative pixels to zero
    for i in range(0,length_lines):
        if averline[i]<0:
            averline[i]=0

    ##Illustration of spatial intensity distribution in x"""
    if plot_x_inten==True:
    
        if same_graph_x == True:
            plt.figure(fig_x_inten_distr)
            x = np.arange(0,length_lines)
            y = averline
            plt.plot(x,y,label=imname[6:9]+" bg= "+str(int(bg)))
            plt.xlabel("xpixel from left to right")
            plt.ylabel("average intensity")
            plt.title("average intensity over x-axis for "+imname[0:5]+imname[9:22])
            plt.legend()
            plt.savefig("x_intensity_distribution"+imname[0:4]+imname[9:22])
            if imname == name_sets[index_acquisitionset][-1]:
                plt.close(fig_x_inten_distr)
            else:
                pass
            
        else:
            fig = plt.figure()
            x = np.arange(length_lines)
            y = averline
            plt.plot(x,y,label=imname[6:8])
            plt.xlabel("xpixel from left to right")
            plt.ylabel("average intensity")
            plt.title("average intensity over x-axis of "+imname)
            plt.figtext(.7, .8, "bg= "+str(int(bg)))
            plt.savefig(str(imname)+"_x_intensity_distribution")
            plt.close (fig)
            
    else:
        pass            
            

    """Averaging total intensity of picture"""
    #cropping averaged column to y-pixels that contain worm: [x0-3sigma, x0+3sigma]
    x = avercolumn[int(popt[1]-3*popt[2]):int(popt[1]+popt[2])]
    #calculating total intensity value per area: Sum of all intensity values divided width of the worm
    tot_inten_value = np.sum(x)/(float(len(x)))
    #appending to list for later processing
    totintensity.append(tot_inten_value)
    calc_stats.append(tot_inten_value)
        

"""statistics on each acquisition set"""
name_sets=np.array(name_sets,dtype=object)

totintensity = [] #list of total intensity values for each image
stats_acquisitions = [] #list of statistical values for each acuisition set
calc_stats = [] #list for calculating statistical values of each acquisition set

for index_acquisitionset in range(0,len(name_sets)): #loop through aquisition sets
    print("Set of " + str(name_sets[index_acquisitionset][1][0:6])+str(name_sets[index_acquisitionset][1][10:22]))
    for j in range(0,len(name_sets[index_acquisitionset])): #loop through images of one set
        imname= name_sets[index_acquisitionset][j]
        print("image", imname)

        process(imname,index_acquisitionset) #add tot_inten_value to totintensity-list for chosen image
        
        ##if last image of set reached, determine statistics: stats_acquisitions=[median_set1,median_dev_set1, med_set2,med_dev_set2,...]
        if imname == name_sets[index_acquisitionset][-1]:
            median = np.median(calc_stats_sn)
            print("Median=",median)
            stats_acquisitions_sn.append(median)
            mean = np.mean(calc_stats_sn) 
            print("Mean=",mean)
            std = np.std(calc_stats_sn)
            print("std=",std)
            meddev = robust.mad(calc_stats_sn)
            stats_acquisitions_sn.append(meddev)
            
            calc_stats = [] #after acquisition set fully processed, clear data
        else:
            pass

"""plotting statistics"""
if plot_stats== True:
    #median values
    means=np.array(stats_acquisitions[0:len(stats_acquisitions):2])
    #median deviations as errors
    std=np.array(stats_acquisitions[1:len(stats_acquisitions):2])
    #time points
    t = []
    for i in range(0,len(time_sets)):
        t.append(float(time_sets[i][0])) #append first time point for each acquisition set
    t=np.array(t)

    ##plot figure
    plt.figure(fig_tot_inten_stats)
    plt.errorbar(t, means, std, linestyle='None', marker='x')
    plt.xlabel("time[hrs]")
    plt.ylabel("total intensity")
    plt.title("total intensity of over time")
    plt.savefig("total_intensity_over_time_stats_"+imname[0:6]+imname[10:22]) 
    plt.close(fig_tot_inten_stats)
else:
    pass

"""Plotting total intensity over time"""
if plot_points==True:
    plt.figure(fig_tot_inten_points)
    totintensity = np.array(totintensity)
    plt.errorbar(time,totintensity,linestyle='None', marker='x')

    plt.xlabel("time[hrs]")
    plt.ylabel("total intensity")
    plt.title("total intensity of over time")
    plt.savefig("total_intensity_over_time_points_"+imname[0:6]+imname[10:22])
    plt.close(fig_tot_inten_points)
else:
    pass
    
if plot_both == True:

    plt.figure(fig_tot_inten)
    
    ##prepare data
    #median values
    means=np.array(stats_acquisitions[0:len(stats_acquisitions):2])
    #median deviations as errors
    std=np.array(stats_acquisitions[1:len(stats_acquisitions):2])
    #time points
    t = []
    for i in range(0,len(time_sets)):
        t.append(time_sets[i][0]) #append first time point for each acquisition set
    t=np.array(t)
    
    totintensity = np.array(totintensity)
    
    ##plot both graphs
    plt.subplot(2,1,1)
    plt.errorbar(time,totintensity,linestyle='None', marker='x')
    plt.ylabel("total intensity")
    plt.title("total intensity of over time")
    
    plt.subplot(2, 1, 2)
    plt.errorbar(t, means, std, linestyle='None', marker='x')
    plt.xlabel("time[hrs]")
    plt.ylabel("total intensity")

    plt.savefig("total_intensity_over_time_"+imname[0:6]+imname[10:22]) 
    plt.close(fig_tot_inten)

