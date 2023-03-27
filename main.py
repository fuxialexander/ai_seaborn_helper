#%%
from ai import auto_plot, describe_df

csv_path = "HPI_master.csv"
x = "hpi_flavor"
y = "index_sa"
plot_type = "boxplot"
#%%
description = describe_df(csv_path)
#%%
# print description, split into 60 characters lines
for i in range(0, len(description), 60):
    print(description[i:i+60])
#%%
code = auto_plot(csv_path, x, y, plot_type, 
    additional_prompt="""
    Create a figure with figsize=(10,10) before plotting;
    Make sure to use the 'hue' parameter to color the plot by 'yr' column in the table; 
    Hide the legend after plot.""")

# %%
