# import gradio as gr
# from dotenv import load_dotenv
# from research_manager import ResearchManager

# load_dotenv(override=True)

# async def run(query: str):
#     async for chunk in ResearchManager().run(query):
#         yield chunk

# with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
#     gr.Markdown("# Deep Research")
#     query_textbox = gr.Textbox(label="What topic would you like to research?")
#     run_button = gr.Button("Run", variant="primary")
#     report = gr.Markdown(label="Report")
    
#     run_button.click(fn=run, inputs=query_textbox, outputs=report)
#     query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

# ui.launch(inbrowser=True)

import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from clarifying_agent import clarifier_agent, ClarifyingQuestions
from agents import Runner, trace

load_dotenv(override=True)

async def get_clarifying_questions(query: str):
    """Generate clarifying questions for the given query using the clarifier agent"""
    with trace("Clarifying questions"):
        result = await Runner.run(clarifier_agent, input=query)
    return result.final_output.questions

# Global state to track the workflow
workflow_state = {
    "original_query": "",
    "current_question": 0,
    "answers": [],
    "questions": []
}

def reset_workflow():
    """Reset the workflow state"""
    workflow_state["original_query"] = ""
    workflow_state["current_question"] = 0
    workflow_state["answers"] = []
    workflow_state["questions"] = []

async def start_clarifying_questions(query: str):
    """Start the clarifying questions workflow"""
    if not query.strip():
        return "Please enter a research query first.", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    
    # Reset workflow and generate questions for this specific query
    reset_workflow()
    workflow_state["original_query"] = query
    
    try:
        # Generate clarifying questions using the agent
        questions = await get_clarifying_questions(query)
        workflow_state["questions"] = questions
        
        if not questions:
            return "Failed to generate clarifying questions. Please try again.", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
        
        total_questions = len(workflow_state["questions"])
        question_text = f"**Question 1 of {total_questions}:**\n\n{workflow_state['questions'][0]}"
        
        return (
            question_text,
            gr.update(visible=True),  # Show answer textbox
            gr.update(visible=True),  # Show next button
            gr.update(visible=False)  # Hide run research button
        )
    except Exception as e:
        return f"Error generating questions: {str(e)}", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

def handle_answer(answer: str):
    """Handle user's answer and move to next question or finish"""
    if not answer.strip():
        return "Please provide an answer before continuing.", gr.update(), gr.update(), gr.update()
    
    # Store the answer
    workflow_state["answers"].append(answer)
    workflow_state["current_question"] += 1
    
    total_questions = len(workflow_state["questions"])
    
    # Check if we have more questions
    if workflow_state["current_question"] < total_questions:
        question_num = workflow_state["current_question"] + 1
        question_text = f"**Question {question_num} of {total_questions}:**\n\n{workflow_state['questions'][workflow_state['current_question']]}"
        
        return (
            question_text,
            gr.update(value=""),  # Clear answer textbox
            gr.update(visible=True),  # Keep next button visible
            gr.update(visible=False)  # Keep run research button hidden
        )
    else:
        # All questions answered, show summary and run research button
        summary = f"**All questions answered! Here's your research specification:**\n\n"
        summary += f"**Original Query:** {workflow_state['original_query']}\n\n"
        for i, (question, answer) in enumerate(zip(workflow_state['questions'], workflow_state['answers']), 1):
            summary += f"**Q{i}:** {question}\n**A{i}:** {answer}\n\n"
        summary += "Click 'Run Full Research' to begin the comprehensive search."
        
        return (
            summary,
            gr.update(visible=False),  # Hide answer textbox
            gr.update(visible=False),  # Hide next button
            gr.update(visible=True)    # Show run research button
        )

async def run_full_research():
    """Run the full research with original query and clarifications"""
    # Construct enhanced query with clarifications
    enhanced_query = f"{workflow_state['original_query']}\n\nAdditional Context:\n"
    for i, (question, answer) in enumerate(zip(workflow_state['questions'], workflow_state['answers']), 1):
        enhanced_query += f"- Q{i}: {question}\n  A{i}: {answer}\n"
    
    # Run the research
    async for chunk in ResearchManager().run(enhanced_query):
        yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    gr.Markdown("Enter your research topic and answer clarifying questions for better results.")
    
    query_textbox = gr.Textbox(
        label="What topic would you like to research?",
        placeholder="e.g., 'Impact of artificial intelligence on healthcare'"
    )
    
    run_button = gr.Button("Start Research", variant="primary")
    
    # Clarifying questions section (initially hidden)
    with gr.Column(visible=True) as questions_section:
        questions_display = gr.Markdown(value="", visible=True)
        
        answer_textbox = gr.Textbox(
            label="Your Answer",
            placeholder="Please provide your answer...",
            visible=False
        )
        
        next_button = gr.Button("Next Question", visible=False)
        run_research_button = gr.Button("Run Full Research", variant="primary", visible=False)
    
    # Report section
    report = gr.Markdown(label="Research Report")
    
    # Event handlers
    run_button.click(
        fn=start_clarifying_questions,
        inputs=query_textbox,
        outputs=[questions_display, answer_textbox, next_button, run_research_button]
    )
    
    next_button.click(
        fn=handle_answer,
        inputs=answer_textbox,
        outputs=[questions_display, answer_textbox, next_button, run_research_button]
    )
    
    run_research_button.click(
        fn=run_full_research,
        outputs=report
    )
    
    # Allow Enter key in answer textbox to move to next question
    answer_textbox.submit(
        fn=handle_answer,
        inputs=answer_textbox,
        outputs=[questions_display, answer_textbox, next_button, run_research_button]
    )

ui.launch(inbrowser=True)