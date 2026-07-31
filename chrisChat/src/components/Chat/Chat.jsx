import { useState } from "react";

import "./Chat.css";
import Slider from "../Slider/Slider";
function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [tone, setTone] = useState(50)
    const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:3000/";
    const handleValue = (value) => {
        setTone(value);
    }
    const handleChat = async () => {
        if (!input.trim()) return;

        const userMessage = { role: "user", content: input };
        const updatedMessages = [...messages, userMessage];
        setMessages(updatedMessages);
        setInput("");

        try {
            const response = await fetch(API_URL + "api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    messages: updatedMessages,
                    tone: tone,
                }),
            });
            const data = await response.json();
            setMessages([...updatedMessages, { role: "assistant", content: data.response || data.error }]);
        } catch (error) {
            setMessages([...updatedMessages, { role: "assistant", content: "Error connecting to server." }]);
        }
    }
    return (
        <>

            <div className="chat-box">
                <h1>Chat with me</h1>
                <textarea placeholder="Chat with me" value={input} onChange={(e) => setInput(e.target.value)}></textarea>
                <button onClick={handleChat}>Send</button>
            </div>
            <div className="response-box">
                {messages.map((msg, idx) => (
                    <div key={idx}>
                        <strong>{msg.role === "user" ? "You: " : "Chris: "}</strong>
                        <span>{msg.content}</span>
                    </div>
                ))}
                <Slider handleValue={handleValue} />
            </div>


        </>
    )
}

export default Chat
