# Fizz
## Your Personal Financial Consultant
Made by: Robert Bloomquist, Ashish D'Souza, Ananth Kumar, and Sharath Palathingal
### What is Fizz?
Fizz is an interactive personal financial consultant perfect for providing the beginning investor with insight rivaling that of financial experts. Fizz offers numerous services, whether that is analyzing users’ current portfolios, simulating the outcomes of potential transactions, or even advising users to implement simple yet effective risk management strategies.

### What We Used To Implement Fizz:
* **BlackRock Aladdin API** for asset risk data
* **Finnhub.io API** for stock pricing, history, and analysis
* **ReactJS** for UI/UX
* **Flask (on PythonAnywhere)** for as our application framework
* **Google Cloud**
  * **Dialogflow Natural Language Processing (NLP)** for the chatbot's responsivity
  * **Firebase** for storing profile data
* **Apache Cassandra - DataStax Astra** for transferring data between front-end and back-end

### How It Works:
A user opens Fizz and is greeted by a prompt to fill out and upload their portfolio and current holdings. Once uploaded, Fizz analyzes this data and is ready to interact with the user. The user can ask a variety of questions, ranging from "Should I buy stock ABC?" to "Tell me about my current portfolio." Fizz, pulling data from various public APIs and expert recommendations, provides relevant and effective answers to the user's questions.

Visit https://stonkify.xyz to use Fizz!

### Resources:
* https://www.blackrock.com/tools/api-tester/hackathon
* https://financialmodelingprep.com/api/v3
* https://cloud.google.com/dialogflow/docs
* https://www.datastax.com/products/datastax-astra
