''' LLM prmpting for effecient working '''
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

LLM = ChatOpenAI(
      model="gpt-4",
      temperature=0.2,
      max_tokens=1024
    )
NAME = ['asthama', 'dengue_fever']
DESCRIPTION = ["Good for asthama related queries.", "Good for dengue_fever related queries."]
PROMPT_TEMPLATE = [ """You are a exceptionally professional allergy specialist doctor. \
 Provide insights, medicines and remedies against data provided by patient. \
 Data consist of History, body vitals and description of allergy. Data in CONTEXT \
 should be use as a CONTEXT in a  final answer. \
 Answer must be in JSON format that consist of doctor's views,\
 medicine and remedies as a keys.

Here is a Data:
{input}
""", 
"""You are a exceptionally professional dengue fever specialist doctor. \
 Provide insights, medicines and remedies against data provided by patient. \
 Data consist of History, body vitals and description of allergy.Data in CONTEXT \
 should be use as a CONTEXT in a  final answer. \
 Answer must be in JSON format that consist of doctor's views,\
 medicine and remedies as a keys.

Here is a Data:
{input}
"""
]
MULTI_PROMPT_ROUTER_TEMPLATE = """When presented with a raw text input for a \
language model in the context of medical prompts,\
 identify the most appropriate model prompt for the input. \
You will receive the names of the available prompts along with descriptions indicating their\
suitability for specific purposes within the medical domain. Additionally,\
you have the option to modify the original input if you believe that revising it will result\
in a more effective response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \ name of the prompt to use or "DEFAULT"
    "next_inputs": string \ a potentially modified version of the original input
}}}}
```

REMEMBER: "destination" MUST be one of the candidate prompt \
names specified below OR it can be "DEFAULT" if the input is not\
well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""

def create_prompt_info(prompt_data : dict)->dict:
    """
    Create information of all available prompts.

    Parameters
    ----------
    prompt_data
        Contain name, description and tempalte of prompts.
    
    Return
    ------
     Dictionary
    """
    prompt_infos = []
    # print(prompt_data)
    name = prompt_data["disease_name"]
    description =  prompt_data['description']
    prompt_template = prompt_data['prompt_template']
    for i, data in enumerate(name) :
        info = {}
        info["name"] = data
        info["description"] = description[i]
        info["prompt_template"] = prompt_template[i]
        prompt_infos.append(info)
    return prompt_infos

def create_destinations_chain():
    """
    Create chains for prompts.

    Parameters
    ----------
    prompt_infos
        Contain all prompts.
    
    Return
    ------
      str, str, dictionary
    """
    default_prompt = ChatPromptTemplate.from_template("{input}")
    default_chain = LLMChain(llm=LLM, prompt=default_prompt)
    prompt_info1 = {'disease_name': NAME,
                    'description': DESCRIPTION,
                    'prompt_template': PROMPT_TEMPLATE}
    prompt_infos = create_prompt_info(prompt_info1)
    destination_chains = {}
    for p_info in prompt_infos:
        name = p_info["name"]
        prompt_template = p_info["prompt_template"]
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = LLMChain(llm=LLM, prompt=prompt)
        destination_chains[name] = chain
    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    destinations_str = "\n".join(destinations)
    return default_chain, destinations_str, destination_chains

def create_llm_chain():
    default_chain, destinations_str, destination_chains = create_destinations_chain()
    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations=destinations_str
    )
    router_prompt = PromptTemplate(
                    template=router_template,
                    input_variables=["input"],
                    output_parser=RouterOutputParser(),
                )

    router_chain = LLMRouterChain.from_llm(LLM, router_prompt)
    memory = ConversationBufferWindowMemory(llm=LLM, input_key='input', output_key= 'text')
    chain = MultiPromptChain(router_chain=router_chain,
                         destination_chains=destination_chains,
                         default_chain=default_chain,
                         verbose= True,
                         memory= memory,
                        )
    return chain

if __name__ == "__main__":
    print(create_llm_chain())