def get_consistency_prompt(context, sentence):
    prompt = f"""
        Context: "{context}"
        Answer: "{sentence}"
        Does the answer convey the same meaning as the context above?
        Answer Yes or No:
    """

    return prompt


def get_factuality_prompt(question, answer, knowledge):
    if knowledge:
        prompt = f"You are a fact checker. Given a question and an answer, determine if the answer is factually consistent with the provided context.\n\nQuestion:\n{question}\n\nAnswer:\n{answer}\n\nContext:\n{knowledge}\n\nIs the answer factually consistent with the context? Output a one-word answer (yes or no)."
    else:
        prompt = f"You are a fact checker. Given a question and an answer, determine if the answer is factually consistent.\n\nQuestion:\n{question}\n\nAnswer:\n{answer}\nIs the answer factually consistent? Output a one-word answer (yes or no)."
    return prompt


def get_quality_prompt(inst, resp):
    prompt = f"""

    Below is an instruction from an user and a candidate answer. Evaluate whether or not the answer is a good example of how AI Assistant should respond to the user’s 
    instruction. Please assign a score using the following 5-point scale:

    1: It means the answer is incomplete, vague, off-topic, controversial, or not exactly what the user asked for. For example, some content seems missing, numbered
    list does not start from the beginning, the opening sentence repeats user’s question. Or the response is from another person’s perspective with their personal experience
    (e.g. taken from blog posts), or looks like an answer from a forum. Or it contains promotional text, navigation text, or other irrelevant information.
    
    2: It means the answer addresses most of the asks from the user. It does not directly address the user’s question. For example, it only provides a high-level
    methodology instead of the exact solution to user’s question.
    
    3: It means the answer  is helpful but not written by an AI Assistant. It addresses all the basic asks from the user. It is complete and self contained with the
    drawback that the response is not written from an AI assistant’s perspective, but from other people’s perspective. The content looks like an excerpt from a blog post,
    web page, or web search results. For example, it contains personal experience or opinion, mentions comments section, or share on social media, etc.
    
    4: It means the answer is written from an AI assistant’s perspective with a clear focus of addressing the instruction. It provide a complete, clear, and
    comprehensive response to user’s question or instruction without missing or irrelevant information. It is well organized, self-contained, and written in a
    helpful tone. It has minor room for improvement, e.g. more concise and focused.
    
    5: It means it is a perfect answer from an AI Assistant. It has a clear focus on being a helpful AI Assistant, where the response looks like intentionally written
    to address the user’s question or instruction without any irrelevant sentences. The answer provides high quality content, demonstrating expert knowledge in the area, is
    very well written, logical, easy-to-follow, engaging and insightful.

    Please assign a score in the following format:

    score: <rating>
    instruction: "{inst}"
    response: "{resp}"
    """
    return prompt


def get_conciseness_prompt(inst, resp):
    prompt = f"""
    Evaluate the conciseness of the AI Assistant's response on a scale of 1 to 5, with 5 being extremely verbose and 1 being exceptionally concise.

    1. Very Concise 
    2. Concise 
    3. Balanced 
    4. Somewhat Verbose 
    5. Extremely Verbose

    Please assign a score in the following format:
    score: <rating>

    instruction: "{inst}"
    response: "{resp}"
    """
    return prompt


def get_generate_prompts_prompts(task, context, goals):
    system_prompt = """You are a helpful prompt generation assistant. Users will provide you with information that you will leverage to create a task-specific prompt for use with another large language model. The information you will be provided with will be:
    Task: A simple description of the user's desired usage of the large language model.
    Context: Additional description of the target use case and sometimes user provided examples.
    Goals: A comma-separated list of any other constraints/goals that the user wants the downstream language model to follow. Example: [Be concise, don't generate incorrect information]
    Placeholders: A comma-separated list of placeholders that are required to be in the prompt. These placeholders MUST be represented in the generated prompt. Example: [{question}, {knowledge}]

    Leverage all of this user-provided information to generate a very concise prompt."""
    user_prompt = f"""Task: {task}
                    Context: {context}
                    Goals: {goals}
                    Placeholders: [(question), (knowledge)]"""
    return system_prompt, user_prompt


def get_generate_best_prompt_prompt(
    inst, resp, criteria_description, rubric, reference_answer
):
    system_prompt = f"""###Task Description:
        An instruction (might include an Input inside it), a response to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
        1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
        2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric.
        3. The output format should look as follows: \"Feedback: (write a feedback for criteria) [RESULT] (an integer number between 1 and 5)\"
        4. Please do not generate any other opening, closing, and explanations.

        ###The instruction to evaluate:
        {inst}

        ###Response to evaluate:
        {resp}

        ###Reference Answer (Score 5):
        {reference_answer}

        ###Score Rubrics:
        [{criteria_description}]
        {rubric}

        ###Feedback: """
    return system_prompt
