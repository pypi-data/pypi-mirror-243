import os
import re
from tqdm import tqdm
from openai import OpenAI


# ---------------------------------------- gpt function ----------------------------------------
def gpt_inference(
    content, apiKey, model="gpt-3.5-turbo", temperature=0.0, n=1, system_prompt=None
):
    client = OpenAI(api_key=apiKey)
    if system_prompt:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]
    else:
        messages = [{"role": "user", "content": content}]
    chatCompletion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        n=n,
    )
    return chatCompletion


class PromptEvaluation:
    def __init__(self, prompt, score, test_results):
        self.system_prompt = prompt
        self.score = score
        self.test_results = test_results

    def __repr__(self) -> str:
        return f"PromptEvaluation(score={self.score}, system_prompt={self.system_prompt}, test_results={self.test_results})"

    def __str__(self):
        return f"PromptEvaluation(score={self.score}, system_prompt={self.system_prompt}, test_results={self.test_results})"


class TestResult:
    def __init__(self, input, output, score):
        self.input = input
        self.score = score
        self.output = output

    # def __repr__(self) -> str:
    #     return (
    #         f"TestResults(score={self.score}, input={self.input}, output={self.output})"
    #     )

    def __str__(self):
        return (
            f"TestResults(score={self.score}, input={self.input}, output={self.output})"
        )


def top_n_scores(eval_list, n=3):
    # Sort the list of PromptEvaluation objects based on scores in descending order
    sorted_evaluations = sorted(eval_list, key=lambda x: x.score, reverse=True)

    # Take the top n evaluations
    top_n_evaluations = sorted_evaluations[:n]

    return top_n_evaluations


def generate_use_case_from_shadow_traffic(shadow_traffic, apiKey, correct_outputs=None):
    prompt = f"""
        Here is an example use case: 
            To develop a secure and efficient internal HR chatbot for a financial
            institution that assists employees with HR-related queries while ensuring the 
            protection of private personal information.
        Given the example questions below: 
            {shadow_traffic}
        Can you describe a use case that summarize a chatbot answering questions similar to these questions?
        """

    chatCompletion = gpt_inference(prompt, apiKey)
    use_case = chatCompletion.choices[0].message.content
    # print("use_case: ", use_case)
    return use_case


def generate_rubric_from_use_case(use_case, apikey):
    prompt = f"""Given this use case: {use_case}

    I would like you to create a single, consolidated evaluation rubric for effectively evaluating chat bot responses. Please structure the rubric as follows:

    ### Score Rubrics:
    Overall Evaluation:
    Score 1: score1_description
    Score 2: score2_description
    Score 3: score3_description
    Score 4: score4_description
    Score 5: score5_description

    Consider the overall effectiveness of the chat bot responses in addressing the use case above in your consolidated evaluation.

    Example:
    ### Score Rubric:
    Overall Evaluation:
    Score 1: The response is filled with jargon and complex language, making it incomprehensible for a non-expert.
    Score 2: the response includes some explanations, but still relies heavily on jargon and complex language. 
    Score 3: The response is somewhat clear, but could still be challenging for a non-expert to fully understand. 
    Score 4: the response is mostly comprehensible to a non-expert, with only a few complex terms or concepts
    Score 5: the response is completely clear and understandable for a non-expert, with no reliance on jargon or complex language.

    Ensure that the rubric focuses on providing an overall evaluation rather than breaking down into multiple categories. Thank you!
    """

    chatCompletion = gpt_inference(prompt, apikey)
    rubric = chatCompletion.choices[0].message.content

    # print("rubric: ", rubric)
    return rubric


def generate_reference_answer(use_case, rubric, shadow_traffic, apikey):
    prompt = f"""Given this use case: {use_case} and this question {shadow_traffic[0]}


Please generate a reference answer that would receive a score of 5 according to the rubric. Ensure that the reference answer is tailored to the specific criteria outlined in the rubric.

Rubric:
{rubric}

Please provide a reference answer that demonstrates a perfect score of 5 in terms of clarity of explanation. Thank you!"""

    chatCompletion = gpt_inference(prompt, apikey)
    reference_answer = chatCompletion.choices[0].message.content

    # print("reference_answer: ", reference_answer)
    return reference_answer


def generate_evaluation_rubric(inst, resp, rubric, reference_answer):
    system_prompt = f"""###Task Description:
        An instruction (might include an Input inside it), a response to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
        1. Write a score that is an integer between 1 and 5. You should refer to the score rubric.
        3. The output format should look as follows: \"Score: (an integer number between 1 and 5)\"
        4. Please do not generate any other opening, closing, and explanations.

        ###The instruction to evaluate:
        {inst}

        ###Response to evaluate:
        {resp}

        ###Reference Answer (Score 5):
        {reference_answer}

        {rubric}

        ###Feedback: """
    return system_prompt


def generate_OPRO_prompt(use_case, problems_str, prev_prompts_and_scores):
    system_prompt = f"""
    You are a helpful prompt generation assistant. Users will provide you with information that you will leverage to create a task-specific prompt for use with another large language model. The information you will be provided with will be:
    Previous System Prompts: previous system prompts and their scores. 
    Example instructions: Example instructions to the system. 
    Your task is to generate the system prompt <SYS>. Below are some previous system prompts with their scores.
    The score ranges from 1 to 5.

    {prev_prompts_and_scores}

    Here is your use_case:
    {use_case}

    Below are some sample instructions.
    {problems_str}

    Generate an system prompt that is different from all the system prompts <SYS> above, and has a higher score
    than all the system prompts <SYS> above. The system prompt should begin with <SYS> and end with </SYS>.
    The system prompt should be concise, effective, and generally applicable to all inputs above.

    Here is an example: 

    <SYS>  You are a conversational chatbot from the year 2012. Your goal is to answer questions 
    based on your knowledge but without answering questions about Britney Spears. I'm here to help! Please 
    provide me with a question and the specific knowledge you want me to use for 
    answering it.</SYS>
    """
    return system_prompt


# test()
