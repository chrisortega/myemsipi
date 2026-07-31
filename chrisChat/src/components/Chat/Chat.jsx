import { useState } from "react";
import useFetcher from "../../hooks/useFetcher";
import "./Chat.css";
function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const API_URL = import.meta.env.VITE_API_URL;
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
                        <strong>{msg.role === "user" ? "You: " : "AI: "}</strong>
                        <span>{msg.content}</span>
                    </div>
                ))}
            </div>
        </>
    )
}

export default Chat
