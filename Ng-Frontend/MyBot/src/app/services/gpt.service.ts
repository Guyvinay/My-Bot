import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Chat, CreateChat, Prompt } from '../modals/chat';

@Injectable({
  providedIn: 'root'
})
export class GptService {

  current_chat:Chat={
    chat_id: 0,
    title: '',
    description: ''
  }

  baseBotUrl = 'http://localhost:5000/chats'

  constructor(
    private http : HttpClient
  ) {}

  max_gpt_requests(user_email:string, chat_id:number,bot_request:Prompt):Observable<any>{

    return this.http.post<any>(
      this.baseBotUrl+`/${user_email}/${chat_id}`,
      bot_request
    )
  }

  get_all_chats(user_email:string):Observable<any> {
    return this.http.get(
      this.baseBotUrl+`/${user_email}`
    )
  }

  create_gpt_chat(user_email:string,chat:CreateChat):Observable<any> {
    return this.http.post<any>(
      this.baseBotUrl+`/${user_email}`, 
      chat
    )
  }

  delete_gpt_chat(user_email:string,chat_id:number):Observable<any> {
    return this.http.delete<any>(
      this.baseBotUrl+`/${user_email}/${chat_id}`
    )
  }

  retriev_gpt_chat_details(user_email:string,chat_id:number):Observable<any> {
    return this.http.get<any>(
      this.baseBotUrl+`/${user_email}/${chat_id}`
    )
  }

  set_current_chat(chat:Chat):void{
    this.current_chat = chat;
  }

  get_current_chat():Chat{
    return this.current_chat;
  }


}
