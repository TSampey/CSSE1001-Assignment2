###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 
#
#   Student Name: Thomas Sampey
#
###################################################################

#
# Do not change the following import
#

from assign2_support import *

####################################################################
#
# Insert your code below
#
####################################################################

class PVData(object):
    def __init__(self):
        """
        This function makes sure that the variable date = None and
        changes the date to yesterdays date.
        Constructor:  __init__ (self)
        """  
        self._date = None
        self.change_date(yesterday())

    def change_date(self, date):
        """
        change_date(self, date)
        Checks if date is not = self, loads data corresponding to date,
        loops through data saving time, temp,sunlight to a list and
        saves power to a dictionary.
        """
        if date != self._date:
            data = load_data(date)
            self._date = date         
            self._timeList = []
            self._tempList = []
            self._sunList = []
            self._powers = {}
            for name in ARRAYS:
                self._powers[name] = []
            for d in data:
                self._timeList.append(d[0])
                self._tempList.append(d[1])
                self._sunList.append(d[2])
                for i,a in enumerate(d[3]):
                    self._powers[ARRAYS[i]].append(a)   

    def get_date(self):
        """
        returns the str(date)
        get_date(None) -> (string)
        """
        return self._date
        
    def get_time(self, time_index):
        """
        returns temperature list 
        get_time(<list>) -> <list>
        """
        return self._timeList[time_index]

    def get_temperature(self):
        """
        returns list of temperature temperature values for loaded
        date.
        get_temperature(None) -> <list>
        """
        return self._tempList
    
    def get_sunlight(self):
        """
        returns list of sunlight values for loaded date
        get_sunlight(None) -> <list>
        """
        return self._sunList

    def get_power(self, array):
        """
        returns a list of power for the loaded date at
        the current array
        get_power(dict(key,value)) -> <list>
        """
        return self._powers[array]


class Plotter(Canvas):
    """
    Plotter is responsible for plotting the different features onto the graph
    such as the click function. It inherits from canvas. 
    """
    def __init__(self, root, pva ,pvData):
        """
        This method initialises everything and creates instances of each argument.
        It also calls to the respective method when the user clicks on the canvas.
        Constructor: __innit__(self,root,plottApp,pvData)
        """
        Canvas.__init__(self,root,bg="white",bd=2,relief=SUNKEN,width=300,\
                        height=300)
        self._pvd = pvData
        self.root= root
        self._app = pva
        self._coordTransl=CoordinateTranslator(300,300,\
                                               len(pvData.get_temperature()))
        root.bind('<Configure>', self.do_conf)
        self.bind('<ButtonRelease-1>', self.btn1Released)
        self.bind('<Button-1>', self.btn1Motion)
        self.bind('<B1-Motion>', self.btn1Motion)

    def plotPower(self):
        """
        plotPower(None)
        This method is responsible for creating what is needed to plot power.
        Enumerates through power index and array and saves each value to a list
        with its index
        """
        coords = []
        placesPower = self._pvd.get_power(self._app.get_current_array())
        for i, power in enumerate(placesPower):
            coords.append(self._coordTransl.power_coords(i, power, \
                                                         self._app.get_current_array()))
        self.create_polygon(coords, fill=POWER_COLOUR)

    def plotTemp(self):
        """
        plotTemp(None)
        This method is responsible for creating what is needed to plot temperature.
        Enumerates through temperature values from get_temperature()
        saves each value to a list with its index.
        """
        tCoords = []
        for i, temp in enumerate(self._pvd.get_temperature()):
            tCoords.append(self._coordTransl.temperature_coords(i, temp))
        self.create_line(tCoords, fill='red')

    def plotSunlight(self):
        """
        plotSunlight(None)
        This method is responsible for creating what is needed to plot Sunlight.
        Enumerates through Sunlight values from get_Sunlight()
        saves each value to a list with its index.
        """
        sCoords = []
        for i, sun in enumerate(self._pvd.get_sunlight()):
            sCoords.append(self._coordTransl.sunlight_coords(i, sun))
        self.create_line(sCoords, fill='orange')

    def refresh(self):
        """
        refresh(None)
        This method is responsible for plotting the power,sun and temp in accordance
        to what checkbox is checked.
        """
        pOn, tOn, sOn = self._app.isValueOn() 
        self.delete(ALL)
        if pOn == 1:
            self.plotPower()
        if tOn == 1:
            self.plotTemp()
        if sOn == 1:
            self.plotSunlight()          
            
    def do_conf(self, e):
        """
        do_conf(e)
        Calls the coordinate translators method of resize and then calls the refresh method
        which redraws whats on the canvas.
        """
        self._coordTransl.resize(self.winfo_width(), self.winfo_height())
        self.refresh()
        
    def btn1Motion(self, e):
        """
        btn1Motion(e) -> None
        This method is called when the user moves the mouse as well as
        having mouse button 1 clicked. Refreshes canvas everytime it is called
        with prevents the line from being duplicated.
        """
        
        if not 0 < e.x < self.winfo_width():
            return
        self.refresh()
        self.create_line((e.x,self.winfo_height()), e.x,0)
        index = self._coordTransl.get_index(e.x)
        self._app.selectedDataAtIndex(index)

    def btn1Released(self, e):
        """
        btn1Released(e)
        Deletes the line on the canvas when mouse button 1 is released. And sends
        data to another method.
        """
        self.refresh()
        self._app.releasedB1Data()
     
class OptionsFrame(Frame):
    """
    OptionsFrame(Frame)
    This class is responsible for the visual aesthetics of the application.
    It also records the state of each option.
    """
    def __init__(self, master, plot,newdate):
        """
        Initialises the instances. It packs each option to the screen and records
        when each option is changed.
        Constructor:__init__(object,object, method)
        """
        self._plot = plot
        self._newDate = newdate    
        Frame.__init__(self, master)
        cBtnFrame = Frame(self)
        cBtnFrame.pack(side=TOP)
        self._cPower = IntVar()
        self._cTemp = IntVar()
        self._cSun = IntVar()
        self._date = StringVar()
        self._defaultOpt = StringVar()
        self._cPower.set(1)
        self._powerCB = Checkbutton(cBtnFrame, text="Power",\
                                    variable = self._cPower,command=self.onChange)
        self._powerCB.pack(side=LEFT)
        self._tempCB = Checkbutton(cBtnFrame, text="Temperature",\
                                   variable = self._cTemp, command=self.onChange)
        self._tempCB.pack(side=LEFT)
        self._sunCB = Checkbutton(cBtnFrame, text="Sunlight",\
                                  variable = self._cSun, command=self.onChange)
        self._sunCB.pack(side=LEFT)
        infoFrame = Frame(self)
        infoFrame.pack(side=TOP, fill=X)   
        dateLabel = Label(infoFrame, text="Choose Date")
        dateLabel.pack(side=LEFT, padx=10, pady=10)
        self._dateBox = Entry(infoFrame, textvariable=self._date)
        self._dateBox.pack(side=LEFT)
        self._date.set(yesterday())
        dateBtn = Button(infoFrame, text='Apply', width=5, command=self.validation)
        dateBtn.pack(side=LEFT, pady=15)
        self._places = ARRAYS
        menu = OptionMenu(infoFrame, self._defaultOpt, *self._places, command=self.checkOpts)
        menu.config(width=25)
        self._defaultOpt.set(ARRAYS[9])
        menu.pack(side=RIGHT, padx=10,pady=10)
      
    def isPowerChecked(self):
        """
        checks if the power checkbox is checked
        isPowerChecked(None) -> (int)
        """
        return self._cPower.get()

    def onChange(self):
        """
        calls a method from another class.
        onChange(None) -> (int)
        """
        self._plot()

    def get_current_array(self):
        """
        Checks which array is clicked within the options menu
        get_current_array(None) -> (int)
        """
        return self._defaultOpt.get()
        
    def isTempChecked(self):
        """
        checks if the temperature checkbox is checked
        isTempChecked(None) -> (int)
        """
        return self._cTemp.get()

    def isSunChecked(self):
        """
        checks if the sun checkbox is checked
        isSunChecked(None) -> (int)
        """
        return self._cSun.get()
        
    def checkOpts(self, option):
        """
        checks to see what checkboxes are checked and sends
        the data to plotapp to call a method.
        isCheckOpts(optoin) -> (int)
        """
        self._plot()
        return option 

    def validation(self):
        """
        called when Apply button is pressed.
        It creates a variable and sends it to 
        isPowerChecked(None) -> (int)
        """
        newDate = self._dateBox.get()
        self._newDate(newDate)
        
class PVPlotApp(object):
    """
    This class is the controller, it retrieves and passes data to the
    other classes which ask for the data it needs to do a certain task.
    """
    def __init__(self, root):
        """
        constructor: __init__(root)
        initialises all the instances and presets some of the G.U.I data.
        """
        self._root = root
        root.title('Pv Plotter')
        root.minsize(800,600)
        self._pvData = PVData()
        self._text=StringVar()     
        self._dataLabel = Label(root)
        self._dataLabel.pack(side = TOP, anchor = W, padx=+10, pady=10)
        self._toDate= StringVar()
        self._toDate= 'Data for ' + self._pvData.get_date()
        self._dataLabel.config(text= self._toDate)
        self.plotter = Plotter(root,self ,self._pvData)
        self.plotter.pack(side=TOP, fill=BOTH, expand=True)
        self._optionsFrame = OptionsFrame(root, self.refreshCanvas, self.newdate)
        self._optionsFrame.pack(side=TOP, fill=X)
        self._points = []

    def isValueOn(self):
        """
        isValueOn(None) -> (int)
        Checks which variables are checked and not checked.
        """
        return self._optionsFrame.isPowerChecked(),self._optionsFrame.isTempChecked(),\
                self._optionsFrame.isSunChecked()

    def newdate(self, date):
        """
        newdate(date) -> None
        Error checking for the date. Checks if the string
        is a valid date and prints out the ValueError.
        """
        try:
            self._pvData.change_date(date)
            self.plotter.refresh()
            self.releasedB1Data()
        except ValueError as e:
            tkMessageBox.showerror("Date Error", str(e))

    def refreshCanvas(self):
        """
        refreshCanvas(None)
        calls a method within the plotter class.
        """
        self.plotter.refresh()

    def get_current_array(self):
        """
        get_current_array(None)
        obtains the array from options frame method.
        """
        return self._optionsFrame.get_current_array()

    def releasedB1Data(self):
        """
        releasedB1Data(None)
        changes the label back to the original string
        when mouse button 1 is released
        """
        self._pDate = self._pvData.get_date() 
        self._tDate= 'Data for ' + self._pDate
        self._dataLabel.config(text= self._tDate)

    def selectedDataAtIndex(self, idx):
        """
        selectedDataAtIndex(int) -> None
        gets the index values and then uses them for
        Pretty_Print_Data() method from the support file to
        style the label.
        """
        cPower,cTemp,cSun = self.isValueOn()
        self._date = self._pvData.get_date()
        self._time = self._pvData.get_time(idx)
        self._temp = self._pvData.get_temperature()[idx]
        self._sunlight = self._pvData.get_sunlight()[idx]
        self._power = self._pvData.get_power(self.get_current_array())\
                      [idx]

        if (cPower == 1) and (cTemp == 1) and (cSun == 1):      
            self._dataLabel.config(text=pretty_print_data(self._date, self._time, self._temp, \
                                                          self._sunlight, self._power))

        elif (cPower == 1) and (cTemp == 0) and (cSun == 0): 
            self._dataLabel.config(text=pretty_print_data(self._date, self._time, None,\
                                                          None, self._power))

        elif (cPower == 0) and (cTemp == 1) and (cSun == 0): 
            self._dataLabel.config(text=pretty_print_data(self._date, self._time, self._temp, \
                                                          None, None))

        elif (cPower == 0) and (cTemp == 0) and (cSun == 1): 
            self._dataLabel.config(text=pretty_print_data(self._date, self._time, None, \
                                                          self._sunlight, None)) 

        elif (cPower == 0) and (cTemp == 1) and (cSun == 1): 
            self._dataLabel.config(text=pretty_print_data(self._date, self._time, self._temp, \
                                                          self._sunlight, None)) 

        elif (cPower == 1) and (cTemp == 0) and (cSun == 1):
            self._dataLabel.config(text=pretty_print_data(self._date, self._time, None, \
                                                          self._sunlight, self._power))

        elif (cPower == 1) and (cTemp == 1) and (cSun == 0):
            self._dataLabel.config(text=pretty_print_data(self._date, self._time, self._temp, \
                                                          None, self._power))
        else:
            pass


 

####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = PVPlotApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
