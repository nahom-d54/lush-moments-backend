"use client";

import type React from "react";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { MessageCircle, X, Send, Minimize2, User } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useToast } from "@/hooks/use-toast";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  id: string;
  text: string;
  sender: "user" | "bot" | "system";
  timestamp: Date;
  is_agent?: boolean;
}

export function AnonymousChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [sessionId, setSessionId] = useState<string>("");
  const [isConnected, setIsConnected] = useState(false);
  const [isTransferred, setIsTransferred] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const { toast } = useToast();

  // Generate or retrieve session ID
  useEffect(() => {
    let storedSessionId = localStorage.getItem("lush-moments-chat-session");
    if (!storedSessionId) {
      storedSessionId = `session-${Date.now()}-${Math.random()
        .toString(36)
        .substr(2, 9)}`;
      localStorage.setItem("lush-moments-chat-session", storedSessionId);
    }
    setSessionId(storedSessionId);
  }, []);

  // WebSocket connection
  useEffect(() => {
    if (!sessionId || !isOpen) return;

    const wsUrl = `ws://localhost:8000/ws/chat/${sessionId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log("WebSocket connected");
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Received:", data);

        const newMessage: Message = {
          id: `msg-${Date.now()}-${Math.random()}`,
          text: data.message,
          sender:
            data.type === "user"
              ? "user"
              : data.type === "system"
              ? "system"
              : "bot",
          timestamp: new Date(data.timestamp),
          is_agent: data.is_agent,
        };

        setMessages((prev) => [...prev, newMessage]);

        // Hide typing indicator when bot responds
        if (data.type === "bot" || data.type === "system") {
          setIsTyping(false);
        }

        // Check if transferred to human
        if (data.transferred) {
          setIsTransferred(true);
        }
      } catch (error) {
        console.error("Error parsing message:", error);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      toast({
        title: "Connection Error",
        description: "Failed to connect to chat. Please try again.",
        variant: "destructive",
      });
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
      setIsConnected(false);
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [sessionId, isOpen, toast]);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !isConnected) return;

    const message = {
      type: "message",
      message: inputValue,
    };

    wsRef.current?.send(JSON.stringify(message));
    setInputValue("");
    setIsTyping(true); // Show typing indicator
  };

  const handleRequestHuman = () => {
    if (!isConnected) return;

    const message = {
      type: "request_human",
      message: "User requested human assistance",
    };

    wsRef.current?.send(JSON.stringify(message));

    toast({
      title: "Transferring to Human Agent",
      description: "One of our team members will assist you shortly.",
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

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
            className="fixed bottom-4 right-4 z-50 w-[90vw] sm:w-[380px]"
            style={{ maxHeight: "calc(100vh - 2rem)" }}
          >
            <Card
              className="shadow-2xl border-2 flex flex-col"
              style={{
                height: isMinimized ? "auto" : "min(600px, calc(100vh - 2rem))",
              }}
            >
              <CardHeader className="flex flex-row items-center justify-between p-4 bg-primary text-primary-foreground rounded-t-lg shrink-0">
                <div className="flex items-center gap-2">
                  <MessageCircle className="h-5 w-5" />
                  <div>
                    <h3 className="font-semibold">Chat with Us</h3>
                    <p className="text-xs opacity-90">
                      {isTransferred ? "Human agent" : "AI assistant"}
                      {" • "}
                      {isConnected ? "Connected" : "Connecting..."}
                    </p>
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
                <CardContent className="p-0 flex-1 flex flex-col min-h-0">
                  {/* Messages */}
                  <div className="flex-1 overflow-y-auto p-4" ref={scrollRef}>
                    <div className="space-y-4">
                      {messages.map((message) => (
                        <div
                          key={message.id}
                          className={`flex ${
                            message.sender === "user"
                              ? "justify-end"
                              : "justify-start"
                          }`}
                        >
                          <div
                            className={`max-w-[80%] rounded-lg px-4 py-2 ${
                              message.sender === "user"
                                ? "bg-primary text-primary-foreground"
                                : message.sender === "system"
                                ? "bg-blue-100 text-blue-900 border border-blue-300"
                                : "bg-muted text-muted-foreground"
                            }`}
                          >
                            {message.sender === "bot" ||
                            message.sender === "system" ? (
                              <div className="text-sm leading-relaxed prose prose-sm dark:prose-invert max-w-none prose-p:my-2 prose-headings:my-2 prose-ul:my-2 prose-ol:my-2 prose-li:my-1">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                  {message.text}
                                </ReactMarkdown>
                              </div>
                            ) : (
                              <p className="text-sm leading-relaxed whitespace-pre-wrap">
                                {message.text}
                              </p>
                            )}
                            <p
                              className={`text-xs mt-1 ${
                                message.sender === "user"
                                  ? "text-primary-foreground/70"
                                  : "text-muted-foreground/70"
                              }`}
                            >
                              {message.timestamp.toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                              {message.is_agent && " • AI"}
                            </p>
                          </div>
                        </div>
                      ))}

                      {/* Typing Indicator */}
                      {isTyping && (
                        <div className="flex justify-start">
                          <div className="max-w-[80%] rounded-lg px-4 py-3 bg-muted text-muted-foreground">
                            <div className="flex items-center gap-1">
                              <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                              <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                              <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce"></div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  {!isTransferred && isConnected && (
                    <div className="px-4 py-2 border-t border-border bg-muted/30">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleRequestHuman}
                        className="w-full text-xs"
                      >
                        <User className="h-3 w-3 mr-1" />
                        Talk to a Human Agent
                      </Button>
                    </div>
                  )}

                  {/* Input */}
                  <div className="p-4 border-t border-border shrink-0 bg-background">
                    <div className="flex gap-2">
                      <Input
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder={
                          isConnected ? "Type your message..." : "Connecting..."
                        }
                        className="flex-1"
                        disabled={!isConnected}
                      />
                      <Button
                        onClick={handleSendMessage}
                        size="icon"
                        className="bg-primary text-primary-foreground hover:bg-primary/90"
                        disabled={!inputValue.trim() || !isConnected}
                      >
                        <Send className="h-4 w-4" />
                      </Button>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">
                      Session: {sessionId.slice(0, 16)}...
                    </p>
                  </div>
                </CardContent>
              )}
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
