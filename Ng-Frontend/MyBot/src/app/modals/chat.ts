export interface Chat {
    chat_id:number;
    title:string;
    description:string;
}
export interface CreateChat {
    title:string;
    description:string;
}
export interface Prompt {
    prompt:string;
}
export interface GPTConversation {
    conversation_id:number;
    prompt:string;
    response:string;
}
export interface Conversation {
    User:string;
    Chatbot:string;
}