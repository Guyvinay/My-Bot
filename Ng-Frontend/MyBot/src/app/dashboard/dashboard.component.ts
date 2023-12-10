import { Component, OnInit } from '@angular/core';
import { GptService } from '../services/gpt.service';
import { Chat, CreateChat } from '../modals/chat';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  user_email: string = 'vinay@gmail.com'
  user_gpt_chats: Chat[] = [];

  created_chat: Chat = {
    chat_id: 0,
    title: '',
    description: ''
  };

  chat_to_be_created: CreateChat = {
    title: '',
    description: 'Chat Description'
  }

  constructor(
    private gpt_service: GptService,
    private routetr: Router
  ) { }

  ngOnInit(): void {
    this.gpt_service.get_all_chats(this.user_email)
      .subscribe(
        (response) => {
          this.user_gpt_chats = response.chats;
          this.user_gpt_chats.reverse();
          console.log(this.user_gpt_chats);
        },
        (error) => {
          console.log(error);
        }
      );
  }

  creatGptChat(): void {
    this.gpt_service.create_gpt_chat(this.user_email, this.chat_to_be_created)
      .subscribe(
        (response) => {
          this.created_chat = response;
          // console.log(this.created_chat);
          this.user_gpt_chats.unshift(this.created_chat);
          // console.log(this.user_gpt_chats);
          window.location.reload();
        },
        (error) => {
          console.log(error);
        }
      );
  }

  delete_chat(chat_id: number): void {
    this.gpt_service.delete_gpt_chat(this.user_email, chat_id)
      .subscribe(
        (response) => {
          // console.log(response);
          let ind = this.user_gpt_chats.findIndex((ch) => ch.chat_id == chat_id);
          if (ind != -1) {
            this.user_gpt_chats.splice(ind, 1);
          }
          // console.log(ind);
        },
        (error) => {
          console.log(error);
        }
      )
  }

  chat_inits(chat: Chat): void {
    this.gpt_service.set_current_chat(chat);
  }
}
