from crewai import Agent, Task


def build_requirements_agent(llm):
    return Agent(
        role="COMSATS Admission Requirements Specialist",
        goal="Clearly list the admission requirements relevant to the student's intended program(s).",
        backstory="You know COMSATS University Islamabad admission criteria and rely only on the data provided.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def build_requirements_task(agent, profile_text, general_text, programs_text):
    return Task(
        description=(
            "Using ONLY the data below, present the admission requirements relevant to this student.\n\n"
            f"STUDENT PROFILE:\n{profile_text}\n\n"
            f"GENERAL REQUIREMENTS:\n{general_text}\n\n"
            f"RELEVANT PROGRAMS:\n{programs_text}\n\n"
            "Do not judge eligibility. Do not invent requirements. State that the data is sample data."
        ),
        expected_output=(
            "Markdown with sections: General Requirements; then for each relevant program: "
            "Academic requirements, Subject requirements, Test requirements, Other requirements. Concise."
        ),
        agent=agent,
        async_execution=True,
    )
