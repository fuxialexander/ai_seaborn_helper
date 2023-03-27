import openai
import pandas as pd
import seaborn as sns
import io
import sys
import traceback
import matplotlib.pyplot as plt
import json

openai.api_key = "sk-xxxxxxxxxxx"

def load_dataframe(csv_path):
    df = pd.read_csv(csv_path)
    return df

def describe_df(filename):
    df = load_dataframe(filename)
    head = df.head(2).to_string()
    summary = df.describe().to_string()
    prompt = f"Describe what's the data in this table with summary\n{head}\n+{summary}\n;"
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\"\"\""]
    )
    code = response.choices[0].text.strip()
    return code

def generate_plot_code(prompt, x, y, plot_type, filename, first=False):
    if first:
        prompt = f"You are a precise python code generator. You only output code, not other texts. Generate Python code that load file called {filename} in pandas, then a using seaborn to create a {plot_type} plot with x-axis as '{x}' and y-axis as '{y}'." + prompt
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    code = response.choices[0].text.strip()
    return code

def execute_code(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(code)
        # savefig in "plot.png"
        result = "success"
    except Exception as e:
        result = "error"
        traceback.print_exc(file=redirected_output)

    output = redirected_output.getvalue()
    sys.stdout = old_stdout

    return result, output

def auto_plot(filename, x, y, plot_type, additional_prompt=""):
    success = False
    i = 0
    while not success:
        if i==0:
            prompt = additional_prompt
        code = generate_plot_code(prompt, x, y, plot_type, filename, first=(i==0))
        # ask for additional prompt from user
        result, output = execute_code(code)
        # keep only 3rd line and last line of output
        if result == "success":
            success = True
        else:
            output = output.splitlines()[2] + output.splitlines()[-1]
            print(output)
            prompt = f"\nError message:\n{output}\n"
            additional_prompt = input("Additional prompt to help the AI generate better code: ")
            prompt += additional_prompt
            prompt += "Please provide a new code to generate the plot as described above."
        
        i += 1
    return code
