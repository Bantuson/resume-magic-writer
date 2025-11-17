from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from .tools import ResumeParserTool, JobAnalyzerTool, ATSOptimizerTool


@CrewBase
class ResumeMagicWriterCrew:
    """ResumeMagicWriter crew for creating tailored, ATS-optimized resumes"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        # Initialize custom tools
        self.resume_parser_tool = ResumeParserTool()
        self.job_analyzer_tool = JobAnalyzerTool()
        self.ats_optimizer_tool = ATSOptimizerTool()
        self.file_read_tool = FileReadTool()

    @agent
    def resume_data_analyst(self) -> Agent:
        """Agent responsible for structuring raw resume data"""
        return Agent(
            config=self.agents_config["resume_data_analyst"],
            tools=[self.resume_parser_tool, self.file_read_tool],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def job_match_strategist(self) -> Agent:
        """Agent responsible for analyzing job-candidate alignment"""
        return Agent(
            config=self.agents_config["job_match_strategist"],
            tools=[self.job_analyzer_tool, self.ats_optimizer_tool],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def resume_writer(self) -> Agent:
        """Agent responsible for generating the final resume"""
        return Agent(
            config=self.agents_config["resume_writer"],
            tools=[self.ats_optimizer_tool],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def structure_candidate_data(self) -> Task:
        """Task to structure raw candidate data"""
        return Task(
            config=self.tasks_config["structure_candidate_data"],
            agent=self.resume_data_analyst(),
        )

    @task
    def analyze_job_requirements(self) -> Task:
        """Task to analyze job requirements and match to candidate"""
        return Task(
            config=self.tasks_config["analyze_job_requirements"],
            agent=self.job_match_strategist(),
            context=[self.structure_candidate_data()],
        )

    @task
    def generate_tailored_resume(self) -> Task:
        """Task to generate the final tailored resume"""
        return Task(
            config=self.tasks_config["generate_tailored_resume"],
            agent=self.resume_writer(),
            context=[
                self.structure_candidate_data(),
                self.analyze_job_requirements(),
            ],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResumeMagicWriter crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
