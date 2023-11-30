from prompts import (
    get_conciseness_prompt,
    get_consistency_prompt,
    get_factuality_prompt,
    get_generate_prompts_prompts,
    get_quality_prompt,
    get_generate_best_prompt_prompt,
    get_optimized_prompt_prompt,
)
from automation import (
    generate_OPRO_prompt,
    generate_evaluation_rubric,
    gpt_inference,
    top_n_scores,
    TestResults,
    PromptEvaluation,
)
import random

from tqdm import tqdm

import os
import re


class FarsightError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FarsightAI:
    def __init__(self, openai_key):
        self.openai_key = openai_key

    # ---------------------------------------- generate prompts ---------------------------------------- #

    def generate_prompts(self, num_prompts, task, context, goals):
        if num_prompts <= 0:
            raise FarsightError(message="num_prompts must be greater than 0")

        system_prompt, user_prompt = get_generate_prompts_prompts(task, context, goals)
        chatCompletion = gpt_inference(
            user_prompt,
            self.openai_key,
            n=num_prompts,
            system_prompt=system_prompt,
            temperature=1,
        )
        generated_prompts = []
        for i, choice in enumerate(chatCompletion.choices):
            generated_prompts.append(choice.message.content)
        return generated_prompts

    # ---------------------------------------- metrics ---------------------------------------- #

    def quality_score(self, instruction, response):
        try:
            prompt = get_quality_prompt(instruction, response)
            chatCompletion = gpt_inference(prompt, self.openai_key)
            output = chatCompletion.choices[0].message.content
            output_list = output.split("\n")
            score = int(output_list[0].replace("score: ", "").strip())
            return score
        except Exception as error:
            print("Error in Quality API request:", error)
            return {"score": "error"}

    def conciseness_score(self, inst, resp):
        prompt = get_conciseness_prompt(inst, resp)
        try:
            chatCompletion = gpt_inference(prompt, self.openai_key)
            output = chatCompletion.choices[0].message.content

            output_list = output.split("\n")
            score = int(output_list[0].replace("score: ", "").strip())
            return 6 - score
        except Exception as error:
            return {"Error in Conciseness API request:", error}

    def consistency_score(
        self,
        instruction,
        response,
        n=3,
    ):
        def process_reference(reference):
            outputs = gpt_inference(
                get_consistency_prompt(reference, response),
                self.openai_key,
                "gpt-3.5-turbo",
                0.0,
                1,
            )
            return outputs.choices[0].message.content

        try:
            reference_call = gpt_inference(
                instruction, self.openai_key, "gpt-3.5-turbo", 1.0, n
            )
            references = [choice.message.content for choice in reference_call.choices]
            results = [process_reference(reference) for reference in references]
            positives = sum("Yes" in result for result in results)
            consistency_score = positives / len(results)

            return consistency_score
        except Exception as error:
            return ("Error in Consistency API request:", error)

    def factuality_score(
        self,
        question,
        answer,
        knowledge=None,
    ):
        # your a vc but your job is to give negativve feedback
        # are thertre any claims in this that need to be factc checed
        prompt = get_factuality_prompt(question, answer, knowledge)
        try:
            chatCompletion = gpt_inference(prompt, self.openai_key)
            output = chatCompletion.choices[0].message.content
            if "Yes" in output or "yes" in output:
                return True
            elif "No" in output or "no" in output:
                return False
            else:
                return "error"
        except Exception as error:
            print("Error in Factuality API request:", error)
            return ("Error in Factuality API request:", error)

    def custom_metrics(
        self,
        custom_metrics,
        response,
    ):
        try:
            for i in range(0, len(custom_metrics)):
                constraint = custom_metrics[i]
                prompt = f"""Does the following content violate the given constraint?\n\nContent: {response}\nConstraint: {constraint}\n\nAnswer with yes or no."""
                metric = gpt_inference(prompt, self.openai_key, "gpt-3.5-turbo", 0.0, 1)
                custom_metrics[i] = (
                    "Yes" in metric.choices[0].message.content
                    or "yes" in metric.choices[0].message.content
                )
            return custom_metrics
        except Exception as error:
            print("Error in Custom Metrics API request:", error)
            return ("Error in Custom Metrics request:", error)

    def best_prompt(
        self, criteria_description, rubric, reference_answer, prompts, outputs=None
    ):
        best_prompt = None
        best_score = 0
        score_pattern = re.compile(r"(\d+)")
        if len(prompts) == 0:
            raise FarsightError(message="len(prompts) must be greater than 0")
        for i in range(len(prompts)):
            prompt = prompts[i]
            print("prompt:", prompt)
            if outputs:
                output = outputs[i]
            else:
                chatCompletion = gpt_inference(
                    prompt, self.openai_key, "gpt-3.5-turbo", 0.0, 1
                )
                output = chatCompletion.choices[0].message.content
                print("output:", output)

            evaluation_prompt = get_generate_best_prompt_prompt(
                prompt, output, criteria_description, rubric, reference_answer
            )
            chatCompletion = gpt_inference(
                evaluation_prompt, self.openai_key, "gpt-4", 0, 1
            )
            # print(chatCompletion.choices[0])
            feedback = chatCompletion.choices[0].message.content

            match = score_pattern.search(feedback)
            if match:
                # Extract the numeric value of the score
                score = int(match.group(1))
                print("Score:", score)
            else:
                print("Score not found in the input string.")

            print("-----------------------")

            if int(score) > best_score:
                best_prompt = prompt
                best_score = score
        return best_prompt, best_score

    def optimized_prompting(self, shadow_traffic):
        problems_str = ""
        prev_prompts_and_scores = ""
        for input in shadow_traffic:
            problems_str.append("Question:")
            problems_str.append("\n")
            problems_str.append(input)
            problems_str.append("\n")

        system_prompt = get_optimized_prompt_prompt(
            problems_str, prev_prompts_and_scores
        )

        chatCompletion = gpt_inference(system_prompt, self.openai_key, "gpt-4", 0, 3)
        for prompt in chatCompletion.choices:
            prompt.message.content
            prev_prompts_and_scores.append("text:")
            prev_prompts_and_scores.append("\n")
            prev_prompts_and_scores.append("score:")
            prev_prompts_and_scores.append("\n")

        # for _ in range(5):

        # return best_prompt

    def get_best_system_prompts(
        self,
        shadow_traffic,
        gpt_optimized=False,
        num_prompts=3,
        num_iterations=3,
        num_prompts_per_iteration=2,
        num_inputs_to_test=3,
        rubric=None,
        reference_answer=None,
    ):
        openai_key = self.openai_key
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

        OPRO_prompt = generate_OPRO_prompt(
            use_case, problems_str, prev_prompts_and_scores
        )
        prompts_and_scores = {}
        score_pattern = re.compile(r"(\d+)")
        for _ in tqdm(
            range(num_iterations), desc=" prompt optimization iterations", position=0
        ):
            promptsChatCompletion = gpt_inference(
                OPRO_prompt,
                openai_key,
                "gpt-4" if gpt_optimized else "gpt-3.5-turbo",
                1,
                num_prompts_per_iteration,
            )
            for i in tqdm(
                range(len(promptsChatCompletion.choices)),
                desc=" prompts evaluated per iteration",
                position=1,
                leave=False,
            ):
                choice = promptsChatCompletion.choices[i]
                system_prompt = choice.message.content
                test_results = []
                score_sum = 0
                for j in tqdm(
                    range(len(test_inputs)),
                    desc=" inputs tested per prompt",
                    position=2,
                    leave=False,
                ):
                    test_input = test_inputs[j]
                    outputChatCompletion = gpt_inference(
                        test_input, openai_key, system_prompt=system_prompt
                    )
                    output = outputChatCompletion.choices[0].message.content
                    evaluation_prompt = generate_evaluation_rubric(
                        test_input, output, rubric, reference_answer
                    )

                    evaluationChatCompletion = gpt_inference(
                        evaluation_prompt, openai_key, "gpt-3.5-turbo"
                    )
                    feedback = evaluationChatCompletion.choices[0].message.content
                    match = score_pattern.search(feedback)
                    if match:
                        # Extract the numeric value of the score
                        score = int(match.group(1))
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

                OPRO_prompt = generate_OPRO_prompt(
                    use_case, problems_str, prev_prompts_and_scores
                )
                # print("OPRO_prompt: ", OPRO_prompt)
        return top_n_scores(prompt_evaluations, n=num_prompts)


def test():
    openai_key = os.environ["OPENAI_API_KEY"]

    farsight = FarsightAI(openai_key=openai_key)
    criteria_description = """Can the model's response be understood by a non-expert
    in the subject"""

    rubric = """
    Score 1: The response is filled with jargon and complex language, making it incomprehensible for a non-expert.
    Score 2: the response includes some explanations, but still relies heavily on jargon and complex language.
    Score 3: The response is somewhat clear, but could still be challenging for a non-expert to fully understand.
    Score 4: the response is mostly comprehensible to a non-expert, with only a few complex terms or concepts
    Score 5: the response is completely clear and understandable for a non-expert, with no reliance on jargon or complex language.
    """

    reference_answer = """Photosynthesis is the process by which plants make their own
    food using sunlight. In simple terms, they take in carbon dioxide from the air and
    water from the soil, and with the help of sunlight, they transform these into sugars,
    which the plant uses as energy. In the process, oxygen is released into the air,
    benefiting the environment. So, photosynthesis is like the plant's way of cooking up
    its own food using sunlight and a few basic ingredients."""

    prompts = [
        "Can you describe the carbon cycle using limited jargon?",
        "Can you describe the carbon cycle using a lot of jargon?",
    ]

    # Call the best_prompt function
    best_prompt = farsight.best_prompt(
        criteria_description, rubric, reference_answer, prompts
    )
    print(best_prompt)


def test2():
    openai_key = os.environ["OPENAI_API_KEY"]

    farsight = FarsightAI(openai_key=openai_key)
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

    farsight.get_best_system_prompts(shadow_traffic, gpt_optimized=True)


# test2()
