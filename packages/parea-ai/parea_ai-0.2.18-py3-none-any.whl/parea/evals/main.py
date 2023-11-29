from dotenv import load_dotenv

from parea.evals.chat import goal_success_ratio
from parea.evals.general import judge_llm_gpt3t, judge_llm_gpt4, lm_vs_lm_factuality_gpt3t, lm_vs_lm_factuality_gpt4, self_check_gpt
from parea.evals.rag import (
    llm_critique_correctness_factory,
    llm_critique_faithfulness_factory,
    precision_response_context_factory,
    ragas_answer_context_faithfulness_factory,
    ragas_answer_relevancy_factory,
    ragas_context_ranking_factory,
    ragas_context_relevancy_factory,
    ragas_percent_target_supported_by_context_factory,
    recall_response,
)
from parea.schemas.models import LLMInputs, Log, Message, ModelParams, Role

load_dotenv("/Users/joschkabraun/dev/project_zero_prompt_engineering/parea-sdk/.env")

if __name__ == "__main__":
    log = Log()

    log.inputs = {
        "context": "I am an artificial intelligence created by OpenAI. I am here to help you with your tasks.",
        "question": "Hello, how are you?",
    }
    log.output = "As an artificial intelligence, I don't have feelings, but I'm here and ready to help you. How can I assist you today?"
    log.target = ""
    log.configuration = LLMInputs(
        model="gpt-3.5-turbo",
        provider="openai",
        model_params=ModelParams(),
        messages=[
            Message(role="user", content="Hello, how are you?"),
        ],
    )

    eval_funcs = [
        # goal_success_ratio,
        # judge_llm_gpt3t,
        # judge_llm_gpt4,
        # self_check_gpt,
        # lm_vs_lm_factuality_gpt4,
        # lm_vs_lm_factuality_gpt3t,
        # precision_response_context_factory(),
        # llm_critique_faithfulness_factory(),
        # recall_response,
        # llm_critique_correctness_factory(),
        # ragas_context_relevancy_factory(),
        # ragas_answer_context_faithfulness_factory(),
        ragas_answer_relevancy_factory(),
        ragas_context_ranking_factory(),
        ragas_percent_target_supported_by_context_factory(),
    ]

    for func in eval_funcs:
        score = func(log)
        print(f"{func.__name__}: {score}")
