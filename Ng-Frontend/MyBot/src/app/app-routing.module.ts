import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MaxGptComponent } from './gpt/max-gpt/max-gpt.component';

const routes: Routes = [
  {path:'dashboard', component:DashboardComponent},
  {path:'max-gpt/:chat_id', component:MaxGptComponent},
  {path:'', redirectTo:'/dashboard', pathMatch:'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
