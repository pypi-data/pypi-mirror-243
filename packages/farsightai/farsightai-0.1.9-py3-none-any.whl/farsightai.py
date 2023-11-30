from openai import OpenAI
from prompts import (
    get_conciseness_prompt,
    get_consistency_prompt,
    get_factuality_prompt,
    get_generate_prompts_prompts,
    get_quality_prompt,
    get_generate_best_prompt_prompt,
    get_optimized_prompt_prompt,
)
import os
import re


class FarsightError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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


# test()
