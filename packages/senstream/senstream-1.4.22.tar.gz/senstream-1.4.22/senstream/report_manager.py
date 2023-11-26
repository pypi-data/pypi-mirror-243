# 1. Handles report generation tasks
# 2. Used to define a scheduler for sending email/text notifications (every day, week, month, year, etc.)
# 3. Used to configure the content of reports
# 4. Handles the plotting and data visualization tasks using matplotlib.pyplot
# 5. Stores recipient information and report naming (e.g. name a report based on site)
import numpy as np
import pandas as pd
from datetime import date
from time import sleep
from progress.bar import FillingCirclesBar

# SenSpot client connection packages
from senstream.resensys import Resensys,Sensors
from senstream.senspot import SenSpot

import warnings
warnings.filterwarnings("ignore")

class ReportGenerator(Resensys):

    def __init__(self,parent,report_prefix="ResensysReport_",export_path="/",duration="24hour"):
        super().__init__(parent.username, parent.password)
        self.conn = parent.conn
        self.sensors = Sensors(self.conn)
        self.sensor_df = self.sensors.getSensors(format="dataframe")

        self.duration = duration
        self.report_prefix = report_prefix
        self.export_path = export_path

        # extract the sites in account for reporting
        sites = self.sensors.getSites(format="dataframe")
        self.sids = sites["SID"].to_list()
        self.reports = []
        self.quantitiesExcluded = []
        self.deviceTypesExcluded = []

    def getDeviceTypes(self):
        return self.sensor_df.DeviceType.unique()
    
    # enter a list of sites to use for reporting
    def filterSites(self,sids):
        self.sids = sids

    # get the included sites in the report generator
    def getReportGeneratorSites(self):
        return self.sids
    
    # specify list of quantites by name to be excluded from the report
    def excludeQuantites(self,quantities_list):
        self.quantitiesExcluded = quantities_list

    # get the list of excluded quantities in the report generator
    def getExcludedQuantities(self):
        return self.quantitiesExcluded
    
    # specify list of quantites by name to be excluded from the report
    def excludeDeviceType(self,device_type_list):
        self.deviceTypesExcluded = device_type_list

    # get the list of excluded quantities in the report generator
    def getExcludedDeviceTypes(self):
        return self.deviceTypesExcluded

    # specify the device type as a string and extract a joined,unformatted dataframe for all device-quantity pairs of deviceType
    def joinDeviceTypeData(self,deviceType,metric=True):
        # initialize an empty join pandas dataframe with "Time" columns
        df_join = pd.DataFrame(columns=["Time"])
        # get the list of devices for the given deviceType
        device_list = self.sensor_df[(self.sensor_df["SID"].isin(self.sids)) & (self.sensor_df["DeviceType"]==deviceType)].DID.to_list()

        with FillingCirclesBar(f'Processing {device_list} SenSpots...',max=(len(device_list))) as bar:
            for device in device_list:
                # get the device quantities
                ss = SenSpot(self.conn,device)
                senspot_quantities = [value for value in ss.getQuantities() if value not in self.quantitiesExcluded]
                name = ss.getName()
                # loop through each quantity in senspot_quantities
                for quantity in senspot_quantities:
                    df_temp = ss.timeStream(quantity,time=[self.duration]).sort_values(by=['Time'])
                    if metric and quantity == "Internal Temperature":
                        df_temp["Value"] = (5/9)*(df_temp["Value"]-32.0) # convert to Celcius
                    df_temp.rename(columns={'Value':name+f'_{quantity}'},inplace=True)
                    df_join = pd.concat([df_join,df_temp])
                sleep(0.02)
                bar.next()

        return df_join
    
    def generateReport(self,downsample_interval="H",downsample_filter="median",fileFormat="csv"):
        deviceTypes = [value for value in self.getDeviceTypes() if value not in self.deviceTypesExcluded]
        df_joins = []
        for deviceType in deviceTypes:
            df = self.joinDeviceTypeData(deviceType)
            df_joins.append(df)
        print(f"Concatenating data and synchronizing timestamps ...\n")
        df_join = pd.concat(df_joins)
        df_join.dropna(how='all', axis=1, inplace=True)
        df_join = df_join.sort_values(by='Time')
        first_column = df_join.pop('Time')
        df_join.insert(0,'Time',first_column)
        df_join = df_join.reindex(columns=sorted(df_join.columns))

        if downsample_filter == "median":
            df_join = df_join.resample(downsample_interval,on="Time",origin="start_day").median()
        elif downsample_filter == "mean":
            df_join = df_join.resample(downsample_interval,on="Time",origin="start_day").mean()
        else: # default to filtering to the median between timestamps
            df_join = df_join.resample(downsample_interval,on="Time",origin="start_day").median()

        file_name = f"{self.export_path}{self.report_prefix}_{date.today()}"
        if fileFormat == "csv":
            df_join.to_csv(file_name+".csv")
        elif fileFormat == "excel":
            df_join.to_csv(file_name+".xlsx",sheetname="Summary")
        elif fileFormat == "json":
            df_join.to_json(file_name+".json",orient="index")
        elif fileFormat == "html":
            # add css formatting later
            df_join.to_html(file_name+".html")
        else:
            df_join.to_csv(file_name+".csv")
        self.logReport()

    # add a record to account report generation log with name, location, datetime, and report settings to AWS server via API
    def logReport(self,fileName,directory,currentTime,duration,downsample_filter,fileFormat):
        print("This is where we log the Report to AWS via API as record in JSON file")

class SenScopeReporter():

    # Instatiate SenScopeReporter object with SenScope-created JSON exporting template 
    def __init__(self,parent,template):
        super().__init__(parent.username, parent.password)
        self.conn = parent.conn
        self.template = template
    
    # handle converting senscope json template into managable datastructures for data extraction and processing
    def parseTemplate():
        print("This is where we parse the exporting file.")

# To Do:
# 1. Option to collect report locally or save remotely on resensys cloud
# 2. Store remote reports in S3 bucket specific to user via the webserver API
# 4. Collect units for a given quantity in column names
# 6. Every report created for a user should get logged in a user log file to be displayed on WebPortal