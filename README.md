# COMSATS University Islamabad – Multi-Agent Admission Assistant

MVP built with Python, Streamlit, CrewAI and Groq (`openai/gpt-oss-120b`).
**Uses SAMPLE data in `data.py`. Not official – verify with COMSATS.**

## Agents
- Requirements Agent (`requirements_agent.py`)
- Eligibility Agent (`eligibility_agent.py`)
- Program Recommendation Agent (`recommendation_agent.py`)
- Summary Agent (`summary_agent.py`) – merges the three reports

## How parallel execution works
In `crew.py`, the Requirements, Eligibility and Recommendation tasks use
`async_execution=True`, so CrewAI runs each in its own thread at the same time.
The Eligibility Agent reads requirement data directly from `data.py`, so it
does not wait for the Requirements Agent. Only the final Summary task waits,
because it lists the three async tasks in `context`. Each parallel task uses
a different agent (required by current CrewAI).

## Deploy (no local install)
1. Push all files to a GitHub repo.
2. On https://share.streamlit.io create an app, select the repo, main file `app.py`.
3. Advanced settings → Python 3.11, and in Secrets add:
   `GROQ_API_KEY = "your_key_here"`
4. Deploy.

## Update requirements
Edit `PROGRAMS` / `GENERAL_REQUIREMENTS` in `data.py`, commit, and the app redeploys.
