from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from io import StringIO

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")



@app.route("/analyze", methods=["POST"])
def analyze():
    if request.method == "POST":
        # Get the uploaded CSV file
        csv_file = request.files["csv_file"]
        
        # Read the CSV file into a Pandas DataFrame
        data = pd.read_csv(StringIO(csv_file.read().decode("utf-8")))
        
        # Perform some analyfsfsis on the data
        # For example, let's plot a histogram of the "Amount" column
        graph_function = request.form.get("graph_function", "scatter_plot")

        if graph_function == "line_plot":
           total = data.groupby(['UPI Banks']).agg({'Volume (Mn) By Costumers':'sum'}).reset_index()
           top_10_highest_volume_mn = total.sort_values(by = 'Volume (Mn) By Costumers',ascending = False)
           m=top_10_highest_volume_mn.head(10)
           d=m.set_index('UPI Banks')
           d.plot(kind='bar')
           plt.ylabel('Volume month by customers')
           plt.savefig("static/plot.png")

        elif graph_function == 'desc':
            desc = data.describe()
            table = desc.to_html()
            return render_template("pre.html",table=table)

        elif graph_function == 'head':
            head = data.head()
            table = head.to_html()    
            return render_template("pre.html",table=table)
        
        elif graph_function == "scatter_plot":
            plt.figure(figsize=(10,6))
            sns.lineplot(x="Month",y='Value (Cr) by Costumers',data=data)
            plt.xlabel('Month',fontweight='bold',size = 12) 
            plt.ylabel('Value (Cr) by Customers',fontweight='bold',size = 12) 
            plt.title(" Trend Month v/s Value (Cr) by Customers ",fontweight='bold',size = 12)    
            plt.savefig("static/plot.png")

        elif graph_function == "volume":
            plt.figure(figsize=(10,6))
            sns.set_style("whitegrid")
            sns.lineplot(x='Month',y='Volume (Mn) By Costumers',data=data)
            plt.xlabel('Month',fontweight='bold',size = 12) 
            plt.ylabel('Volume (Mn) By Customers',fontweight='bold',size = 12) 
            plt.title("Trend Month v/s Volume (Mn) By Customers ",fontweight='bold',size = 12)
            plt.savefig("static/plot.png")

        elif graph_function == "value": 
            plt.figure(figsize=(10,6))
            sns.lineplot(x="Month",y='Value (Cr)',data=data)
            plt.xlabel('Month',fontweight='bold',size = 12) 
            plt.ylabel('Value (Cr)',fontweight='bold',size = 12) 
            plt.title(" Trend Month v/s Value (Cr)",fontweight='bold',size = 12) 
            plt.savefig("static/plot.png") 

        elif graph_function == "histogram":
            plt.figure(figsize=(10,6))
            sns.lineplot(x="Month",y='Volume (Mn)',data=data)
            plt.xlabel('Month',fontweight='bold',size = 12) 
            plt.ylabel('Volume (Mn)',fontweight='bold',size = 12) 
            plt.title(" Trend Month v/s Volume (Mn) ",fontweight='bold',size = 12)
            plt.savefig("static/plot.png")
        
        elif graph_function == "phonepay":

            phonePe_Payment = (data.loc[data['UPI Banks'] == 'PhonePe'])

            plt.figure(figsize=(10,6))
            sns.set_style("whitegrid")
            sns.lineplot(x='Month',y='Volume (Mn) By Costumers',data =phonePe_Payment)
            plt.xlabel('Month',fontweight='bold',size = 12) 
            plt.ylabel('Volume (Mn) By Customers',fontweight='bold',size = 12) 
            plt.title("Trend Month v/s Volume (Mn) By Customers for only phonePe_Payment ",fontweight='bold',size = 12)
            plt.savefig("static/plot.png")

        elif graph_function == "gpay":

            phonePe_Payment = (data.loc[data['UPI Banks'] == 'Google Pay'])

            plt.figure(figsize=(10,6))
            sns.set_style("whitegrid")
            sns.lineplot(x='Month',y='Volume (Mn) By Costumers',data =phonePe_Payment)
            plt.xlabel('Month',fontweight='bold',size = 12) 
            plt.ylabel('Volume (Mn) By Costumers',fontweight='bold',size = 12) 
            plt.title("Trend Month v/s Volume (Mn) By Customers for only Google ",fontweight='bold',size = 12)
            plt.savefig("static/plot.png")    

        # Render the results page with the graph
        return render_template("results.html", plot_url="static/plot.png")

if __name__ == "__main__":
    app.run(debug=True)