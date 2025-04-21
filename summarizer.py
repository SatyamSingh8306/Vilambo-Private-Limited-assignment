from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()


GEMINI_API_KEY= os.environ.get("GEMINI_API_KEY")

def summarizeEmail(body):
    prompt = PromptTemplate(
        template="""Acting like a Good Reader and Writer, summarize the body of the email in 3 sentences. 

        NOTE: SUMMARIZE IN EXACTLY 3 SENTENCES AND RETURN ONLY THE SUMMARY. 
        Body: {body}

        SUMMARY:
        """,
        input_variables=["body"]
    )   
    parser = StrOutputParser()

    model = ChatGroq(
        model="gemma2-9b-it"
    )
    chain = prompt | model | parser

    result = chain.invoke({"body": body})
    return result

if __name__ =="__main__":
    ans = summarizeEmail("Hii i am Satyam Singh")
    print(ans)