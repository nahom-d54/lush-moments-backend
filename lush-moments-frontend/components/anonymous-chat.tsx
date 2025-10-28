"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { MessageCircle, X, Send, Minimize2 } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

interface Message {
  id: string
  text: string
  sender: "user" | "assistant"
  timestamp: Date
}

export function AnonymousChat() {
  const [isOpen, setIsOpen] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")
  const [sessionId, setSessionId] = useState<string>("")
  const scrollRef = useRef<HTMLDivElement>(null)

  // Generate or retrieve session ID
  useEffect(() => {
    let storedSessionId = localStorage.getItem("lush-moments-chat-session")
    if (!storedSessionId) {
      storedSessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
      localStorage.setItem("lush-moments-chat-session", storedSessionId)
    }
    setSessionId(storedSessionId)

    // Load chat history from localStorage
    const storedMessages = localStorage.getItem(`lush-moments-chat-${storedSessionId}`)
    if (storedMessages) {
      try {
        const parsed = JSON.parse(storedMessages)
        setMessages(parsed.map((msg: Message) => ({ ...msg, timestamp: new Date(msg.timestamp) })))
      } catch (e) {
        console.error("Failed to parse stored messages", e)
      }
    } else {
      // Welcome message
      setMessages([
        {
          id: "welcome",
          text: "Hello! Welcome to Lush Moments. How can we help you plan your perfect celebration today?",
          sender: "assistant",
          timestamp: new Date(),
        },
      ])
    }
  }, [])

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (sessionId && messages.length > 0) {
      localStorage.setItem(`lush-moments-chat-${sessionId}`, JSON.stringify(messages))
    }
  }, [messages, sessionId])

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: `msg-${Date.now()}`,
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")

    // Simulate AI response (in production, this would call your backend API)
    setTimeout(() => {
      const responses = [
        "Thank you for your message! We'd love to help you plan your event. What type of celebration are you planning?",
        "That sounds wonderful! Our team specializes in creating beautiful décor for all types of events. Would you like to schedule a consultation?",
        "Great question! We offer three main packages: Essential, Deluxe, and Signature. Each can be customized to fit your needs. Would you like to learn more about any specific package?",
        "We typically recommend booking 4-6 weeks in advance for best availability. What date are you considering for your event?",
        "I'd be happy to help you with that! For detailed pricing and availability, I can connect you with our team. Would you like to book a consultation or get a quote?",
      ]

      const assistantMessage: Message = {
        id: `msg-${Date.now()}-assistant`,
        text: responses[Math.floor(Math.random() * responses.length)],
        sender: "assistant",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    }, 1000)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <>
      {/* Chat Bubble Button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            className="fixed bottom-4 right-4 z-50"
          >
            <Button
              size="lg"
              onClick={() => setIsOpen(true)}
              className="h-14 w-14 rounded-full shadow-lg bg-primary text-primary-foreground hover:bg-primary/90"
            >
              <MessageCircle className="h-6 w-6" />
            </Button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="fixed bottom-4 right-4 z-50 w-[90vw] sm:w-[380px] max-h-[80vh] sm:max-h-[600px]"
          >
            <Card className="shadow-2xl border-2 h-full flex flex-col">
              <CardHeader className="flex flex-row items-center justify-between p-4 bg-primary text-primary-foreground rounded-t-lg flex-shrink-0">
                <div className="flex items-center gap-2">
                  <MessageCircle className="h-5 w-5" />
                  <div>
                    <h3 className="font-semibold">Chat with Us</h3>
                    <p className="text-xs opacity-90">We typically reply instantly</p>
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setIsMinimized(!isMinimized)}
                    className="h-8 w-8 text-primary-foreground hover:bg-primary-foreground/20"
                  >
                    <Minimize2 className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setIsOpen(false)}
                    className="h-8 w-8 text-primary-foreground hover:bg-primary-foreground/20"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>

              {!isMinimized && (
                <CardContent className="p-0 flex-1 flex flex-col overflow-hidden">
                  {/* Messages */}
                  <ScrollArea className="flex-1 p-4 min-h-0" ref={scrollRef}>
                    <div className="space-y-4">
                      {messages.map((message) => (
                        <div
                          key={message.id}
                          className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
                        >
                          <div
                            className={`max-w-[80%] rounded-lg px-4 py-2 ${
                              message.sender === "user"
                                ? "bg-primary text-primary-foreground"
                                : "bg-muted text-muted-foreground"
                            }`}
                          >
                            <p className="text-sm leading-relaxed">{message.text}</p>
                            <p
                              className={`text-xs mt-1 ${message.sender === "user" ? "text-primary-foreground/70" : "text-muted-foreground/70"}`}
                            >
                              {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </ScrollArea>

                  {/* Input */}
                  <div className="p-4 border-t border-border flex-shrink-0">
                    <div className="flex gap-2">
                      <Input
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your message..."
                        className="flex-1"
                      />
                      <Button
                        onClick={handleSendMessage}
                        size="icon"
                        className="bg-primary text-primary-foreground hover:bg-primary/90"
                        disabled={!inputValue.trim()}
                      >
                        <Send className="h-4 w-4" />
                      </Button>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">Session ID: {sessionId.slice(0, 20)}...</p>
                  </div>
                </CardContent>
              )}
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
