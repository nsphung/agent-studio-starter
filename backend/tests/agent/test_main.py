from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.models import LiteLLMModel
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

# OpenAI model
model = LiteLLMModel(
    model="github_copilot/gpt-5-mini",  # Provider must be specified
    api_key="your-api-key",  # optional, can be set via environment variable
    base_url="your-api-base",  # optional, for custom endpoints
    temperature=1.0,
    allowed_openai_params=["logprobs", "top_logprobs"],
)

# Sample to show how we could test with LLM as Judge. In practice, you would replace the `actual_output` with the output from your LLM application and set the `expected_output` to what you anticipate the correct answer should be. The `retrieval_context` can be used to provide any relevant information that the LLM might need to generate its response.


def test_case_failure() -> None:
    correctness_metric = GEval(
        model=model,
        name="Correctness",
        criteria="Determine if the 'actual output' is correct based on the 'expected output'.",
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
        threshold=0.5,
    )
    helpfulness = GEval(
        model=model,
        name="Helpfulness",
        criteria="Determine whether the `actual output` is helpful in answering the `input`.",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    )

    test_case = LLMTestCase(
        input="What's the weather in sf ?",
        # Replace this with the actual output from your LLM application
        actual_output="The weather in San Francisco is currently 68 degrees Fahrenheit with clear skies.",
        expected_output="It's freezing in San Francisco with a high of 50 degrees Fahrenheit and strong winds.",
        retrieval_context=["Weather report: 50 degrees Fahrenheit and strong winds."],
    )
    assert_test(test_case, [correctness_metric, helpfulness])


def test_case_success() -> None:
    correctness_metric = GEval(
        model=model,
        name="Correctness",
        criteria="Determine if the 'actual output' is correct based on the 'expected output'.",
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
        threshold=0.5,
    )

    test_case = LLMTestCase(
        input="What's the weather in sf ?",
        # Replace this with the actual output from your LLM application
        actual_output="It's freezing in San Francisco with a high of 50 degrees Fahrenheit and strong winds.",
        expected_output="It's freezing in San Francisco with a high of 50 degrees Fahrenheit and strong winds.",
        retrieval_context=["Weather report: 50 degrees Fahrenheit and strong winds."],
    )
    assert_test(test_case, [correctness_metric])
