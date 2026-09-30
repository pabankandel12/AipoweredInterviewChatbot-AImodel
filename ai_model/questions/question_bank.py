"""Curated, skill-tagged interview records used as the local RAG knowledge base."""

QUESTION_BANK = [
    {"skill": "python", "level": "medium", "question": "Explain how you would structure a Python service that reads data, validates it, and returns a reliable API response.", "rubric": "Discuss separation of concerns, validation, error handling, and testing."},
    {"skill": "javascript", "level": "medium", "question": "How do promises and async/await help you handle asynchronous work in JavaScript? Give a project example.", "rubric": "Explain asynchronous control flow, error handling, and a real use case."},
    {"skill": "react", "level": "medium", "question": "Describe a React component you built. How did you manage its state and keep the interface responsive?", "rubric": "Cover component design, state management, and user experience."},
    {"skill": "node.js", "level": "medium", "question": "How would you design a Node.js endpoint that validates input and handles failures safely?", "rubric": "Mention validation, status codes, error handling, and logging."},
    {"skill": "express", "level": "easy", "question": "What is middleware in Express, and where have you used it?", "rubric": "Explain request-response flow and a practical middleware example."},
    {"skill": "mongodb", "level": "medium", "question": "How would you choose fields and indexes for a MongoDB collection used by an interview application?", "rubric": "Discuss document shape, query patterns, indexes, and trade-offs."},
    {"skill": "mysql", "level": "medium", "question": "How do you design a relational schema that keeps related data consistent?", "rubric": "Discuss keys, normalization, relationships, and constraints."},
    {"skill": "rest api", "level": "medium", "question": "What makes a REST API easy for a frontend team to use and maintain?", "rubric": "Mention resource design, status codes, validation, versioning, and documentation."},
    {"skill": "docker", "level": "hard", "question": "How would containerizing an application improve consistency across local development and deployment?", "rubric": "Explain images, containers, environment configuration, and deployment trade-offs."},
    {"skill": "machine learning", "level": "medium", "question": "Explain how you would evaluate whether a machine-learning feature is useful before deploying it.", "rubric": "Cover data split, metric selection, baseline comparison, and limitations."},
    {"skill": "natural language processing", "level": "medium", "question": "How can text preprocessing affect the quality of an NLP matching system?", "rubric": "Discuss tokenization, normalization, stopwords, and domain vocabulary."},
    {"skill": "data analysis", "level": "medium", "question": "Tell me about an analysis where you turned raw data into a decision or recommendation.", "rubric": "Describe the data, method, finding, and practical impact."},
    {"skill": "general", "level": "easy", "question": "Tell me about a project you are proud of and the contribution you made to it.", "rubric": "Look for a clear role, actions, outcome, and reflection."},
    {"skill": "general", "level": "medium", "question": "Describe a difficult problem you faced in a project. How did you investigate it and what was the result?", "rubric": "Look for structured problem solving, technical reasoning, and measurable outcome."},
    {"skill": "general", "level": "hard", "question": "Describe a technical decision where you had to balance speed, quality, and maintainability.", "rubric": "Look for alternatives, trade-offs, justification, and reflection."},
]
