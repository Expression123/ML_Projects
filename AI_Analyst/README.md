# AI DATA ANALYST

---

This project analyzes dataset uploaded by a user and outputs a detailed report.

---

## Project Overview

---

As a data scientist, having an agentic solution that gives me insights, information about a  particular dataset before  modelling is something i have always thought of. I probably will still do analysis myself but i will know the things to look for and things to look deeper for. The application is built for data analysts/scientists who just need an idea of what they will be working with. The project can also be used by anyone who wants a detailed, analysis on a dataset.
The application gives a full detailed result of dataset. it inspects, cleans and analyzes the dataset.***

### Key Features

---

- Data Upload
- Automated DAtaset Inspection
- AI Cleaning Plan generation
- AI assisted data cleaning
- Automated Analysis
- Markdown report generation
- Emailing Agent
- Downloadable Analysis report
- Optional Target column Selection

---



# System Architecture

```
                ┌─────────────────┐
                │   User Upload   │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Inspection Agent│
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Cleaning Planner│
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Cleaning Agent  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Analysis Agent  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │  Report Agent   │
                └────────┬────────┘
                         ↓
            ┌────────────┴────────────┐
            ↓                         ↓
    Markdown Report             HTML / Email
```



# Agent Workflow

---

- Inspection Agent:This Agent gives the workflow the gist of the dataset like preliminary findings. The tools used are inspect_dataset, inspect categorical columns and inspect outliers
- Cleaning Plan Agent: THe cleaning planner uses the output from the insection agent to create a structured plan on how to go about the cleaning process. I did this so the cleaner will not just do anything to avoid dataquality issues because during testing i had some issues with cleaner doing it alone.
- CleaningAgent: Thie agent makes the data set more suitable for use. It removes duplicates, drop missing rows and does column convertion etc. The agent is equiped with tools to makee this happen.The agent strictly follows the cleaning output from cleaning plan
- Analysis Agent: This is the agent that does the brain work i would say because it uses outut from earlier ageents to with tools it is equipped with to study the data set closely to understand its true meaning and inner relationships.  
- Report Agent simply gives us the output of every thing that has been done in a nicely formatted way(Markdown) and also sends us an email with the report. The report agent also uses MCP to save the generated report in the specified location***



## Tools And Technologies

---



### Technology	                Purpose

- Python	                            Core application
- Pandas	                            Data processing
- OpenAI Agents SDK	    Agent orchestration
- Pydantic	                            Structured outputs
- MCP	                            Filesystem integration
- Gradio	                            User interface
***



## DEsign Decisions

- I used a manual pipiline (The workflow is orchestrated by an agent) because i wanted full control of what was happening and i wanted it to follow that path.
- I used structured pydantic output through the project because i already know what im expecting and most importantly how i will use the output.
- In the project, outliers are only detected and not modified because i ran into serious issues when i was modifying for examlple the agent might assume that a particular column is imbalanced removing lots of rows from the dataset while in that imbalance is the reality of the dataset.
- I used a shared shared analystcontext in the project so agents can easily access the outputs of other agents.

## Project Structure
AI_Analyst/
│                   
├── app/            
│   ├── agents/
│   ├── context/
│   ├── mcp/
│   ├── pipeline/
│   ├── prompts/
│   ├── tools/
│   ├── frontend.py
│   └── main.py
│
├── data/
├── sandbox/
├── .env
└── README.md


## Future Improvements 
- Visualization Agent
- LLM based orchestration
- Persistent report hisory
- More dataset formats

## Author 
***
Ibrahim Gbade
Data Scientist / Machine Learning Engineer
***
