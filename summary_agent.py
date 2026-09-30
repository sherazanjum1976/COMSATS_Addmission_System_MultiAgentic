from crewai import Agent, Task


def build_summary_agent(llm):
    return Agent(
        role="Admission Summary Writer",
        goal="Combine the specialist reports into a short, friendly summary for the student.",
        backstory="You write clear, encouraging, honest summaries for students and parents.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def build_summary_task(agent, context_tasks, student_name):
    return Task(
        description=(
            f"Write a concise, student-friendly final summary for {student_name} using the three reports in context "
            "(requirements, eligibility, recommendations). Do not add new facts."
        ),
        expected_output=(
            "Under 200 words: overall assessment, top recommended program(s), key next steps. "
            "End with: 'This result is AI-generated using sample data. Please verify with the latest official "
            "COMSATS University Islamabad admission policies.'"
        ),
        agent=agent,
        context=context_tasks,
        async_execution=False,
    )
