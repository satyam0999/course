
import os
import psycopg2
import psycopg2.extras
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = "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"
os.environ["LANGCHAIN_API_KEY"] = "ls__5670527b7a0f43c683a3fe115273f935"
os.environ["LANGCHAIN_TRACING_V2"] = "true"


hostname = 'database-1.cyoiigtc7vtp.ap-south-1.rds.amazonaws.com'
database = 'CourseFinderDB'
username = 'postgres'
pwd = 'Foreign_123'  
port_id = 5432

def generate_output(question):
    
    db = SQLDatabase.from_uri(f"postgresql://{username}:{pwd}@{hostname}:{port_id}/{database}")
   
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    generate_query = create_sql_query_chain(llm, db)
    
    
    query = generate_query.invoke({"question": question})
    print(query)
    
    # Connect to the PostgreSQL database and execute the query
    try:
        with psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query)
                results = cur.fetchall()
                print(results)
                
                if not results:
                    return "No Universities Matched"
                else:
                    return [dict(record) for record in results]
    except Exception as error:
        print(f"Database or query error: {error}")
        return "Database or query error"

# Example usage of the function
if __name__ == "__main__":
    question = "domain: data science, study level: postgraduate, select course, study level, fees, duration, TOEFL score, college website, scholarship from table, use ILIKE in SQL query"
    results = generate_output(question)
    if isinstance(results, list):
        for result in results:
            print(result)
    else:
        print(results)
