from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd


connection=sqlite3.connect("data/minard.db")
city_df=pd.read_sql("""SELECT * FROM cities;""",con=connection)
temperature_df= pd.read_sql("SELECT * FROM temperatures;",con=connection)
troop_df= pd.read_sql("""SELECT * FROM troop;""", con= connection)
connection.close()
fig,axes= plt.subplots(nrows=2,figsize=(25,12),gridspec_kw={"height_ratios":[4,1]})

m= Basemap(projection="lcc",resolution="i",width=1000000,height=400000,
           lon_0=31,lat_0=55,ax=axes[0])
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54,58),labels=[True,False,False,False])
m.drawmeridians(range(23,56,2),labels=[False,False,False,True])

lonc= city_df["lonc"].values
latc= city_df["latc"].values
city_names= city_df["city"].values
x,y=m(lonc,latc)
for xi,yi,city_name in zip(x,y,city_names):
    axes[0].annotate(text=city_name,xy=(xi,yi),fontsize=14,zorder=2)

rows= troop_df.shape[0]
lonp= troop_df["lonp"].values
latp= troop_df["latp"].values
survivals= troop_df["surviv"].values
directions= troop_df["direc"].values
x,y=m(lonp,latp)
for i in range(rows-1):
    if directions[i]== "A":
        line_color= "tan"
    else:
        line_color= "black"
    start_stop_lons= (x[i],x[i+1])
    start_stop_lats= (y[i],y[i+1])
    line_width= survivals[i]
    axes[0].plot(start_stop_lons,start_stop_lats,color= line_color,linewidth=line_width/10000,zorder=1)

lont= temperature_df["lont"].values
temp_celsius= (temperature_df["temp"]*5/4).astype(int)
annotations= temp_celsius.astype(str).str.cat(temperature_df["date"],sep="°C")
axes[1].plot(lont,temp_celsius,linestyle="dashed",color="black")
for xi,yi,annotation in zip(lont,temp_celsius,annotations):
    axes[1].annotate(annotation,xy=(xi-0.3,yi-7),fontsize=16)
axes[1].set_ylim(-50,10)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].grid()
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])

axes[0].set_title("Napoleon's disastrous Russian campaign of 1812",loc="left",fontsize=30)
plt.tight_layout()
plt.savefig("minard_clone.png")
