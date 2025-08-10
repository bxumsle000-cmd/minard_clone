import pandas as pd
import sqlite3

class CreateMinardDb:
    def __init__(self):
        with open("data/minard.txt") as f:
            lines= f.readlines()

        column_names= lines[2].split()
        patterns_to_be_replace= ("(", "$", ")", ",")

        adjusted_column_names=[]
        for column_name in column_names:
            for pattern in patterns_to_be_replace:
                if pattern in column_name:
                    column_name= column_name.replace(pattern, "")
            adjusted_column_names.append(column_name)
        self.lines= lines        
        self.column_names_city= adjusted_column_names[:3]
        self.column_names_temperature= adjusted_column_names[3:7]
        self.column_names_troop= adjusted_column_names[7:]

    def create_city_dataframe(self):
        i=6
        longitudes, latitudes, cities=[],[],[]
        while i<=25:
            lonc, latc, city= self.lines[i].split()[0:3]
            longitudes.append(float(lonc))
            latitudes.append(float(latc))
            cities.append(city)
            i+=1
        city_data= (longitudes,latitudes, cities)

        city_df= pd.DataFrame()
        for column_name,data in zip(self.column_names_city,city_data):
            city_df[column_name]= data
        return city_df

    def create_temperature_dataframe(self):
        i=6
        longitudes,temperatures,days,dates=[],[],[],[]
        while i<=14:
            longitudes.append(float(self.lines[i].split()[3]))
            temperatures.append(float(self.lines[i].split()[4]))
            days.append(int(self.lines[i].split()[5]))
            if i==10:
                dates.append("Nov 24")
            else:
                dates.append(self.lines[i].split()[6]+" "+self.lines[i].split()[7])
            i+=1
        temperature_data= (longitudes,temperatures,days,dates)

        temperature_df= pd.DataFrame()
        for column_name,data in zip(self.column_names_temperature,temperature_data):
            temperature_df[column_name]= data
        return temperature_df
    
    def create_troop_dataframe(self):
        i=6
        longitudes, latitudes, survivals, directions, division=[],[],[],[],[]
        while i<=53:
            division.append(int(self.lines[i].split()[-1]))
            directions.append(self.lines[i].split()[-2])
            survivals.append(int(self.lines[i].split()[-3]))
            latitudes.append(float(self.lines[i].split()[-4]))
            longitudes.append(float(self.lines[i].split()[-5]))
            i+=1
        troop_data= (longitudes, latitudes, survivals, directions, division)

        troop_df=pd.DataFrame()
        for column_name,data in zip(self.column_names_troop,troop_data):
            troop_df[column_name]= data
        return troop_df
    
    def create_database(self):
        city_df=self.create_city_dataframe()
        temperature_df= self.create_temperature_dataframe()
        troop_df= self.create_troop_dataframe()

        connection= sqlite3.connect("data/minard.db")
        df_dict= {
        "cities":city_df,
        "temperatures": temperature_df,
        "troop": troop_df
        }
        for k,v in df_dict.items():
            v.to_sql(name=k,con=connection,index=False,if_exists="replace")

create_minard_db= CreateMinardDb()
create_minard_db.create_database()
