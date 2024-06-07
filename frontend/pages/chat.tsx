
import { GoogleGenerativeAI } from "@google/generative-ai";
import { useState, useRef, useEffect } from "react";
import { auth } from "@/firebase/firebase_store";
import Top_Nav from "@/_components/Top_Nav";
import { useRouter } from "next/router";
import toast from "react-hot-toast";
import { set } from "firebase/database";
import { VscSend } from "react-icons/vsc";
import { RiSendPlaneFill } from "react-icons/ri";
import { chatsRecoilState } from "@/_recoil/cosmic";
import { useRecoilState } from "recoil";

const genAI = new GoogleGenerativeAI("AIzaSyAsi474NfYaPT1nBU24huFKWQtghZ0R74c");

async function runPrompt(valueOfPrompt: string, previousChats: string[]) {
    // For text-only input, use the gemini-pro model
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    let prompt =
    `(Pretend you are a chatbot : FutureFund - AI Based Investment Helper , you can talk about Any Stocks, Any Crypto, Gold ETF, Retirement Planning, Mutual Funds, RDs, Any finance related things like these , don't mention your name until asked, try to talk about financial stuffs more, majorly try indian finance, give short chat response), and give response to the text : '${valueOfPrompt}' , and don't answer for any questions which are not related to finance or investments, etc. tell them strictly that you are a not trained for these questions. 
These are the context, please condsider them wisely while responding\n` +
    previousChats.join("\n");

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(text);
    return text;
}

function ChatBot() {

    const [chats, setChats] = useRecoilState<any>(chatsRecoilState);
    useEffect(() => {
        if (chats?.length === 0) {
            setChats([
                {
                    content: `Hello, I am FutureFund AI, how may I assist you today ?`,
                    role: "assistant",
                },
            ]);
        }        // eslint-disable-next-line
    }, [auth?.currentUser?.displayName]);

    const theme = "dark";

    const router = useRouter();
    const [redirected, setRedirected] = useState<boolean>(false);
    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged(async user => {
            if (!user && !redirected) {
                await auth.signOut();
                toast(' ⓘ  Please Login to access.');
                setRedirected(true);
                router.push('/login');
            }
        });

        return () => unsubscribe();
    }, [redirected]);


    const [message, setMessage] = useState("");

    const [isTyping, setIsTyping] = useState(false);
    const chatContainerRef = useRef<any>(null);

    const [discDisplayed, setDiscDisplayed] = useState(false);
    useEffect(() => {
        "use client";
        if (!discDisplayed) {
            setDiscDisplayed(true);
            toast('Please Note:  All the chats are temporary and will not be saved for privacy reasons.', {
                duration: 2000,
                icon: '🔒',
                position: 'bottom-right',
            });
        }
    }, []);

    const chat = async (e: any, message: any) => {
        e.preventDefault();

        if (!message) return;

        setIsTyping(true);

        let msgs = [...chats];
        msgs = [...msgs,{ role: "user", content: message } ];
        setChats(msgs);

        setMessage("");

        try {
            const response = await runPrompt(
                message,
                msgs.filter((x) => x.role === "user").map((chat: any) => chat.content)
            );
            msgs = [...msgs,{ role: "assistant", content: response } ];
            setChats(msgs);
        } catch (error) {
            console.error("Error generating response:", error);
        }

        setIsTyping(false);
    };

    useEffect(() => {
        // Scroll to the bottom of the chat container
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop =
                chatContainerRef.current.scrollHeight;
        }
    }, [chats]);

    return (
        <>
            <Top_Nav />
            <div className={theme + " chatpage"}>
                <main>
                    <section
                        ref={chatContainerRef}
                        className={theme + " allChatsContainer"}
                    >
                        {chats && chats.length
                            ? chats.map((chat: any, index: number) => (
                                <p
                                    key={index}
                                    className={chat.role === "user" ? "user_msg" : ""}
                                ><span style={{ textAlign: "left" }}>{chat.content}</span>
                                </p>
                            ))
                            : ""}
                        {isTyping && (
                            <p>
                                <i>{isTyping ? "Typing" : ""}</i>
                            </p>
                        )}
                    </section>

                    <div className={theme + " inputChat"}>
                        <form action="" onSubmit={(e) => chat(e, message)}>
                            <input
                                type="text"
                                name="message"
                                value={message}
                                placeholder="Type your message here"
                                autoComplete="off"
                                onChange={(e) => setMessage(e.target.value)}
                            />
                            <button type="submit">
                                <RiSendPlaneFill color="#000" size={"20px"} />
                            </button>
                        </form>
                    </div>
                </main>
            </div>
        </>
    );
}

export default ChatBot;