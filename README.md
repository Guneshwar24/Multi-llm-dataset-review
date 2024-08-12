# LLM vs PandasAI for Interactive Data Analysis

This project demonstrates two approaches to interactive data analysis using Language Models (LLMs): a standard LLM approach and a PandasAI-enhanced approach. Both implementations use Streamlit for the user interface and support multiple LLM providers (OpenAI, Anthropic, and Ollama).

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Comparison of Approaches](#comparison-of-approaches)
6. [Why PandasAI?](#why-pandasai)
7. [Limitations](#limitations)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

This project consists of two main scripts:
1. `standard_llm_analysis.py`: Uses a standard LLM approach for data analysis.
2. `pandasai_analysis.py`: Utilizes PandasAI for enhanced data analysis capabilities.

Both scripts allow users to upload CSV files, select an LLM provider, and interactively ask questions about their data.

## Features

- Support for multiple LLM providers: OpenAI, Anthropic, and Ollama
- CSV file upload functionality
- Interactive chat interface for querying data
- Real-time data preview
- Persistent chat history
- Error handling and informative error messages

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/llm-data-analysis-comparison.git
   cd llm-data-analysis-comparison
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install streamlit pandas pandasai langchain-openai langchain-anthropic langchain-community python-dotenv
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Usage

1. Run the standard LLM analysis script:
   ```
   streamlit run standard_llm_analysis.py
   ```

2. Run the PandasAI-enhanced analysis script:
   ```
   streamlit run pandasai_analysis.py
   ```

3. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Upload a CSV file, choose an LLM provider, and start asking questions about your data.

## Comparison of Approaches

### Standard LLM Approach (`standard_llm_analysis.py`)
- Uses LangChain to interact with various LLM providers
- Processes queries using a custom `process_query` function
- Provides natural language responses based on the data
- Limited ability to perform direct calculations or data manipulations
<img width="1440" alt="Skjermbilde 2024-08-12 kl  03 32 33" src="https://github.com/user-attachments/assets/4202b69e-28a8-4648-8077-75f429222a6e">
<img width="1440" alt="Skjermbilde 2024-08-12 kl  03 32 37" src="https://github.com/user-attachments/assets/bb3482df-4be2-4c52-9ac4-6452a2562f90">


### PandasAI Approach (`pandasai_analysis.py`)
- Uses PandasAI's SmartDataframe for enhanced data analysis
- Capable of performing direct calculations and data manipulations
- Generates and executes Python code to answer queries
- Provides more accurate and specific answers for data-related questions
<img width="1440" alt="Skjermbilde 2024-08-12 kl  03 32 41" src="https://github.com/user-attachments/assets/5b58254c-1d33-478f-8ea6-aca321eb6fa4">


## Why PandasAI?

PandasAI offers several advantages over the standard LLM approach for data analysis:

1. **Direct Calculations**: PandasAI can perform calculations and data manipulations on the spot, providing numerical answers to queries like "What's the average salary?" or "How many employees are in each department?"

2. **Code Generation**: PandasAI generates and executes Python code to answer queries, allowing for more complex data operations.

3. **Data-Aware Responses**: The SmartDataframe is aware of the data structure and can provide more accurate and specific answers based on the actual data content.

4. **Flexibility**: PandasAI can handle a wide range of data-related tasks, from simple summaries to complex aggregations and visualizations.

5. **Iterative Analysis**: Users can ask follow-up questions based on previous results, enabling a more interactive and in-depth analysis process.

## Limitations

While PandasAI offers significant advantages, it's important to note some limitations:

1. **Complexity**: PandasAI may introduce additional complexity compared to the simpler standard LLM approach.

2. **Resource Usage**: PandasAI may require more computational resources, especially for large datasets or complex queries.

3. **Learning Curve**: Users may need to familiarize themselves with PandasAI-specific features and capabilities.

## Contributing

Contributions to improve this comparison or extend the functionality of either approach are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
