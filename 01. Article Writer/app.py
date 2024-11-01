import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def create_crew(topic):
    # Initialize LLM
    llms = ChatGroq(
        model="groq/llama-3.1-8b-instant",
        api_key=os.getenv("Groq_API_Key"),
    )

    # Agent: Content Planner
    planner = Agent(
        role="Content Planner",
        goal=f"Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article "
        f"about the topic: {topic}."
        "You collect information that helps the "
        "audience learn something "
        "and make informed decisions. "
        "Your work is the basis for "
        "the Content Writer to write an article on this topic.",
        allow_delegation=False,
        verbose=True,
        llm=llms,
    )

    # Agent: Content Writer
    writer = Agent(
        role="Content Writer",
        goal=f"Write insightful and factually accurate "
        f"opinion piece about the topic: {topic}",
        backstory="You're working on a writing "
        f"a new opinion piece about the topic: {topic}. "
        "You base your writing on the work of "
        "the Content Planner, who provides an outline "
        "and relevant context about the topic. "
        "You follow the main objectives and "
        "direction of the outline, "
        "as provide by the Content Planner. "
        "You also provide objective and impartial insights "
        "and back them up with information "
        "provide by the Content Planner. "
        "You acknowledge in your opinion piece "
        "when your statements are opinions "
        "as opposed to objective statements.",
        allow_delegation=False,
        verbose=True,
        llm=llms,
    )

    # Agent: Content Editor
    editor = Agent(
        role="Editor",
        goal="Edit a given blog post to align with "
        "the writing style of the organization. ",
        backstory="You are an editor who receives a blog post "
        "from the Content Writer. "
        "Your goal is to review the blog post "
        "to ensure that it follows journalistic best practices,"
        "provides balanced viewpoints "
        "when providing opinions or assertions, "
        "and also avoids major controversial topics "
        "or opinions when possible.",
        allow_delegation=False,
        verbose=True,
        llm=llms,
    )

    # Task: Content Planner
    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, "
            f"and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering "
            "their interests and pain points.\n"
            "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
        agent=planner,
    )

    # Task: Content Writer
    write = Task(
        description=(
            "1. Use the content plan to craft a compelling "
            f"blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
            "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
        agent=writer,
    )

    # Task: Content Editor
    edit = Task(
        description=(
            "Proofread the given blog post for "
            "grammatical errors and "
            "alignment with the brand's voice."
        ),
        expected_output="A well-written blog post in markdown format, "
        "ready for publication, "
        "each section should have 2 or 3 paragraphs.",
        agent=editor,
    )

    # Create Crew
    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        process=Process.sequential,
        verbose=True,
    )

    # Generate the article
    result = crew.kickoff(inputs={"topic": topic})
    return result


def main():
    # Set page configuration
    st.set_page_config(page_title="AI Article Generator", page_icon="✍️", layout="wide")

    # Title
    st.title("🖊️ AI-Powered Article Generator")

    # Topic input
    topic = st.text_input(
        "Enter the topic for your article:",
        placeholder="e.g., Rivalry between Nikola Tesla and Thomas Edison",
    )

    # Generate button
    if st.button("Generate Article", type="primary"):
        # Validate input
        if not topic:
            st.error("Please enter a topic!")
            return

        # Show loading spinner
        with st.spinner("Generating your article... This might take a few moments."):
            try:
                # Generate the article
                article = create_crew(topic)

                # Display the article
                st.markdown("## 📄 Generated Article")
                st.markdown(article)

            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Sidebar information
    st.sidebar.info(
        "💡 How it works:\n"
        "1. Enter a topic\n"
        "2. Click 'Generate Article'\n"
        "3. AI agents will plan, write, and edit the article"
    )


# Run the app
if __name__ == "__main__":
    main()
