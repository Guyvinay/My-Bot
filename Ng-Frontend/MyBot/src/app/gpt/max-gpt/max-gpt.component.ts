import { Component, OnInit } from '@angular/core';
import { Chat, Conversation, GPTConversation, Prompt } from 'src/app/modals/chat';
import { GptService } from 'src/app/services/gpt.service';

@Component({
  selector: 'app-max-gpt',
  templateUrl: './max-gpt.component.html',
  styleUrls: ['./max-gpt.component.css']
})
export class MaxGptComponent implements OnInit {

  user_email : string = 'vinay@gmail.com';
  chat_id : number = 32;
  
  current_chat:Chat = {
    chat_id: 0,
    title: '',
    description: ''
  }

  messages: { sender: string, content: string }[] = [];

  // conversations: Conversation = {
  //   User : '',
  //   Chatbot : ''
  // }

  conversations:Conversation[] = [];


  userInput = '';

  gpt_conversations:GPTConversation[] = [];

  prompt:Prompt = {
    prompt: ''
  }

  constructor(
    private gpt_service : GptService 
  ){}

  

  ngOnInit(): void {

    this.gpt_service.retriev_gpt_chat_details(this.user_email, this.chat_id)
                    .subscribe(
                      (response)=>{
                        this.gpt_conversations = response.conversations;
                        
                        this.gpt_conversations.forEach((conv)=>{
                          this.conversations.push(
                            {
                              User:conv.prompt,
                              Chatbot:conv.response
                            }
                          )
                        });
                        
                       
                        console.log(this.conversations);

                        this.conversations.forEach((conv)=>{
                          // console.log(conv);
                          this.messages.push(
                            {
                              sender:'User',
                              content:conv.User
                            }
                          );
                          this.messages.push(
                            {
                              sender:'Chabot',
                              content:conv.Chatbot
                            }
                          )
                        }
                          )
                          
                      },
                      (error)=>{
                        console.log(error);
                      },
                      ()=>{
                      },
                    );

                    console.log(this.current_chat);
                    this.current_chat =  this.gpt_service.get_current_chat();
                    console.log(this.current_chat);
    
  }
  sendMessage(): void {
    if (this.prompt.prompt.trim() !== '') {
      // Add user message to the chat messages
      this.messages.push({ sender: 'User', content: this.prompt.prompt });
      // this.gpt_conversations.push({ prompt: 'User', content: this.prompt.prompt });
      // Send user message to the backend
      this.gpt_service.max_gpt_requests(this.user_email,this.chat_id,this.prompt).subscribe(
        (chatbotResponse) => {
        // Add chatbot response to the chat messages
        // console.log(chatbotResponse);
        
        this.messages.push({ sender: 'Chatbot', content: chatbotResponse.response });
        // this.messages.push(...chatbotResponse.map((message: any) => ({ sender: 'Chatbot', content: message })));
      },
      (error)=>{
        console.log(error);
      });

      // Clear user input after sending
      this.prompt.prompt = '';
    }
  }



}
