"use client"

import { useState, useEffect, useCallback } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import ChatInterface from "@/components/chat-interface"
import ThreadSidebar from "@/components/thread-sidebar"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"
import { BackendAPI } from "@/lib/api"
import Loading from "./loading"

export default function Home() {
    const router = useRouter()
    const searchParams = useSearchParams()
    const [isSidebarOpen, setIsSidebarOpen] = useState(false)
    const [threads, setThreads] = useState<{ id: string; title: string }[]>([])
    const [token, setToken] = useState<string | null>(null)
    const [loginEmail, setLoginEmail] = useState("")
    const [loginPassword, setLoginPassword] = useState("")
    const [loginError, setLoginError] = useState<string | null>(null)
    const [isAuthLoading, setIsAuthLoading] = useState(true)
    const [resetChat, setResetChat] = useState(false)
    const [initialLoadComplete, setInitialLoadComplete] = useState(false) // New state
    const currentThreadId = searchParams.get("thread") || ""

    // On mount, load token from localStorage (client only)
    useEffect(() => {
        if (typeof window !== "undefined") {
            setIsAuthLoading(true)
            const storedToken = localStorage.getItem("jwtToken")
            if (storedToken) setToken(storedToken)
            setIsAuthLoading(false)
        }
    }, [])

    // Persist token, fetch threads, handle initial redirect
    useEffect(() => {
        if (token && !isAuthLoading) { // Ensure auth check is done
            localStorage.setItem("jwtToken", token);
            BackendAPI.fetchThreads(token)
                .then((data) => {
                    const fetchedThreads = (data.data || []);
                    setThreads(fetchedThreads);
                    setInitialLoadComplete(true); // Mark initial load as complete
                })
                .catch(() => {
                    setThreads([]);
                    setInitialLoadComplete(true); // Also mark complete on error
                });
        } else if (!token && !isAuthLoading) {
             setInitialLoadComplete(true); // No token, load is complete
        }
    }, [token, isAuthLoading, router, initialLoadComplete]);

    // Login handler
    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoginError(null)
        try {
            const t = await BackendAPI.login(loginEmail, loginPassword)
            setToken(t)
            localStorage.setItem("jwtToken", t)
        } catch (err: any) {
            setLoginError(err.message || "Login failed")
        }
    }

    const createNewThread = () => {
        router.push(`/?`)
        setIsSidebarOpen(false)
        setResetChat(true) // trigger chat reset
    }

    const updateThreadTitle = useCallback(
        async (threadId: string, title: string) => {
            if (!token) return
            try {
                const updated = await BackendAPI.updateThread(token, threadId, title)
                setThreads((prev) =>
                    prev.map((thread) => (thread.id === threadId ? { ...thread, title: updated.title } : thread)),
                )
            } catch { }
        },
        [token],
    )

    const deleteThread = async (threadId: string) => {
        if (!token) return
        try {
            await BackendAPI.deleteThread(token, threadId)
            const updatedThreads = threads.filter((thread) => thread.id !== threadId)
            setThreads(updatedThreads)
            if (currentThreadId === threadId && updatedThreads.length > 0) {
                router.push(`/?thread=${updatedThreads[0].id}`)
            } else if (updatedThreads.length === 0) {
                createNewThread()
            }
        } catch { }
    }

    if (isAuthLoading) {
        return <Loading />
    }

    if (!token) {
        return (
            <main className="flex items-center justify-center h-screen">
                <form onSubmit={handleLogin} className="bg-white p-8 rounded shadow-md w-full max-w-sm">
                    <h2 className="text-xl font-semibold mb-4">Login</h2>
                    <input
                        type="email"
                        placeholder="Email"
                        value={loginEmail}
                        onChange={(e) => setLoginEmail(e.target.value)}
                        className="w-full mb-2 p-2 border rounded"
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={loginPassword}
                        onChange={(e) => setLoginPassword(e.target.value)}
                        className="w-full mb-4 p-2 border rounded"
                        required
                    />
                    {loginError && <div className="text-red-500 mb-2">{loginError}</div>}
                    <Button type="submit" className="w-full">Login</Button>
                </form>
            </main>
        )
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
                updateThreadTitle={updateThreadTitle}
                isOpen={isSidebarOpen}
                setIsOpen={setIsSidebarOpen}
            />

            {/* Main chat area */}
            <div className="flex-1 flex flex-col h-full">
                <ChatInterface
                    threadId={currentThreadId || undefined}
                    token={token!}
                    updateThreadTitle={updateThreadTitle}
                    onNewThread={(newThreadId: string) => {
                        // 1. Update the URL
                        router.push(`/?thread=${newThreadId}`);

                        // 2. Optimistically add the new thread to the UI
                        setThreads((prevThreads) => [
                            { id: newThreadId, title: "New Chat..." },
                            ...prevThreads,
                        ]);
                    }}
                    reset={resetChat}
                    onResetHandled={() => setResetChat(false)}
                />
            </div>
        </main>
    )
}
