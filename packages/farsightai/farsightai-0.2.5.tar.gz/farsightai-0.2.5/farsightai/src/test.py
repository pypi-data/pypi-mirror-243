import pytest
import os

from farsightai import (
    FarsightAI,
)

"""
To run tests run the following commands: 

echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
source ~/.zshrc
echo $OPENAI_API_KEY

"""
openai_key = os.environ["OPENAI_API_KEY"]

inst = "who is the president of the united states"
resp = "As of my last knowledge update in January 2022, Joe Biden is the President of the United States. However, keep in mind that my information might be outdated as my training data goes up to that time, and I do not have browsing capabilities to check for the most current information. Please verify with up-to-date sources."
farsight = FarsightAI(openai_key=openai_key)


def test_custom_metrics():
    # Call the custom_metrics function
    custom_metric = farsight.custom_metrics(["do not mention Joe Biden"], resp)
    print(custom_metric)
    # Assert that custom_metric is a list
    assert isinstance(custom_metric, list)
    # Assert that all elements in the list are booleans
    assert all(isinstance(metric, bool) for metric in custom_metric)


def test_consistency_metrics():
    # Call the consistency_metric function
    consistency_score_metric = farsight.consistency_score(inst, resp)
    # Assert that consistency_metric is a list
    print(consistency_score_metric)
    assert isinstance(consistency_score_metric, float)


def test_quality_metrics():
    # Call the quality_metric function
    quality_score_metric = farsight.quality_score(inst, resp)
    # Assert that quality_metric is a list
    assert isinstance(quality_score_metric, int)
    assert quality_score_metric > 0
    assert quality_score_metric <= 5


def test_conciseness_metrics_short():
    # Call the conciseness_metric function
    resp = "Joe Biden"
    conciseness_score_metric = farsight.conciseness_score(inst, resp)
    print(resp)
    print(conciseness_score_metric)
    # Assert that conciseness_metric is a list
    assert isinstance(conciseness_score_metric, int)
    assert conciseness_score_metric > 0
    assert conciseness_score_metric >= 3
    assert conciseness_score_metric <= 5


def test_conciseness_metrics_long():
    # Call the conciseness_metric function
    resp = "As of my last knowledge update in January 2022, Joe Biden is the President of the United States. However, keep in mind that my information might be outdated as my training data goes up to that time, and I do not have browsing capabilities to check for the most current information. Please verify with up-to-date sources.As of my last knowledge update in January 2022, Joe Biden is the President of the United States. However, keep in mind that my information might be outdated as my training data goes up to that time, and I do not have browsing capabilities to check for the most current information. Please verify with up-to-date sources."
    conciseness_score_metric = farsight.conciseness_score(inst, resp)
    # Assert that conciseness_metric is a list
    print(resp)
    print(conciseness_score_metric)

    assert isinstance(conciseness_score_metric, int)
    assert conciseness_score_metric > 0
    assert conciseness_score_metric <= 3


def test_factuality_metrics_no_knowledge():
    # Call the factuality_metric function
    resp = "As of my last knowledge update in January 2022, Katie Pelton is the President of the United States. However, keep in mind that my information might be outdated as my training data goes up to that time, and I do not have browsing capabilities to check for the most current information. Please verify with up-to-date sources."
    factuality_score_metric = farsight.factuality_score(inst, resp)
    # Assert that factuality_metric is a boolean
    assert isinstance(factuality_score_metric, bool)
    assert not factuality_score_metric


def test_factuality_metrics_false():
    # Call the factuality_metric function
    resp = "As of my last knowledge update in January 2022, Katie Pelton is the President of the United States. However, keep in mind that my information might be outdated as my training data goes up to that time, and I do not have browsing capabilities to check for the most current information. Please verify with up-to-date sources."
    factuality_score_metric = farsight.factuality_score(inst, resp, None)
    # Assert that factuality_metric is a boolean
    assert isinstance(factuality_score_metric, bool)
    assert not factuality_score_metric


def test_factuality_metrics_true():
    # Call the factuality_metric function
    factuality_score_metric = farsight.factuality_score(inst, resp, None)
    # Assert that factuality_metric is a boolean
    assert isinstance(factuality_score_metric, bool)
    assert factuality_score_metric


def test_generate_prompts():
    # Call the prompts function
    task = "you are a wikipedia chatbot"
    context = "the year is 2012"
    goals = ["answer questions"]
    num_prompts = 5

    prompts = farsight.generate_prompts(num_prompts, task, context, goals)
    # Assert that prompts is a list
    assert isinstance(prompts, list)
    assert len(prompts) == num_prompts
    # Assert that all elements in the list are str
    assert all(isinstance(prompt, str) for prompt in prompts)


def test_generate_prompts_negative_num_prompts():
    # Call the prompts function
    task = "you are a wikipedia chatbot"
    context = "the year is 2012"
    goals = ["answer questions"]
    num_prompts = -1
    # Assert that generate_prompts raises error
    with pytest.raises(Exception) as context:
        farsight.generate_prompts(num_prompts, task, context, goals)
    assert "num_prompts must be greater than 0" in context.value.message


### this test takes a long time to run, uncomment if necessary ###
# def test_best_prompt():
#     criteria_description = """Can the model's response be understood by a non-expert
#     in the subject"""

#     rubric = """
#     Score 1: The response is filled with jargon and complex language, making it incomprehensible for a non-expert.
#     Score 2: the response includes some explanations, but still relies heavily on jargon and complex language.
#     Score 3: The response is somewhat clear, but could still be challenging for a non-expert to fully unsterdtnad.
#     Score 4: the response is mostly comprehensible to a non-expert, with only a few complex terms or concepts
#     Score 5: the response is completely clear and understandable for a non-expert, with no reliance on jargon or complex language.
#     """

#     reference_answer = """Photosynthesis is the process by which plants make their own
#     food using sunlight. In simple terms, they take in carbon dioxide from the air and
#     water from the soil, and with the help of sunlight, they transform these into sugars,
#     which the plant uses as energy. In the process, oxygen is released into the air,
#     benefiting the environment. So, photosynthesis is like the plant's way of cooking up
#     its own food using sunlight and a few basic ingredients."""

#     prompts = [
#         "Can you describe the carbon cycle using limited jargon?",
#         "Can you describe the carbon cycle using a lot of jargon??",
#     ]

#     # Call the best_prompt function
#     best_prompt, score = farsight.best_prompt(
#         criteria_description, rubric, reference_answer, prompts
#     )
#     print(best_prompt, score)
#     # Assert that custom_metric is a list
#     assert isinstance(best_prompt, str)
#     assert isinstance(best_prompt, int)


def run_all_tests():
    # Run all test functions in this file
    pytest.main([__file__])

    # # Run specific test functions within this file
    # pytest.main([__file__ + "::test_best_prompt"])

    # Run multiple specific test functions
    # pytest.main(
    #     [
    #         __file__ + "::test_custom_metrics",
    #         __file__ + "::test_consistency_metrics",
    #         __file__ + "::test_quality_metrics",
    #         __file__ + "::test_conciseness_metrics_short",
    #         __file__ + "::test_conciseness_metrics_long",
    #         __file__ + "::test_factuality_metrics_no_knowledge",
    #         __file__ + "::test_factuality_metrics_false",
    #         __file__ + "::test_factuality_metrics_true",
    #         __file__ + "::test_generate_prompts",
    #     ]
    # )


run_all_tests()
