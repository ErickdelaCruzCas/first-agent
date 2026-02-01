import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function



def main():
    print("Hello from first-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if api_key is None:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Make sure it is set in a .env file."
        )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    # Loop for iterative agent behavior (max 20 iterations)
    for iteration in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            )
        )

        usage = response.usage_metadata

        if args.verbose:
            print(f"Iteration {iteration + 1}:")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")

        # Add response candidates to conversation history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # Check if the response contains function calls
        if response.candidates[0].content.parts[0].function_call:
            function_results = []

            # Iterate over function calls and execute them
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    # Call the function
                    function_call_result = call_function(part.function_call, verbose=args.verbose)

                    # Validate the result
                    if not function_call_result.parts:
                        raise RuntimeError("Function call result has no parts")

                    if function_call_result.parts[0].function_response is None:
                        raise RuntimeError("Function response is None")

                    if function_call_result.parts[0].function_response.response is None:
                        raise RuntimeError("Function response.response is None")

                    # Add to list of function results
                    function_results.append(function_call_result.parts[0])

                    # Print verbose output
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

            # Append function results to messages as user content
            messages.append(types.Content(role="user", parts=function_results))
        else:
            # No function calls, print the final response and exit
            print("Final response:")
            print(response.text)
            return

    # If we reach here, max iterations were hit without a final response
    print("Error: Maximum iterations reached without a final response from the agent.")
    exit(1)

if __name__ == "__main__":
    main()





