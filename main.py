#%%
import pandas as pd
from ai import load_dataframe, auto_plot

csv_path = "HPI_master.csv"
x = "hpi_flavor"
y = "index_sa"
plot_type = "boxplot"
#%%
code = auto_plot(csv_path, x, y, plot_type, additional_prompt="Make sure to use the 'hue' parameter to color the plot by year column in the table; return only the code, not any other text. Do not show legend. Remeber the data frame is called 'df'.")
print(f"Plotting code: {code}")

# %%
