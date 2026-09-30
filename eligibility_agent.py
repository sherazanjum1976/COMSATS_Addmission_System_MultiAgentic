from crewai import Agent, Task


def build_eligibility_agent(llm):
    return Agent(
        role="COMSATS Eligibility Evaluator",
        goal="Assess whether the student appears eligible by comparing the profile with the requirement data.",
        backstory="You are a careful admissions officer who compares each criterion fairly and never guesses missing facts.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def build_eligibility_task(agent, profile_text, general_text, programs_text):
    return Task(
        description=(
            "Compare the student profile against the requirement data below.\n\n"
            f"STUDENT PROFILE:\n{profile_text}\n\n"
            f"GENERAL REQUIREMENTS:\n{general_text}\n\n"
            f"PROGRAM REQUIREMENTS:\n{programs_text}\n\n"
            "Rules: use only the given data; if information is missing (e.g. entry test not taken), "
            "mark it as pending, not failed."
        ),
        expected_output=(
            "The FIRST line must be exactly one of:\n"
            "STATUS: Eligible\nSTATUS: Potentially Eligible\nSTATUS: Requirements Not Met\n"
            "Then markdown with: Satisfied requirements (bullets); Missing/pending requirements (bullets); "
            "Explanation (2-4 sentences). If multiple programs are given, give the overall status on the first line "
            "and a one-line status per program."
        ),
        agent=agent,
        async_execution=True,
    )
