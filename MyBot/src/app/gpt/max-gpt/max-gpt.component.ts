import { Component, OnInit } from '@angular/core';
import { GptService } from 'src/app/services/gpt.service';

@Component({
  selector: 'app-max-gpt',
  templateUrl: './max-gpt.component.html',
  styleUrls: ['./max-gpt.component.css']
})
export class MaxGptComponent implements OnInit {


  user_email : string = 'vinay@gmail.com'

  constructor(
    private gpt_service : GptService 
  ){}

  ngOnInit(): void {
    this.gpt_service.get_all_chats(this.user_email)
                    .subscribe(
                      (response)=>{
                        console.log(response);
                      },
                      (error)=>{
                        console.log(error);
                      }
                    )
  }

}
