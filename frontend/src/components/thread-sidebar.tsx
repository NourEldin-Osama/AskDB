"use client"

import { useState } from "react"
import Link from "next/link"
import { PlusCircle, Trash2, X, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

interface ThreadSidebarProps {
    threads: { id: string; name: string; lastMessage?: string }[]
    currentThreadId: string
    createNewThread: () => void
    deleteThread: (id: string) => void
    updateThreadName: (id: string, name: string) => void
    isOpen: boolean
    setIsOpen: (isOpen: boolean) => void
}

export default function ThreadSidebar({
    threads,
    currentThreadId,
    createNewThread,
    deleteThread,
    updateThreadName,
    isOpen,
    setIsOpen,
}: ThreadSidebarProps) {
    const [editingId, setEditingId] = useState<string | null>(null)
    const [editName, setEditName] = useState("")

    const startEditing = (id: string, currentName: string) => {
        setEditingId(id)
        setEditName(currentName)
    }

    const saveEdit = () => {
        if (editingId && editName.trim()) {
            updateThreadName(editingId, editName.trim())
            setEditingId(null)
        }
    }

    return (
        <>
            {/* Mobile overlay */}
            {isOpen && <div className="fixed inset-0 bg-black/20 z-40 md:hidden" onClick={() => setIsOpen(false)} />}

            {/* Sidebar */}
            <div
                className={cn(
                    "fixed md:relative z-50 w-64 h-full sidebar-gradient text-sidebar-foreground border-r shadow-sm transition-transform duration-300 ease-in-out",
                    isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0",
                )}
            >
                <div className="flex items-center justify-between p-4 border-b">
                    <h2 className="font-semibold text-lg">Conversations</h2>
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => setIsOpen(false)}
                        className="md:hidden"
                        aria-label="Close sidebar"
                    >
                        <X className="h-5 w-5" />
                    </Button>
                </div>

                <div className="p-2">
                    <Button variant="outline" className="w-full justify-start gap-2" onClick={createNewThread}>
                        <PlusCircle className="h-4 w-4" />
                        New Conversation
                    </Button>
                </div>

                <ScrollArea className="h-[calc(100vh-120px)]">
                    <div className="space-y-1 p-2">
                        {threads.map((thread) => (
                            <div key={thread.id} className="group">
                                {editingId === thread.id ? (
                                    <div className="flex items-center p-2 rounded-md border">
                                        <input
                                            type="text"
                                            value={editName}
                                            onChange={(e) => setEditName(e.target.value)}
                                            onBlur={saveEdit}
                                            onKeyDown={(e) => e.key === "Enter" && saveEdit()}
                                            className="flex-1 bg-transparent outline-none"
                                            autoFocus
                                        />
                                    </div>
                                ) : (
                                    <Link
                                        href={`/?thread=${thread.id}`}
                                        onClick={() => setIsOpen(false)}
                                        className={cn(
                                            "flex items-center justify-between p-2 rounded-md hover:bg-sidebar-hover transition-colors",
                                            currentThreadId === thread.id && "bg-sidebar-active",
                                        )}
                                    >
                                        <div className="flex items-center gap-2 overflow-hidden">
                                            <MessageSquare className="h-4 w-4 flex-shrink-0" />
                                            <div className="truncate">
                                                <div className="font-medium truncate">{thread.name}</div>
                                                {thread.lastMessage && (
                                                    <div className="text-xs text-gray-500 truncate">{thread.lastMessage}</div>
                                                )}
                                            </div>
                                        </div>

                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="h-7 w-7"
                                            onClick={(e) => {
                                                e.preventDefault()
                                                e.stopPropagation()
                                                deleteThread(thread.id)
                                            }}
                                            aria-label="Delete thread"
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </Link>
                                )}
                            </div>
                        ))}
                    </div>
                </ScrollArea>
            </div>
        </>
    )
}
