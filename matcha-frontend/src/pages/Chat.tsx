import { useCallback, useEffect, useRef, useState } from "react"
import { useNavigate, useParams, Link } from "react-router-dom"
import Topbar from "../components/Topbar"
import StatusMessage from "../components/StatusMessage"
import { useAuth } from "../context/AuthContext"
import { fetchConversations, fetchMessages, sendMessage } from "../services/chat"
import type { Conversation, Message } from "../types/chat"
import "./Chat.css"

/* Chat temps réel entre users connectés (match) : liste des conversations + fil de messages */
export default function Chat() {
    const { id } = useParams()
    const openId = id ? Number(id) : null
    const navigate = useNavigate()
    const { isAuthenticated, user, incomingMessage, refreshUnreadMessages } = useAuth()

    const [conversations, setConversations] = useState<Conversation[]>([])
    const [messages, setMessages] = useState<Message[]>([])
    const [draft, setDraft] = useState("")
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(true)
    const threadEndRef = useRef<HTMLDivElement>(null)

    const loadConversations = useCallback(async () => {
        try {
            setConversations(await fetchConversations())
        } catch (e) {
            setError(e instanceof Error ? e.message : "Erreur serveur")
        } finally {
            setLoading(false)
        }
    }, [])

    const openConversation = useCallback(async (userId: number) => {
        try {
            // le GET marque les messages reçus comme lus côté backend
            setMessages(await fetchMessages(userId))
            refreshUnreadMessages()
            setConversations(prev => prev.map(conv =>
                conv.user_id === userId ? { ...conv, unread_count: 0 } : conv
            ))
        } catch (e) {
            setError(e instanceof Error ? e.message : "Erreur serveur")
        }
    }, [refreshUnreadMessages])

    // 1 chargement initial de la liste des matchs
    useEffect(() => {
        if (!isAuthenticated) return
        loadConversations()
    }, [isAuthenticated, loadConversations])

    // 2 ouverture d'une conversation via l'URL /chat/:id
    useEffect(() => {
        if (!isAuthenticated || openId === null) return
        openConversation(openId)
    }, [isAuthenticated, openId, openConversation])

    // 3 message reçu en temps réel via le socket
    useEffect(() => {
        if (!incomingMessage) return
        if (openId !== null && incomingMessage.sender_id === openId) {
            setMessages(prev => [...prev, incomingMessage])
            openConversation(openId) // marque comme lu + resynchronise
        } else {
            loadConversations() // met à jour aperçus + compteurs
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [incomingMessage])

    // 4 scroll en bas du fil à chaque nouveau message
    useEffect(() => {
        threadEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages])

    if (!isAuthenticated) {
        return <div className="app-container"> <Topbar></Topbar><h1>Veuillez vous connecter</h1></div>
    }

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault()
        if (openId === null || !draft.trim()) return
        try {
            const sent = await sendMessage(openId, draft)
            setMessages(prev => [...prev, sent])
            setDraft("")
            loadConversations()
        } catch (e) {
            setError(e instanceof Error ? e.message : "Erreur serveur")
        }
    }

    const openConv = conversations.find(conv => conv.user_id === openId)

    return (
        <div className="app-container page-scroll">
        <Topbar />
        <div className="chat-page">
            {error && <StatusMessage type="error" message={error} onClose={() => setError(null)} />}

            <div className={`chat-layout ${openId !== null ? "chat-layout--open" : ""}`}>
                <ConversationList
                    conversations={conversations}
                    loading={loading}
                    activeId={openId}
                    onSelect={(userId) => navigate(`/chat/${userId}`)}
                />
                <ConversationThread
                    conversation={openConv ?? null}
                    messages={messages}
                    myUserId={user?.id ?? 0}
                    draft={draft}
                    onDraftChange={setDraft}
                    onSend={handleSend}
                    onBack={() => navigate("/chat")}
                    threadEndRef={threadEndRef}
                />
            </div>
        </div>
        </div>
    )
}

interface ConversationListProps {
    conversations: Conversation[]
    loading: boolean
    activeId: number | null
    onSelect: (userId: number) => void
}

/* Colonne de gauche : un item par match, aperçu du dernier message + non-lus */
function ConversationList({ conversations, loading, activeId, onSelect }: ConversationListProps) {
    return (
        <aside className="chat-list">
            <h2 className="chat-list-title">Messages</h2>
            {loading && <p className="chat-hint">Chargement...</p>}
            {!loading && conversations.length === 0 && (
                <p className="chat-hint">Pas encore de match. Va liker des profils !</p>
            )}
            {conversations.map(conv => (
                <button
                    key={conv.user_id}
                    className={`chat-item ${conv.user_id === activeId ? "chat-item--active" : ""}`}
                    onClick={() => onSelect(conv.user_id)}
                >
                    {conv.profile_photo_url ? (
                        <img className="chat-item-photo" src={conv.profile_photo_url} alt="" />
                    ) : (
                        <div className="chat-item-photo chat-item-photo--empty">👤</div>
                    )}
                    <div className="chat-item-body">
                        <span className="chat-item-name">
                            {conv.first_name ?? conv.username}
                            {conv.is_online && <span className="chat-online-dot" title="En ligne" />}
                        </span>
                        <span className="chat-item-preview">
                            {conv.last_message ?? "Nouveau match — dites bonjour !"}
                        </span>
                    </div>
                    {conv.unread_count > 0 && (
                        <span className="chat-item-unread">{conv.unread_count}</span>
                    )}
                </button>
            ))}
        </aside>
    )
}

interface ConversationThreadProps {
    conversation: Conversation | null
    messages: Message[]
    myUserId: number
    draft: string
    onDraftChange: (value: string) => void
    onSend: (e: React.FormEvent) => void
    onBack: () => void
    threadEndRef: React.RefObject<HTMLDivElement | null>
}

/* Colonne de droite : fil de messages + zone de saisie */
function ConversationThread({
    conversation, messages, myUserId, draft, onDraftChange, onSend, onBack, threadEndRef,
}: ConversationThreadProps) {
    if (!conversation) {
        return (
            <section className="chat-thread chat-thread--empty">
                <p className="chat-hint">Sélectionne une conversation</p>
            </section>
        )
    }

    return (
        <section className="chat-thread">
            <header className="chat-thread-header">
                <button className="chat-back" onClick={onBack} aria-label="Retour">←</button>
                {conversation.profile_photo_url ? (
                    <img className="chat-item-photo" src={conversation.profile_photo_url} alt="" />
                ) : (
                    <div className="chat-item-photo chat-item-photo--empty">👤</div>
                )}
                <div className="chat-thread-title">
                    <span className="chat-item-name">
                        {conversation.first_name ?? conversation.username}
                        {conversation.is_online && <span className="chat-online-dot" title="En ligne" />}
                    </span>
                    <ThreadStatus conversation={conversation} />
                </div>
                <Link className="chat-profile-link" to={`/user/${conversation.user_id}`}>Voir profil</Link>
            </header>

            <div className="chat-messages">
                {messages.length === 0 && (
                    <p className="chat-hint">Aucun message. Lance la conversation !</p>
                )}
                {messages.map(message => (
                    <MessageBubble key={message.id} message={message} mine={message.sender_id === myUserId} />
                ))}
                <div ref={threadEndRef} />
            </div>

            <form className="chat-input-row" onSubmit={onSend}>
                <input
                    className="chat-input"
                    type="text"
                    placeholder="Écris ton message..."
                    value={draft}
                    maxLength={1000}
                    onChange={(e) => onDraftChange(e.target.value)}
                />
                <button className="chat-send" type="submit" disabled={!draft.trim()}>Envoyer</button>
            </form>
        </section>
    )
}

/* En ligne, ou dernière connexion du match */
function ThreadStatus({ conversation }: { conversation: Conversation }) {
    if (conversation.is_online) {
        return <span className="chat-thread-status chat-thread-status--online">En ligne</span>
    }
    if (!conversation.last_online) {
        return null
    }
    const lastSeen = new Date(conversation.last_online).toLocaleString("fr-FR", {
        day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
    })
    return <span className="chat-thread-status">Vu le {lastSeen}</span>
}

/* Bulle de message, alignée selon l'expéditeur */
function MessageBubble({ message, mine }: { message: Message; mine: boolean }) {
    const time = new Date(message.created_at).toLocaleTimeString("fr-FR", {
        hour: "2-digit", minute: "2-digit",
    })
    return (
        <div className={`chat-bubble-row ${mine ? "chat-bubble-row--mine" : ""}`}>
            <div className={`chat-bubble ${mine ? "chat-bubble--mine" : ""}`}>
                <p className="chat-bubble-text">{message.content}</p>
                <span className="chat-bubble-time">{time}</span>
            </div>
        </div>
    )
}
