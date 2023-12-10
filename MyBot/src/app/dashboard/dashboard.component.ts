import { Component, OnInit } from '@angular/core';
import { GptService } from '../services/gpt.service';
import { Chat, CreateChat } from '../modals/chat';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  user_email : string = 'vinay@gmail.com'

  user_gpt_chats:Chat[] = [];

  created_chat!: Chat;

  chat_to_be_created:CreateChat = {
    title: '',
    description: 'Chat Description'
  }
  
  constructor(
    private gpt_service : GptService 
  ){}

  ngOnInit(): void {
    this.gpt_service.get_all_chats(this.user_email)
                    .subscribe(
                      (response)=>{
                        this.user_gpt_chats = response.chats;
                        console.log(this.user_gpt_chats);
                      },
                      (error)=>{
                        console.log(error);
                      }
                    )
  }

  creatGptChat():void {
    this.gpt_service.create_gpt_chat(this.user_email,this.chat_to_be_created)
                    .subscribe(
                      (response)=>{
                        this.created_chat = response;
                        console.log(this.created_chat)
                        this.user_gpt_chats.push(this.created_chat);
                        console.log(this.user_gpt_chats);
                      },
                      (error)=>{
                        console.log(error);
                      }
                    )
  }
}
