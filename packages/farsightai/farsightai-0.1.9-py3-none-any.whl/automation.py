import random
from farsightai import gpt_inference
import os
import re
from tqdm import tqdm


class PromptEvaluation:
    def __init__(self, prompt, score, test_results):
        self.system_prompt = prompt
        self.score = score
        self.test_results = test_results

    def __repr__(self) -> str:
        return f"PromptEvaluation(score={self.score}, system_prompt={self.system_prompt}, test_results={self.test_results})"

    def __str__(self):
        return f"PromptEvaluation(score={self.score}, system_prompt={self.system_prompt}, test_results={self.test_results})"


class TestResults:
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

    print("rubric: ", rubric)
    return rubric


def generate_reference_answer(use_case, rubric, shadow_traffic, apikey):
    prompt = f"""Given this use case: {use_case} and this question {shadow_traffic[0]}


Please generate a reference answer that would receive a score of 5 according to the rubric. Ensure that the reference answer is tailored to the specific criteria outlined in the rubric.

Rubric:
{rubric}

Please provide a reference answer that demonstrates a perfect score of 5 in terms of clarity of explanation. Thank you!"""

    chatCompletion = gpt_inference(prompt, apikey)
    reference_answer = chatCompletion.choices[0].message.content

    print("reference_answer: ", reference_answer)
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


def get_best_system_prompts(
    shadow_traffic,
    gpt_optimized=False,
    num_prompts=3,
    num_iterations=3,
    num_prompts_per_iteration=2,
    num_inputs_to_test=3,
    rubric=None,
    reference_answer=None,
):
    openai_key = os.environ["OPENAI_API_KEY"]
    if not rubric or not reference_answer:
        # use_case = generate_use_case_from_shadow_traffic(shadow_traffic, openai_key)
        use_case = """A financial institution wants to improve its HR services by implementing an internal HR chatbot.
        The chatbot's main objective is to assist employees with their HR-related queries while ensuring the protection of their private 
        personal information. The chatbot will be designed to answer various questions such as current job openings in the company, application 
        procedures for specific positions, the status of job applications, information about the company's benefits and perks, policies on remote work 
        or flexible schedules, updating personal information in the HR system, employee onboarding processes, available training and development 
        opportunities, performance evaluation procedures, and information about employee assistance programs or wellness initiatives. By providing 
        accurate and timely responses, the chatbot aims to enhance employee satisfaction and streamline HR processes within the financial institution."""

        if not rubric:
            # rubric = generate_rubric_from_use_case(use_case, openai_key)
            rubric = """
                ### Score Rubric:
                Overall Evaluation:
                Score 1: The chatbot responses are consistently inaccurate and provide incorrect information, leading to confusion and frustration for employees.
                Score 2: The chatbot responses are often inaccurate and may provide incorrect information, causing some confusion for employees.
                Score 3: The chatbot responses are generally accurate, but there may be occasional instances of incorrect or incomplete information.
                Score 4: The chatbot responses are mostly accurate, with only a few instances of incorrect or incomplete information.
                Score 5: The chatbot responses are consistently accurate and provide correct information, ensuring clarity and reliability for employees.
            """
        if not reference_answer:
            # reference_answer = generate_reference_answer(
            #     use_case, rubric, shadow_traffic, openai_key
            # )
            reference_answer = """The current job openings in the company are as follows:

            1. Senior Financial Analyst: This position requires a strong background in financial analysis and reporting. The responsibilities include conducting financial research, analyzing financial statements, and providing recommendations to improve financial performance. Interested candidates should have a bachelor's degree in finance or a related field and at least 5 years of experience in financial analysis.

            2. Customer Service Representative: We are looking for individuals with excellent communication skills and a customer-centric approach. The role involves handling customer inquiries, resolving complaints, and providing exceptional service. Candidates should have a high school diploma or equivalent and prior customer service experience is preferred.

            3. IT Support Specialist: This position requires technical expertise in troubleshooting hardware and software issues. The responsibilities include providing technical support to employees, installing and configuring software, and maintaining computer systems. Interested candidates should have a bachelor's degree in computer science or a related field and at least 2 years of experience in IT support.

            4. Compliance Officer: We are seeking individuals with a strong understanding of regulatory requirements and compliance frameworks. The role involves developing and implementing compliance policies, conducting audits, and ensuring adherence to legal and industry standards. Candidates should have a bachelor's degree in business, finance, or a related field and at least 3 years of experience in compliance.

            5. Marketing Coordinator: This position requires creativity and strong organizational skills. The responsibilities include assisting in the development and execution of marketing campaigns, managing social media platforms, and coordinating events. Interested candidates should have a bachelor's degree in marketing or a related field and prior experience in marketing or advertising.

            Please note that these job openings are subject to change and additional positions may become available in the future. For more information on specific job requirements and application procedures, please visit our company's career page or contact the HR department directly."""

    problems_str = ""
    prev_prompts_and_scores = ""
    for input in shadow_traffic[:5]:
        problems_str += "\tQuestion:"
        problems_str += "\n\t"
        problems_str += input
        problems_str += "\n"

    test_inputs = random.sample(shadow_traffic, num_inputs_to_test)
    prompt_evaluations = []

    OPRO_prompt = generate_OPRO_prompt(use_case, problems_str, prev_prompts_and_scores)
    prompts_and_scores = {}
    # print("test_input: ", test_input)
    score_pattern = re.compile(r"(\d+)")
    # print("OPRO_prompt:", OPRO_prompt)
    for _ in tqdm(range(num_iterations), desc=" prompt optimization", position=0):
        promptsChatCompletion = gpt_inference(
            OPRO_prompt,
            openai_key,
            "gpt-4" if gpt_optimized else "gpt-3.5-turbo",
            1,
            num_prompts_per_iteration,
        )
        for i in tqdm(
            range(len(promptsChatCompletion.choices)),
            desc=" prompts evaluated",
            position=1,
            leave=False,
        ):
            choice = promptsChatCompletion.choices[i]
            system_prompt = choice.message.content
            test_results = []
            # print("------------------------------")

            # print("system_prompt: ", system_prompt)
            score_sum = 0
            for j in tqdm(
                range(len(test_inputs)), desc=" inputs tested", position=2, leave=False
            ):
                test_input = test_inputs[j]
                outputChatCompletion = gpt_inference(
                    test_input, openai_key, system_prompt=system_prompt
                )
                output = outputChatCompletion.choices[0].message.content
                # print("------------------------------")

                # print("output: ", output)
                evaluation_prompt = generate_evaluation_rubric(
                    test_input, output, rubric, reference_answer
                )
                # print("evaluation_prompt: ", evaluation_prompt)

                evaluationChatCompletion = gpt_inference(
                    evaluation_prompt, openai_key, "gpt-3.5-turbo"
                )
                feedback = evaluationChatCompletion.choices[0].message.content
                match = score_pattern.search(feedback)
                if match:
                    # Extract the numeric value of the score
                    score = int(match.group(1))
                    print("Score:", score)
                    score_sum += score
                    test_results.append(TestResults(test_input, output, score))
                else:
                    print("Score not found in the input string.")

            avg_score = score_sum / num_inputs_to_test
            prev_prompts_and_scores += "\n\ttext:"
            prev_prompts_and_scores += "\n\t"
            prev_prompts_and_scores += system_prompt
            prev_prompts_and_scores += "\n"

            prev_prompts_and_scores += "\tscore:"
            prev_prompts_and_scores += "\n\t"
            prev_prompts_and_scores += str(avg_score)
            prev_prompts_and_scores += "\n"
            prompts_and_scores[system_prompt] = avg_score
            prompt_evaluations.append(
                PromptEvaluation(system_prompt, avg_score, test_results)
            )
            print(prompt_evaluations)

            OPRO_prompt = generate_OPRO_prompt(
                use_case, problems_str, prev_prompts_and_scores
            )
            # print("OPRO_prompt: ", OPRO_prompt)
    return top_n_scores(prompt_evaluations, n=num_prompts)


def test():
    shadow_traffic = [
        "What are the current job openings in the company?",
        "How can I apply for a specific position?",
        "What is the status of my job application?",
        "Can you provide information about the company's benefits and perks?",
        "What is the company's policy on remote work or flexible schedules?",
        "How do I update my personal information in the HR system?",
        "Can you explain the process for employee onboarding?",
        "What training and development opportunities are available for employees?",
        "How is performance evaluation conducted in the company?",
        "Can you assist with information about employee assistance programs or wellness initiatives?",
    ]

    get_best_system_prompts(shadow_traffic, gpt_optimized=True)


test()
