# CodexTutor: Socratic AI Learning Interface

**An advanced generative AI platform engineered for instructional scaffolding and self-discovery.**

CodexTutor is a specialized Socratic Wrapper for Large Language Models (LLMs). Unlike traditional Ai assistants that act as direct answer engines, CodexTutor is designed as a pedagogical tool that guides students through complex academic problems using incremental, non-directive questioning. By withholding the final solution, the application ensures that the learner remains the primary cognitive agent in the problem-solving process.

## Educational Philosophy

The application is built on the Socratic Method, a form of cooperative dialogue that stimulates deep learning and critical thinking.

* Instructional Scaffolding: Providing temporary support to students as they develop new skills, gradually removing assistance as mastery increases.
* Active Inquiry: Forcing users to discover analytical breakthroughs through a series of pointed, logical questions.
* Misconception Diagnosis: Leveraging LLM reasoning to identify where a student's logic is failing and redirecting them without providing the correct answer.

## Technical Architecture

* Generative Engine: Powered by the Google Gemini 1.5 Flash API for rapid, high-reasoning natural language processing.
* System Prompt Engineering: Uses complex system-level constraints to prevent the model from providing solutions, even when prompted for the answer by the user.
* State Management: Utilizes streamlit.session_state to maintain persistence in conversational context, allowing the AI to "remember" previous steps in a multi-turn math or coding problem.
* Tiered Hint System: A secondary logic branch generates context-aware nudges. These hints provide a lower level of abstraction than standard Socratic questions but still stop short of the final solution.

## Key Features

* Zero-Answer Constraint: The core logic prevents the AI from providing direct solutions, encouraging user engagement with the material.
* Subject-Specific Logic: Dynamically adjusts the AI's pedagogical voice based on the academic discipline (e.g., Mathematics, Computer Science, or Humanities).
* On-Demand Hint Engine: A dedicated utility for providing strategic clues when a student reaches a cognitive roadblock.
* Professional Interface: A clean, distraction-free environment optimized for academic concentration and long-form study sessions.

## Tech Stack

* Language: Python 3.10+
* Web Framework: Streamlit
* AI Integration: Google Generative AI (Gemini)
* Environment: Streamlit Community Cloud

---

Launch the App Live: [codextutor-aitutor.streamlit.app]
