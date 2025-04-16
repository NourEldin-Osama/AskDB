import { Loader2 } from "lucide-react"

export default function Loading() {
    return (
        <div className="flex flex-col items-center justify-center h-screen w-screen bg-[hsl(var(--background))] animate-fade-in">
            <div className="relative flex items-center justify-center mb-4">
                <span className="absolute inline-flex h-16 w-16 rounded-full bg-blue-100 dark:bg-[hsl(var(--user)/0.15)] animate-ping" />
                <Loader2 className="h-12 w-12 text-teal-500 dark:text-[hsl(var(--user))] animate-spin z-10" />
            </div>
            <h2 className="text-xl font-semibold text-gray-800 dark:text-[hsl(var(--foreground))] tracking-wide drop-shadow">Loading ...</h2>
        </div>
    )
}
