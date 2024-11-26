from crewai import Crew
from agents.analyst_agent import AnalystAgent
from tasks.analysis_task import AnalysisTasks
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    
    # Cria o agente analista
    analyst = AnalystAgent(
        supabase_url=os.getenv('SUPABASE_URL'),
        supabase_key=os.getenv('SUPABASE_KEY')
    ).get_agent()
    
    # Instancia as tasks
    analysis_tasks = AnalysisTasks()
    task = analysis_tasks.analyze_retail_data(analyst)

    # Configura e executa a crew
    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    print("\n=== RESULTADO DA ANÁLISE DE VAREJO ===")
    print(result)
    return result

if __name__ == "__main__":
    main()
