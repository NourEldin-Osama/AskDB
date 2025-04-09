"use client"

import { useState, useEffect, useCallback } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { v4 as uuidv4 } from "uuid"
import ChatInterface from "@/components/chat-interface"
import ThreadSidebar from "@/components/thread-sidebar"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"

export default function Home() {
    const router = useRouter()
    const searchParams = useSearchParams()
    const [isSidebarOpen, setIsSidebarOpen] = useState(false)
    const [threads, setThreads] = useState<{ id: string; name: string; lastMessage?: string }[]>([])
    const currentThreadId = searchParams.get("thread") || ""

    // Initialize with a default thread if none exists
    useEffect(() => {
        if (typeof window !== "undefined") {
            const storedThreads = localStorage.getItem("chatThreads")
            let parsedThreads = storedThreads ? JSON.parse(storedThreads) : []

            if (parsedThreads.length === 0) {
                const newThreadId = uuidv4()
                parsedThreads = [{ id: newThreadId, name: "New Conversation" }]
                localStorage.setItem("chatThreads", JSON.stringify(parsedThreads))
                router.push(`/?thread=${newThreadId}`)
            } else if (!currentThreadId) {
                router.push(`/?thread=${parsedThreads[0].id}`)
            }

            setThreads(parsedThreads)
        }
    }, [router, currentThreadId])

    const createNewThread = () => {
        const newThreadId = uuidv4()
        const updatedThreads = [{ id: newThreadId, name: "New Conversation" }, ...threads]
        setThreads(updatedThreads)
        localStorage.setItem("chatThreads", JSON.stringify(updatedThreads))
        router.push(`/?thread=${newThreadId}`)
        setIsSidebarOpen(false)
    }

    const updateThreadName = useCallback((threadId: string, name: string) => {
        setThreads((prevThreads) => {
            const threadExists = prevThreads.some(thread => thread.id === threadId);
            if (!threadExists) return prevThreads; // Avoid updates if thread is deleted

            const needsUpdate = prevThreads.find(thread => thread.id === threadId)?.name !== name;
            if (!needsUpdate) return prevThreads; // Avoid unnecessary updates

            const updated = prevThreads.map((thread) =>
                thread.id === threadId ? { ...thread, name } : thread
            );
            localStorage.setItem("chatThreads", JSON.stringify(updated));
            return updated;
        });
    }, []);

    const updateThreadLastMessage = useCallback((threadId: string, message: string) => {
        setThreads((prevThreads) => {
            const threadExists = prevThreads.some(thread => thread.id === threadId);
            if (!threadExists) return prevThreads; // Avoid updates if thread is deleted

            const needsUpdate = prevThreads.find(thread => thread.id === threadId)?.lastMessage !== message;
            if (!needsUpdate) return prevThreads; // Avoid unnecessary updates

            const updated = prevThreads.map((thread) =>
                thread.id === threadId ? { ...thread, lastMessage: message } : thread
            );
            localStorage.setItem("chatThreads", JSON.stringify(updated));
            return updated;
        });
    }, []);

    const deleteThread = (threadId: string) => {
        const updatedThreads = threads.filter((thread) => thread.id !== threadId)
        setThreads(updatedThreads)
        localStorage.setItem("chatThreads", JSON.stringify(updatedThreads))

        if (currentThreadId === threadId && updatedThreads.length > 0) {
            router.push(`/?thread=${updatedThreads[0].id}`)
        } else if (updatedThreads.length === 0) {
            createNewThread()
        }
    }

    return (
        <main className="flex h-screen overflow-hidden chat-container">
            {/* Mobile sidebar toggle */}
            <div className="fixed top-4 left-4 z-50 md:hidden">
                <Button
                    variant="outline"
                    size="icon"
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    aria-label="Toggle sidebar"
                >
                    <Menu className="h-5 w-5" />
                </Button>
            </div>

            {/* Sidebar for thread management */}
            <ThreadSidebar
                threads={threads}
                currentThreadId={currentThreadId}
                createNewThread={createNewThread}
                deleteThread={deleteThread}
                updateThreadName={updateThreadName}
                isOpen={isSidebarOpen}
                setIsOpen={setIsSidebarOpen}
            />

            {/* Main chat area */}
            <div className="flex-1 flex flex-col h-full">
                {currentThreadId && (
                    <ChatInterface
                        threadId={currentThreadId}
                        updateThreadName={updateThreadName}
                        updateThreadLastMessage={updateThreadLastMessage}
                    />
                )}
            </div>
        </main>
    )
}
