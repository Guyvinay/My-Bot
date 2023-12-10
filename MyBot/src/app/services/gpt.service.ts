import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CreateChat } from '../modals/chat';

@Injectable({
  providedIn: 'root'
})
export class GptService {


  baseBotUrl = 'http://localhost:5000/chats'

  constructor(
    private http : HttpClient
  ) {}

  max_gpt_requests(user_email:string, chat_id:number,bot_request:any):Observable<any>{

    return this.http.post<any>(
      this.baseBotUrl+user_email+`/${chat_id}`,
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


}
