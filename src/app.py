import streamlit as st
from llm_functions import ask_llm, init_open_ai, execute_tools
from utils import SYSTEM_PROMPT, TOOLS, is_far_enough
from streamlit_folium import st_folium
import folium

# Init openAI client
openai_client = init_open_ai()

# Get user input
prompt = st.chat_input("Ask me a location!")

# -----------------------------
# Initialize session state
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "map_coords" not in st.session_state:
    st.session_state.map_coords = []

# -----------------------------
# Trim memory if history is too long
# -----------------------------
if len(st.session_state.chat_history) > 10:
    st.session_state.chat_history = st.session_state.chat_history[-6:]
    summary = ask_llm(openai_client, [*st.session_state.chat_history[:4], {
        "role": "user",
        "content": "Summarize the previous messages as 3 bullet points."
    }]).content
    st.session_state.chat_history = [{"role": "user", "content": summary}] + st.session_state.chat_history[-6:]

# -----------------------------
# SIDEBAR — Map and controls
# -----------------------------
with st.sidebar:
    st.subheader("📍 Location Map")

    if st.session_state.map_coords:
        # Use last point as map center
        center = st.session_state.map_coords[-1]
        map_obj = folium.Map(location=[center["latitude"], center["longitude"]], zoom_start=10)

        # Add markers to map
        for coord in st.session_state.map_coords:
            folium.Marker(
                location=[coord["latitude"], coord["longitude"]],
                popup=coord["name"]
            ).add_to(map_obj)

        # Show map
        st_folium(map_obj, width=600, height=400)

        # Optional: Reset button
        if st.button("🗑️ Clear All Locations"):
            st.session_state.map_coords = []
            st.rerun()
    else:
        st.info("No coordinates yet. Ask for a location.")

# -----------------------------
# MAIN — Chat interface
# -----------------------------

st.subheader("💬 Chat")

# Show past chat messages
for message in st.session_state.chat_history:
    if message["role"] != "function":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# -----------------------------
# Process new prompt
# -----------------------------
if prompt:
    # Add user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Ask the model (includes tool schema)
    response = ask_llm(openai_client, [SYSTEM_PROMPT] + st.session_state.chat_history, tools=TOOLS)

    # -----------------------------
    # If tool was called (e.g. geocode)
    # -----------------------------
    if hasattr(response, "tool_calls") and response.tool_calls:
        tools_responses = execute_tools(response.tool_calls)

        for i, tool in enumerate(response.tool_calls):
            tool_content = str(tools_responses[i]) if tools_responses[i] else "No response"
            message = {
                "role": "function",
                "tool_call_id": tool.id,
                "name": tool.function.name,
                "content": tool_content
            }
            st.session_state.chat_history.append(message)

            # Handle geocoding tool response
            if tool.function.name == "geocode":
                try:
                    location_data = eval(tool_content) if isinstance(tool_content, str) else tool_content
                    lat = float(location_data.get("latitude"))
                    lon = float(location_data.get("longitude"))
                    name = location_data.get("location", "Unknown location")

                    coord = {"latitude": lat, "longitude": lon, "name": name}

                    # Only add if far enough from existing points
                    if is_far_enough(coord, st.session_state.map_coords):
                        st.session_state.map_coords.append(coord)
                except Exception as e:
                    st.warning(f"Error processing coordinates: {e}")

        # Ask model again after tools were executed
        updated_messages = [SYSTEM_PROMPT] + st.session_state.chat_history
        final_response = ask_llm(openai_client, updated_messages, stream=True)

        with st.chat_message("assistant"):
            full_response = st.write_stream(final_response)

        st.session_state["chat_history"].append(
            {"role": "assistant", "content": full_response}
        )
        st.rerun()

    # -----------------------------
    # No tools used, just text response
    # -----------------------------
    else:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response.content
        })
        with st.chat_message("assistant"):
            st.write(response.content)
