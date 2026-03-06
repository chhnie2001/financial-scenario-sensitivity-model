## Sample Outputs

### Revenue Scenario Projection
![Revenue Scenario](outputs/revenue_scenario.png)

### Gross Profit Sensitivity Heatmap
![Heatmap](outputs/gross_profit_heatmap.png)

### Break-even Analysis
![Break-even](outputs/break_even_analysis.png)

# Financial Scenario & Sensitivity Modeling

A Python-based financial modeling project that analyzes historical financial performance and simulates forward-looking scenarios using sensitivity analysis and break-even evaluation.

This project demonstrates how financial analysts can combine structured financial data, scenario modeling, and Python-based analytics to support decision-making.

---

# Project Overview

This project builds a simple financial modeling pipeline using historical financial data from **Applied Optoelectronics, Inc. (AAOI)**.

The workflow includes:

• Historical financial data preparation  
• Revenue and cost projection modeling  
• Scenario analysis under different growth assumptions  
• Sensitivity analysis across key variables  
• Break-even evaluation  
• Data visualization and summary outputs  

The goal is to demonstrate **financial modeling, analytical thinking, and Python-based decision support workflows**.

---

# Key Features

### Financial Scenario Modeling

Revenue and cost projections are simulated using parameterized assumptions such as:

- revenue growth rate
- cost structure
- operating margin

The model generates projected financial outcomes under multiple scenarios.

---

### Sensitivity Analysis

The project evaluates how financial outcomes respond to changes in key variables, including:

- revenue growth
- cost structure
- operating leverage

Sensitivity tables help identify the most influential drivers of profitability.

---

### Break-even Analysis

Break-even levels are estimated to understand the revenue threshold required for sustainable profitability.

This helps illustrate downside risk and margin sensitivity.

---

### Data Visualization

The model generates visual outputs such as:

- revenue projections
- profit sensitivity heatmaps
- break-even charts

These help communicate financial insights clearly.

---

# Project Structure


financial-scenario-sensitivity-model

data/
aaoi_financials.csv
fetch_aaoi_financials.py

model/
projection_model.py

notebooks/
scenario_model.ipynb

outputs/
revenue_scenario.png
gross_profit_heatmap.png
break_even_analysis.png
scenario_summary.csv
scenario_summary_with_breakeven.csv

README.md
requirements.txt


---

# Data Source

Historical financial data for **Applied Optoelectronics, Inc. (AAOI)** is maintained through a hybrid workflow:

• Selected financial fields are refreshed using the **SEC EDGAR Company Facts API**  
• A curated annual dataset is preserved locally to ensure continuity and model stability

This approach allows the project to demonstrate automated financial data ingestion while maintaining consistent historical inputs for modeling.

---

# Modeling Logic

The financial model follows a simplified analytical framework.

### Revenue Projection


Revenue = Previous Revenue × (1 + Growth Rate)


### Cost Estimation


Cost = Fixed Cost + Variable Cost Rate × Revenue


### Profit Calculation


Profit = Revenue − Cost


### Margin Calculation


Margin = Profit / Revenue


Sensitivity analysis is then performed by varying model assumptions across multiple scenarios.

---

# Example Outputs

The project produces several analytical outputs.

### Revenue Projection

Revenue scenarios under different growth assumptions.

### Profit Sensitivity

Heatmap illustrating how profitability changes with revenue growth and cost structure.

### Break-even Analysis

Revenue level required to achieve positive operating profit.

---

# How to Run

### Install dependencies


pip install -r requirements.txt


### Refresh financial data


python data/fetch_aaoi_financials.py


### Run the model

Open the notebook:


notebooks/scenario_model.ipynb


Then run all cells to generate analysis outputs.

---

# Skills Demonstrated

This project demonstrates the following capabilities:

- Financial modeling
- Scenario analysis
- Sensitivity analysis
- Business analytics
- Python data analysis
- Data visualization
- Structured analytical workflows

---

# Potential Extensions

Future improvements could include:

- discounted cash flow modeling
- Monte Carlo simulation
- multi-company peer comparison
- automated financial statement parsing

---

# Author

Chu Haonie  
MS Business Analytics – Washington University in St. Louis