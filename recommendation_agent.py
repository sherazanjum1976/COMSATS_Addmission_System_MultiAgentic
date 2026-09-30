from crewai import Agent, Task


def build_recommendation_agent(llm):
    return Agent(
        role="COMSATS Program Advisor",
        goal="Recommend the most suitable COMSATS programs for the student's background, subjects and interests.",
        backstory="You are an academic counselor who matches students to programs realistically.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def build_recommendation_task(agent, profile_text, all_programs_text):
    return Task(
        description=(
            "Recommend suitable programs from the list below for this student.\n\n"
            f"STUDENT PROFILE:\n{profile_text}\n\n"
            f"AVAILABLE COMSATS PROGRAMS (sample data):\n{all_programs_text}\n\n"
            "Consider background group, subjects, marks, entry test and interests. Only recommend programs from the list."
        ),
        expected_output=(
            "Markdown ranking of 3-5 programs. For each: Program name; Why it fits; "
            "Eligibility considerations; Missing requirements (or 'None identified')."
        ),
        agent=agent,
        async_execution=True,
    )
