# 🗺️ GeoChat: Conversational Map Assistant with OpenAI Function Calling

GeoChat is a conversational web application powered by **OpenAI's GPT models** that allows users to ask for **locations in natural language** and instantly view them on an **interactive map**. The assistant understands location prompts, fetches geographic coordinates using a custom geocoding tool, and displays them via **Streamlit and Folium**.

The project is made in a way that it is easy to extrapolate to use any other llm.

--- 

![app_demo](https://raw.githubusercontent.com/cberdejo/GeoChat/main/screenshots/example.png)

---

## 🚀 Features

- 💬 **Conversational chat** interface using OpenAI Chat Completions API.
- 🧠 **Function Calling (Tool Use)**: GPT automatically triggers geolocation tool when needed.
- 🌍 **Interactive map** that updates in real time using Streamlit + Folium.

- 🔁 **Automatic context summarization** for long conversations.

---

## 📦 Tech Stack

- **Python 3.11**
- [Streamlit](https://streamlit.io) – UI
- [OpenAI](https://platform.openai.com/docs) – LLM backend
- [Folium](https://python-visualization.github.io/folium/) – Map visualization
- [Geopy](https://geopy.readthedocs.io/) – Distance filtering
- [Nominatim API](https://nominatim.openstreetmap.org/) – Geocoding service

---

## 🧠 How LLM Tool Use Works

The assistant is instructed via a **system prompt** to only respond to location-based queries. If a user asks for a city or town, the assistant uses OpenAI's **function calling mechanism** to:

1. Trigger the `geocode(location)` function.
2. Fetch coordinates from Nominatim (OpenStreetMap).
3. Return latitude/longitude to the model.
4. Let the LLM **continue the conversation** using those coordinates.

This creates an experience where the model **not only performs an action**, but also **explains** and **responds** in natural language with the result.

---

## 🗺️ Sidebar Map Behavior

The left sidebar includes:

- A live-updating **Folium map** centered on the latest location.
- All visited coordinates shown as **interactive markers**.
- A button to **clear all points**.
- Automatic filtering to prevent points that are too close (<2 km).

---

## 📁 Project Structure

```
GeoChat
├─ 📁src
│  ├─ 📄app.py
│  ├─ 📄llm_functions.py
│  ├─ 📄tools.py
│  └─ 📄utils.py
├─ 📄.env-template
├─ 📄.gitignore
├─ 📄.python-version
├─ 📄LICENSE
├─ 📄pyproject.toml
├─ 📄README.md
└─ 📄uv.lock
```

---



## 🔧 Installation & Run

### Create a `.env` file with your OpenAI key:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxx
```

### 🐳 Docker
1. Build the image:

```bash
docker build -t geochat-app .
```

2. Run the container:

```bash
docker run -p 8501:8501  geochat-app
```

### 💻 Local setup (with uv)
1. Install uv

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

2. Run the app

```bash
uv run streamlit run app.py
```




## 📜 License

MIT License – free to use, adapt, and share.

---

