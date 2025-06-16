from textwrap import dedent

pages = [
  {
    "id": "123",
    "title": "SmartGarden Monitor",
    "content": dedent("""
                      # 🌱 SmartGarden Monitor

                      **Topic:** Internet of Things (IoT)  
                      **Type:** Demo Project Description

                      ## Overview

                      SmartGarden Monitor is an end-to-end IoT solution designed to help hobbyist gardeners remotely track and optimize the health of their indoor and outdoor plants. By leveraging a network of low-power sensors, cloud data storage, and a user-friendly mobile dashboard, SmartGarden Monitor demonstrates how projects can seamlessly retrieve and present rich, topic-specific descriptions—in this case, plant-care use cases in the IoT domain.

                      ---

                      ## 🔧 Key Features

                      - **Sensor Network**
                        - Soil moisture, ambient temperature, light intensity, and humidity sensors
                        - MQTT-based data streaming to a central hub

                      - **Cloud Backend**
                        - Serverless data ingestion (AWS Lambda)
                        - Time-series storage in a managed database (InfluxDB)
                        - RESTful API for querying historical and real-time data

                      - **Mobile Dashboard**
                        - React Native app for iOS and Android
                        - Visual charts for sensor trends and alerts
                        - Push notifications when environmental thresholds are crossed

                      - **Topic-Driven Description Retrieval**
                        - Demonstrates how the app fetches project descriptions from a MongoDB store
                        - Keyword-matching logic to select appropriate content based on the selected topic (e.g. “IoT”)
                        - Example: querying “smart farming” returns this project

                      ---

                      ## 🧱 Tech Stack

                      - **Hardware:** ESP32 microcontrollers, DHT22 sensors, capacitive soil moisture probes  
                      - **Cloud Services:** AWS IoT Core, AWS Lambda, Amazon API Gateway, InfluxDB Cloud  
                      - **Database:** MongoDB Atlas (for project descriptions by topic)  
                      - **Frontend:** React Native, VictoryCharts  
                      - **Backend:** Node.js with Express.js, MQTT.js

                      ---

                      ## 🚀 Demo Workflow

                      1. **User selects a topic** (e.g., “IoT”)
                      2. **App retrieves** matching project descriptions from the database
                      3. **User taps** on “SmartGarden Monitor” and sees this full description
                      4. **User navigates** to a live dashboard showing real-time sensor data

                      ---

                      ## 🧠 Why This Demo?

                      This dummy project showcases your app’s core feature: dynamically fetching and displaying detailed, topic-relevant project descriptions. It highlights a complete IoT pipeline and serves as a tangible use case for retrieving structured content based on user intent.
                    """).strip()
  },
  {
    "id": "456",
    "title": "AutoResume Builder",
    "content": dedent("""
                      # 🧠 AutoResume Builder

                      **Topic:** Natural Language Processing (NLP)  
                      **Type:** Demo Project Description

                      ## Overview

                      AutoResume Builder is an AI-powered tool that helps users generate professional resumes by simply describing their skills, experiences, and career goals in natural language. This project showcases how NLP techniques can be used to parse, structure, and enhance unstructured input into polished, domain-specific documents.

                      The app demonstrates the retrieval of project descriptions by topic—in this case, "NLP"—and presents a full overview with relevant technical components and a clear use case.

                      ---

                      ## ✨ Key Features

                      - **Natural Language Input Parsing**
                        - Users describe their work history and goals in plain English
                        - NLP model extracts and categorizes skills, roles, dates, and achievements

                      - **Resume Template Generator**
                        - Dynamically fills resume templates with extracted data
                        - Multiple professional templates to choose from (PDF output)

                      - **LLM-Powered Content Enhancement**
                        - Large Language Model (LLM) polishes user-provided content
                        - Suggests improvements to tone, structure, and clarity

                      - **Topic-Aware Description Retrieval**
                        - This project is fetched from a topic index labeled "NLP"
                        - Demonstrates how topic-based descriptions help users understand real-world NLP applications

                      ---

                      ## 🧱 Tech Stack

                      - **Frontend:** Next.js + TailwindCSS  
                      - **Backend:** FastAPI with spaCy + Hugging Face Transformers  
                      - **LLM:** OpenAI GPT-4 or similar for content polishing  
                      - **Database:** PostgreSQL (user data), MongoDB (project descriptions)  
                      - **PDF Generation:** WeasyPrint or Puppeteer

                      ---

                      ## 🚀 Demo Workflow

                      1. **User selects the “NLP” topic** from a list
                      2. **App retrieves** the AutoResume Builder project description and displays it
                      3. **User provides** a paragraph about their work experience
                      4. **NLP pipeline** extracts entities and fills the resume automatically
                      5. **LLM enhances** the content and generates a PDF-ready resume

                      ---

                      ## 🧠 Why This Demo?

                      AutoResume Builder shows the power of NLP for document automation. It also highlights how your app retrieves and displays rich project descriptions based on selected topics, enabling quick discovery and inspiration for developers and learners."""
                    ).strip()
  }
]