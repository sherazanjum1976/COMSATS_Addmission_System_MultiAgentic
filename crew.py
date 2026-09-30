import os

# Set BEFORE importing crewai: no telemetry/tracing prompts, writable storage on Streamlit Cloud
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")
os.environ.setdefault("CREWAI_STORAGE_DIR", "/tmp/crewai")

from crewai import LLM, Crew, Process

from data import all_programs_text, general_requirements_text, target_programs_text
from eligibility_agent import build_eligibility_agent, build_eligibility_task
from recommendation_agent import build_recommendation_agent, build_recommendation_task
from requirements_agent import build_requirements_agent, build_requirements_task
from summary_agent import build_summary_agent, build_summary_task

MODEL = "groq/openai/gpt-oss-120b"  # Groq via CrewAI's LiteLLM integration


def _llm():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY is not set. Add it in Streamlit Secrets.")
    return LLM(model=MODEL, api_key=key, temperature=0.2, timeout=120)


def _clean(text):
    # CrewAI treats {braces} as template variables; remove them from user text
    return str(text).replace("{", "(").replace("}", ")")


def _profile_text(p):
    return _clean(
        f"Name: {p['name']}\n"
        f"Qualification status: {p['qualification']}\n"
        f"{p['matric_system']} percentage: {p['matric_pct']}%\n"
        f"Intermediate/A-Level group: {p['background']}\n"
        f"Intermediate/A-Level percentage: {p['inter_pct']}%\n"
        f"CGPA: {p['cgpa']}\n"
        f"Subjects: {p['subjects']}\n"
        f"Entry test: {p['entry_test']}\n"
        f"Preferred program: {p['preferred'] or 'Not sure'}\n"
        f"Skills/interests: {p['interests']}\n"
        f"Other info: {p['extra']}"
    )


def run_admission_crew(profile: dict) -> dict:
    profile_text = _profile_text(profile)
    general = general_requirements_text()
    targets = target_programs_text(profile["preferred"], profile["background"])
    everything = all_programs_text()

    # Independent agents (each with its own LLM instance)
    req_agent = build_requirements_agent(_llm())
    elig_agent = build_eligibility_agent(_llm())
    rec_agent = build_recommendation_agent(_llm())
    sum_agent = build_summary_agent(_llm())

    # Three async tasks -> run concurrently. Eligibility gets requirement data directly
    # from data.py, so it does NOT wait for the Requirements Agent.
    t_req = build_requirements_task(req_agent, profile_text, general, targets)
    t_elig = build_eligibility_task(elig_agent, profile_text, general, targets)
    t_rec = build_recommendation_task(rec_agent, profile_text, everything)

    # Only this final task waits for the three async tasks (via context)
    t_sum = build_summary_task(sum_agent, [t_req, t_elig, t_rec], _clean(profile["name"]))

    crew = Crew(
        agents=[req_agent, elig_agent, rec_agent, sum_agent],
        tasks=[t_req, t_elig, t_rec, t_sum],
        process=Process.sequential,
        verbose=False,
    )
    crew.kickoff()

    def out(task):
        return task.output.raw if task.output else "No output returned."

    return {
        "requirements": out(t_req),
        "eligibility": out(t_elig),
        "recommendation": out(t_rec),
        "summary": out(t_sum),
    }
