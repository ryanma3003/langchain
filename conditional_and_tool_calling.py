import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
import re


@tool
def calculate(expression: str) -> str:
    """Menghitung ekspresi matematika yang diberikan."""
    try:
        # Membatasi operasi yang diperbolehkan untuk keamanan
        allowed_chars = set("0123456789+-*/().")
        if not all(c in allowed_chars for c in expression):
            return "Ekspresi tidak valid. Hanya boleh menggunakan angka dan operator +, -, *, /, (, )."

        result = eval(expression)
        return f"Hasil perhitungan: {result}"
    except Exception as e:
        return f"Terjadi kesalahan dalam perhitungan: {str(e)}"

# Tool fallback: general_info
@tool
def general_info(query: str) -> str:
    """Mencari informasi berdasarkan kata kunci yang diberikan."""
    search_results = {
        "AI": "Artificial Intelligence (AI) adalah teknologi yang memungkinkan komputer untuk berpikir dan belajar seperti manusia.",
        "Python": "Python adalah bahasa pemrograman populer yang digunakan untuk pengembangan web, data science, dan kecerdasan buatan.",
        "Blockchain": "Blockchain adalah teknologi yang digunakan untuk mencatat transaksi secara terdesentralisasi."
    }
    return search_results.get(query, "Informasi tidak ditemukan.")

@tool
def summarize_information(info: str) -> str:
    """Meringkas informasi utama dari hasil pencarian."""
    if "AI" in info:
        return "AI memungkinkan komputer untuk berpikir dan belajar layaknya manusia."
    elif "Python" in info:
        return "Python adalah bahasa pemrograman serbaguna yang digunakan dalam berbagai bidang."
    elif "Blockchain" in info:
        return "Blockchain adalah sistem pencatatan transaksi yang terdesentralisasi dan aman."
    else:
        return "Informasi tidak tersedia untuk diringkas."

@tool
def generate_report(user_input: str, summary: str) -> str:
    """Membuat laporan singkat berdasarkan hasil ringkasan."""
    report = f"📌 Laporan tentang {user_input}\n"
    report += f"📖 Ringkasan: {summary}\n"
    report += "🔍 Sumber: Data diperoleh dari pencarian AI.\n"
    return report

# Agent Initialization
def run_agent(user_input: str):
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # OpenAi Initialization
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

    if re.search(r'\d+[\+\-\*/]\d+', user_input):
        # agent = initialize_agent(
        #     tools=[calculate],
        #     llm=llm,
        #     agent=AgentType.OPENAI_FUNCTIONS,
        #     verbose=True
        # )

        # response = agent.run(user_input)
        # print("\n✅ **Final Output:**", response)
        return "digit"
    elif "Blockchain" in user_input:  
        # agent = initialize_agent(
        #     tools=[general_info, summarize_information, generate_report],
        #     llm=llm,
        #     agent=AgentType.OPENAI_FUNCTIONS,
        #     verbose=True
        # )

        # # 1️⃣ Cari informasi berdasarkan topik
        # info = agent.run(f"Cari informasi tentang {user_input}")
        # print("Info: \n", info)

        # # 2️⃣ Ringkas informasi yang ditemukan
        # summary = agent.run(f"Ringkas informasi berikut: {info}")
        # print("Summary: \n", summary)

        # # 3️⃣ Buat laporan akhir
        # report = agent.run(f"Buat laporan berdasarkan topik {user_input} dan ringkasan {summary}")
        # print("Laporan Akhir:\n", report)
        return "string"


if __name__ == "__main__":
    print("\n=== Hallo ===")
    run_agent("Hitung 25 * 4 + 10")

    print("\n=== Halo apa yang dapat kami bantu? ===")
    run_agent("Apa itu Blockchain?")
