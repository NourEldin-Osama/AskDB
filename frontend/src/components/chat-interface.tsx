"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Send, Loader2, Copy as CopyIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"
import { BackendAPI } from "@/lib/api"

interface Message {
    id: string
    content: string
    role: "user" | "assistant"
    timestamp: number
}

interface ChatInterfaceProps {
    threadId?: string
    token: string
    updateThreadTitle: (threadId: string, title: string) => void
    onNewThread?: (threadId: string) => void
    reset?: boolean
    onResetHandled?: () => void
}

export default function ChatInterface({ threadId, token, updateThreadTitle, onNewThread, reset, onResetHandled }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null)
    const inputRef = useRef<HTMLTextAreaElement>(null)
    const prevThreadIdRef = useRef<string | undefined>(undefined);

    // Reset messages and input when reset flag is set
    useEffect(() => {
        if (reset) {
            setMessages([]);
            setInput("");
            if (onResetHandled) onResetHandled();
            prevThreadIdRef.current = undefined;
        }
    }, [reset, onResetHandled]); // Added onResetHandled dependency

    // Load messages for the current thread from backend AND handle clearing
    useEffect(() => {
        if (threadId) {
            // Only fetch if switching to a different thread (not just after creating/sending first message)
            if (
                messages.length === 0 ||
                (prevThreadIdRef.current && prevThreadIdRef.current !== threadId)
            ) {
                BackendAPI.fetchChatHistory(token, threadId)
                    .then((data) => {
                        const mapped = (data.messages || []).map((msg: any, idx: number) => ({
                            id: `${threadId}-${idx}`,
                            content: msg.content,
                            role: msg.role === "ai" ? "assistant" : "user",
                            timestamp: Date.now() + idx, // Not accurate, but required for UI
                        }));
                        setMessages(mapped);
                    })
                    .catch(() => setMessages([])); // Clear on error
            }
            prevThreadIdRef.current = threadId;
        } else {
            if (messages.length > 0) {
                setMessages([]);
                setInput(""); // Also clear input here
            }
            prevThreadIdRef.current = undefined;
        }
        // Only re-run if threadId or token changes.
    }, [threadId, token]);


    // Scroll to bottom when messages change
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages])

    // Focus input on mount
    useEffect(() => {
        inputRef.current?.focus()
    }, [])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!input.trim()) return

        const userMessage: Message = {
            id: Date.now().toString(),
            content: input.trim(),
            role: "user",
            timestamp: Date.now(),
        }

        setMessages((prev) => [...prev, userMessage])
        setInput("")
        setIsLoading(true)

        try {
            let data
            let newThreadId = threadId
            if (!threadId) {
                data = await BackendAPI.chatbotMessage(token, userMessage.content)
                if (typeof data.thread_id === "string" && data.thread_id) {
                    newThreadId = data.thread_id
                    if (onNewThread && newThreadId) onNewThread(newThreadId)
                    // Update thread title only when creating a new thread
                    if (typeof newThreadId === "string") {
                        const threadTitle = userMessage.content.length > 30
                            ? userMessage.content.substring(0, 30) + "..."
                            : userMessage.content
                        updateThreadTitle(newThreadId, threadTitle)
                    }
                }
            } else {
                data = await BackendAPI.chatbotMessage(token, userMessage.content, threadId)
            }

            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                content: data.response,
                role: "assistant",
                timestamp: Date.now(),
            }

            setMessages((prev) => [...prev, botMessage])
        } catch (error) {
            toast.error("Failed to get a response. Please try again.")
            console.error("Error:", error)
        } finally {
            setIsLoading(false)
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }

    return (
        <div className="flex flex-col h-full bg-gradient-to-br from-background via-background/80 to-user/5">
            {/* Title Area */}
            <div className="text-center py-4"> {/* Removed border classes */}
                <h1 className="text-xl font-semibold welcome-heading">AskDB</h1> {/* Added welcome-heading class */}
            </div>
            {/* Chat messages area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                    <div className="flex items-center justify-center h-full">
                        <div className="glass-effect text-center p-8 rounded-lg">
                            <h2 className="welcome-heading text-2xl mb-2">
                                Start a conversation
                            </h2>
                            <p className="text-foreground/60">Send a message to begin chatting with the assistant</p>
                        </div>
                    </div>
                ) : (
                    messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'
                                }`}
                        >
                            <div
                                className={`${message.role === 'user'
                                    ? 'message-bubble-user'
                                    : 'message-bubble-bot'
                                    } px-4 py-2 rounded-lg max-w-[80%] relative`}
                            >
                                <div
                                    className="text-user-foreground prose dark:prose-invert max-w-none"
                                    dangerouslySetInnerHTML={{ __html: message.content }}
                                />
                                {message.role === "assistant" && (
                                    <div className="flex justify-end">
                                        <button
                                            type="button"
                                            className="mt-1 bg-white/80 hover:bg-white text-xs text-gray-700 px-2 py-1 rounded shadow transition flex items-center gap-1"
                                            onClick={() => {
                                                navigator.clipboard.writeText(
                                                    // Strip HTML tags for clean copy
                                                    message.content.replace(/<[^>]+>/g, "")
                                                );
                                                toast.success("Copied!");
                                            }}
                                            aria-label="Copy to clipboard"
                                        >
                                            <CopyIcon className="w-4 h-4" />
                                            Copy
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                )}
                {isLoading && (
                    <div className="flex items-start">
                        <div className="glass-effect rounded-lg p-3">
                            <div className="flex items-center space-x-2">
                                <Loader2 className="h-4 w-4 animate-spin text-bot" />
                                <span className="text-foreground/80">Thinking...</span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div className="border-t border-blue-200 dark:border-[hsl(var(--surface-border))] bg-surface/80 dark:bg-[hsl(var(--surface)/0.8)] backdrop-blur-sm p-4">
                <form onSubmit={handleSubmit} className="flex space-x-2">
                    <Textarea
                        ref={inputRef}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Type your message..."
                        className="input-background flex-1 min-h-[40px] max-h-[100px] resize-none focus-visible:ring-[hsl(var(--user)/0.15)] w-full overflow-y-auto border border-blue-200 dark:border-[hsl(var(--surface-border))] placeholder-gray-500 bg-[hsl(var(--surface))] text-[hsl(var(--foreground))]"
                        style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}
                        disabled={isLoading}
                    />
                    <Button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="self-end"
                        size="lg" // Updated to use the larger size variant
                    >
                        {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-6 w-6 text-white" />}
                        <span className="sr-only">Send message</span>
                    </Button>
                </form>
            </div>
        </div>
    )
}
