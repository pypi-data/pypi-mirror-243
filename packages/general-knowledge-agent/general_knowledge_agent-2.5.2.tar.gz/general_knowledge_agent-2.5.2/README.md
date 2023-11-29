<p align="center">
    <img src="https://www.nearlyhuman.ai/wp-content/uploads/2022/04/virtual-copy.svg" width="200"/>
</p>

# Nearly Human General Knowledge Agent

An AI-powered knowledge assistant, ready to answer your questions, provide insights, and assist with a wide range of general knowledge inquiries.

Generalizable to any client with their respective data. Configuration details shown below.

## Prerequisites

- Mamba

## Installing as a Dependency
### Mamba
Add as a dependency to any `conda.yml` file
```
- git+https://github.com/nearlyhuman/general-knowledge-agent.git@main
```

### Pip
Install into current Python virtual environment
```
pip install git+https://github.com/nearlyhuman/general-knowledge-agent.git@main
```

## Usage
### Import as dependency
```
from general_knowledge_agent.agent import GeneralKnowledgeAgent

class MyNewAgent(GeneralKnowledgeAgent):
   pass
```

## Configuration
### cortex.yml
Every Cortex model requires a cortex.yml configuration file in order to run.

The following are a list of parameters which may be configured to support any particular client.
```
params:
  - deployment_name: "gpt-35-16k"
  - model: "gpt-3.5-turbo-16k"
  - system_prompt: "Some system prompt"
  - prompt_template: "
  Possible Document Section Context: {context}

  Instruction: {instruction}
  "
  - prompt_variables: ['instruction', 'context']
  - inquiry_system_prompt: "
  Given the following user prompt and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n
  You should follow the following rules when generating and answer:\n
  - Always prioritize the user prompt over the conversation log.\n
  - Ignore any conversation log that is not directly related to the user prompt.\n
  - If the user prompt is unreleated to the conversation log, return the user prompt as the answer.\n
  - Only attempt to answer if a question was posed.\n
  - The question should be a single sentence.\n
  - You should remove any words that are not relevant to the question.

  Example 1:\n  

  CONVERSATION LOG: User: Test\n
  Assistant: What is your question?\n\n

  USER PROMPT: What can you assist me with?\n\n

  Final answer: What can you assist me with?
  "
  - inquiry_template: "
  CONVERSATION LOG: {conversation_history}\n\n

  USER PROMPT: {user_prompt}\n\n

  Final answer:"
  - inquiry_variables: ['user_prompt', 'conversation_history']
  - inquiry_temperature: 0.1
  - max_retries: 2
  - timeout: 14
  - chroma_directory: "data/chroma_db"
  - temperature: 0
  - context_dropout_threshold: 0.8
  - expose_section_headers: True
  - model_version: 1

training_steps:
  - setup_azure_openai_access: "Setup Azure OpenAI API access"
  - initialize: "Initialize model"
  - read_docs: "Read documents"
  - preprocess_docs: "Preprocess documents"
  - fine_tune: "Fine-tune model with LangChain"
  - thread_batch_eval_pipe: "Evaluate model"
  - setup_deployment_variables: "Setup deployment variables"

deployment_steps:
  - setup_azure_openai_access: "Setup Azure OpenAI API access"
  - fine_tune: "Fine-tune model with LangChain"
```
