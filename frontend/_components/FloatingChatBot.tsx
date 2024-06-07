import { GoogleGenerativeAI } from "@google/generative-ai";
import { useState, useRef, useEffect } from "react";
import { auth } from "@/firebase/firebase_store";
import { useRouter } from "next/router";
import toast from "react-hot-toast";
import { RiSendPlaneFill, RiChat3Fill } from "react-icons/ri";
import { IoMdClose } from "react-icons/io";
import { useRecoilState } from "recoil";
import { chatsRecoilState } from "@/_recoil/cosmic";

const genAI = new GoogleGenerativeAI("AIzaSyAsi474NfYaPT1nBU24huFKWQtghZ0R74c");

async function runPrompt(valueOfPrompt: any, previousChats: any) {
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    let prompt =
        `(Pretend you are a chatbot: FutureFund - AI Based Investment Helper, you can talk about Any Stocks, Any Crypto, Gold ETF, Retirement Planning, Mutual Funds, RDs, Any finance related things like these, don't mention your name until asked, try to talk about financial stuffs more, majorly try Indian finance, give short chat response), and give response to the text: '${valueOfPrompt}', and don't answer for any questions which are not related to finance or investments, etc. tell them strictly that you are not trained for these questions. 
These are the context, please consider them wisely while responding\n` +
        previousChats.join("\n");

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(text);
    return text;
}

export default function FixedChatBot() {
    const [isOpen, setIsOpen] = useState(false);
    const router = useRouter();
    const location = router.pathname;
    const chatbotRef = useRef<any>(null);
    const [chats, setChats] = useRecoilState<any>(chatsRecoilState);

    useEffect(() => {
        if (chats?.length === 0) {
            setChats([
                {
                    content: `Hello, I am FutureFund AI, how may I assist you today?`,
                    role: "assistant",
                },
            ]);
        }
    }, [auth?.currentUser?.displayName]);

    const theme = "dark";
    const [redirected, setRedirected] = useState(false);
    const [message, setMessage] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const chatContainerRef = useRef<any>(null);
    const [discDisplayed, setDiscDisplayed] = useState(false);

    const chat = async (e: any, message: any) => {
        e.preventDefault();
        if (!message) return;
        setIsTyping(true);
        let msgs = [...chats];
        msgs.push({ role: "user", content: message });
        setChats([...msgs]);
        setMessage("");
        try {
            const response = await runPrompt(
                message,
                msgs.filter(x => x.role === "user").map(chat => chat.content)
            );
            msgs.push({ role: "assistant", content: response });
            setChats(msgs);
        } catch (error) {
            console.error("Error generating response:", error);
        }
        setIsTyping(false);
    };

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [chats]);

    useEffect(() => {
        if (location === "/login" || location === "/register" || location === "/chat") {
            setIsOpen(false);
        }
    }, [location]);

    useEffect(() => {
        function handleClickOutside(event: any) {
            if (chatbotRef.current && !chatbotRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        }
        if (isOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        } else {
            document.removeEventListener("mousedown", handleClickOutside);
        }
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isOpen]);

    if (location === "/login" || location === "/register" || location === "/chat" || location === "/") {
        return null;
    }

    return (
        <>
            <button
                onClick={() =>{ if(!isOpen) setIsOpen(true)}}
                className="fixed bottom-4 right-4 bg-slate-200 text-white p-4 rounded-full shadow-lg hover:bg-slate-100"
            >
                {isOpen ? <IoMdClose color="black" size={24} /> : <RiChat3Fill size={24} color="black" />}
            </button>
            {isOpen && (
                <div
                    ref={chatbotRef}
                    className="fixed bottom-20 right-4 bg-[#2a2c34] border rounded-lg shadow-lg p-4 w-[400px] max-w-[90vw] z-[9999]"
                >
                    <main>
                        <section
                            ref={chatContainerRef}
                            className="allChatsContainer text-white max-h-[350px] overflow-y-auto"
                        >
                            {chats && chats.length
                                ? chats.map((chat: any, index: number) => (
                                    <p
                                        key={index}
                                        className={chat.role === "user" ? "user_msg pr-2 text-slate-300 text-right" : "p-2 bg-[#ffffff08] pr-2 rounded-lg"}
                                    ><span style={{ textAlign: "left" }}> {chat.content}</span>
                                    </p>
                                ))
                                : ""}
                            {isTyping && (
                                <p>
                                    <i>{isTyping ? "Typing" : ""}</i>
                                </p>
                            )}
                        </section>
                        <div>
                            <form action="" className="flex" onSubmit={(e) => chat(e, message)}>
                                <input
                                    type="text"
                                    name="message"
                                    value={message}
                                    placeholder="Type your message here"
                                    autoComplete="off"
                                    onChange={(e) => setMessage(e.target.value)}
                                    className="border rounded outline-none bg-transparent text-white border-[#ffffff90] text-xs p-2 w-full"
                                />
                                <button type="submit" className="bg-[#00000000] text-white p-2 rounded ml-2">
                                    <RiSendPlaneFill color="#fff" size={"20px"} />
                                </button>
                            </form>
                        </div>
                    </main>
                </div>
            )}
        </>
    );
}
