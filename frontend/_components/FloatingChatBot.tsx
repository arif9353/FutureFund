import { GoogleGenerativeAI } from "@google/generative-ai";
import { useState, useRef, useEffect } from "react";
import { auth } from "@/firebase/firebase_store";
import Top_Nav from "@/_components/Top_Nav";
import { useRouter } from "next/router";
import toast from "react-hot-toast";
import { RiSendPlaneFill, RiChat3Fill } from "react-icons/ri";
import { IoMdClose } from "react-icons/io";
import { useRecoilState } from "recoil";
import { chatsRecoilState } from "@/_recoil/cosmic";

const genAI = new GoogleGenerativeAI("AIzaSyAsi474NfYaPT1nBU24huFKWQtghZ0R74c");

async function runPrompt(valueOfPrompt: string, previousChats: string[]) {
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    let prompt =
        `(Pretend you are a chatbot by FutureFund - AI Based Investment Allocation Engine , you can talk only talk about Investments, Stocks, Retirement Planning, Mutual Funds, things like these , don't mention your name until asked, try to talk about indian financial stuffs more, give short chat response), and give response to the text : '${valueOfPrompt}' , and don't answer for any questions which are not related to finance or investments, etc. tell them strictly that you are a not trained for these questions. 
    These are the context, please condsider them wisely while responding\n` +
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

    const [chats, setChats] = useRecoilState<any>(chatsRecoilState);


    useEffect(() => {
        if (chats?.length === 0) {
            setChats([
                {
                    content: `Hello, I am FutureFund AI, how may I assist you today ?`,
                    role: "assistant",
                },
            ]);
        }
    }, [auth?.currentUser?.displayName]);

    const theme = "dark";
    const [redirected, setRedirected] = useState<boolean>(false);
    const [message, setMessage] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const chatContainerRef = useRef<any>(null);
    const [discDisplayed, setDiscDisplayed] = useState(false);

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
                msgs.filter((x) => x.role === "user").map((chat: any) => chat.content)
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
            chatContainerRef.current.scrollTop =
                chatContainerRef.current.scrollHeight;
        }
    }, [chats]);

    useEffect(() => {
        if (location === "/login" || location === "/register" || location === "/chat") {
            setIsOpen(false)
        }
    }, [location])

    if (location === "/login" || location === "/register" || location === "/chat") {

        return <></>;
    }
    return (
        <>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="fixed bottom-4 right-4 bg-slate-200 text-white p-4 rounded-full shadow-lg hover:bg-slate-100 "
            >
                {isOpen ? <IoMdClose color="black" size={24} /> : <RiChat3Fill size={24} color="black" />}
            </button>
            {isOpen && (
                <div className={` fixed bottom-20 right-4 bg-[#2a2c34] border rounded-lg shadow-lg p-4 w-[400px] max-w-[90vw] z-[9999]`}>
                    <main>
                        <section
                            ref={chatContainerRef}
                            className={`allChatsContainer text-white max-h-[350px] overflow-y-auto`}
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
                        <div className={``}>
                            <form action="" className="flex " onSubmit={(e) => chat(e, message)}>
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
