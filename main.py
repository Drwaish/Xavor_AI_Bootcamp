""""""
from prompting import prompt_maker
from llm_prompt import create_llm_chain

def main():
    '''
    Driver function to get data.
    '''
    prompt = prompt_maker()
    chain = create_llm_chain()
    print(chain.run(prompt))



if __name__ == "__main__":
   main()