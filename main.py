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


        
        
    



    
1111111111111111111111111111111111111111111
def agent_loop(client, messages, verbose):
    
    
    for i in range(MAX_ATTEMPTS):
        try:
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
    
            if not response.candidates:
                print("Agent failed to return a response")
                break
            for candidates in response.candidates:
                
                messages.append(candidates.content) 
            if verbose:
                print(f"{response.candidates[0].content}")
        
    
            if not response.function_calls:
                print("Agent's Final Response:")
                print(response.candidates[0].content.parts[0].text) 
                break
            else:
                function_responses = []  
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose) 
                    if (
                        not function_call_result.parts
                        or not function_call_result.parts[0].function_response
                    ):
                        raise Exception("empty function call result")
                    if verbose:
                        print(f"->{function_call_result.parts[0].function_response.response}") 
                    function_responses.append(function_call_result.parts[0])
                messages.append(genai.types.Content(role="user", parts=function_responses)) 
                       
                
            

     
        except Exception as e:
            print(f"\nError: {e}") 
            break
   
    else:
        print(f"\n{MAX_ATTEMPTS} reached without a final response.")
    
            
            
        
        
                
    
                
        
    
    
    
            
    
    
    
    
                
        
        

        
                
    
    
            
       


            
                    
        
                
        
                  


       
























if __name__ == "__main__":
    main()
