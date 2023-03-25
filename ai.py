
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

def send_dfframe_to_gpt(df):
    head = df.head().to_string()
    summary = df.describe().to_string()

    prompt = f"Here is the head of the dataframe called 'df' :\n{head}\n\n;"
    return prompt

def generate_plot_code(prompt, x, y, plot_type):
    prompt += f"Generate Python code using seaborn to create a {plot_type} plot with x-axis as '{x}' and y-axis as '{y}'."
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    code = response.choices[0].text.strip()
    return code

def execute_code(code, df):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    local_vars = {"df": df, "sns": sns}
    try:
        exec(code, None, local_vars)
        # savefig in "plot.png"
        plt.show()
        plt.savefig("plot.png")
        result = "success"
    except Exception as e:
        result = "error"
        traceback.print_exc(file=redirected_output)

    output = redirected_output.getvalue()
    sys.stdout = old_stdout

    return result, output

def auto_plot(filename, x, y, plot_type, additional_prompt=""):
    df = load_dataframe(filename)
    prompt = additional_prompt + send_dfframe_to_gpt(df)
    success = False

    while not success:
        code = generate_plot_code(prompt, x, y, plot_type)
        print(code)
        result, output = execute_code(code,df)

        if result == "success":
            success = True
        else:
            prompt = f"\n\nError message:\n{output}\n\n"
            prompt += "Please provide a new code to generate the plot as described above."
            prompt +=additional_prompt

    return code
