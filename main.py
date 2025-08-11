from ast import arguments
import sys
import os
from google import genai # type: ignore
from google.genai import types # type: ignore
from dotenv import load_dotenv # type: ignore

from prompts import system_prompt
from call_function import call_function, available_functions

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    

        
    agent_loop(client, messages, verbose)


        
        
    



    




def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    messages.append(response.candidates[0].content)
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text
    if response.function_calls:
        
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose) 
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Error:Fatal") 
            if verbose:
            
                    print(f"-> {function_call_result.parts[0].function_response.response}") 
            response_message = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                        response={"result": function_call_result.parts[0].function_response.response}, 
                    )
                ]
            )
            messages.append(response_message) 
        return response_message
            
        
        
        
                
    
    
            
       
        

        
               
    


MAX_ATTEMPTS = 20 
def agent_loop(client, messages, verbose):   
    for i in range(MAX_ATTEMPTS):
        result = generate_content(client, messages, verbose)
        try: 
                
            generate_content(client, messages, verbose) 
            if result.response.text:
                
                 
                print(f'{}') 
                break
                
        
                  


        except Exception as e: 
            print(f"Error: {e}") 
            break 

    else: 
        print(f"Max iterations ({MAX_ATTEMPTS}) reached.")
























if __name__ == "__main__":
    main()
