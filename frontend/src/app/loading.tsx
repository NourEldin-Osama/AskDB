import { Loader2 } from "lucide-react"

export default function Loading() {
    return (
        <div className="flex flex-col items-center justify-center h-screen w-screen bg-gradient-to-br from-background via-background/80 to-user/10 animate-fade-in">
            <div className="relative flex items-center justify-center mb-4">
                <span className="absolute inline-flex h-16 w-16 rounded-full bg-user/20 animate-ping" />
                <Loader2 className="h-12 w-12 text-user animate-spin z-10" />
            </div>
            <h2 className="text-xl font-semibold text-user-foreground tracking-wide drop-shadow">Loading ...</h2>
        </div>
    )
}
