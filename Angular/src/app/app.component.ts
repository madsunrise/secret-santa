import {Component} from '@angular/core';
import {NetworkService} from "./UserService";


@Component({
    selector: 'secret-santa',
    template: `
        <header>
            <h1> Тайный Санта 2018</h1>
        </header>

        <body>
        <div style="width: 400px; margin-left: 100px;">
            <div class="form-group">
                <label for="name">Твоя имя</label>
                <input type="text" class="form-control" id="name" placeholder="Представишься?" [(ngModel)]="name">
            </div>

            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" id="email" placeholder="Только без ошибок!"
                       [(ngModel)]="email">
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else. It's a
                    lie.
                </small>
            </div>

            <div class="form-group">
                <label for="wish">Пожелание</label>
                <input type="text" class="form-control" id="wish" [(ngModel)]="wish" placeholder="Ну давай, жги">
            </div>

            <div class="form-group">
                <label for="room">Идентификатор комнаты</label>
                <input type="text" class="form-control" id="room" placeholder="Не ошибись!" [(ngModel)]="room">
            </div>


            <div class="col-md-8">
                <button class="btn btn-default" (click)="submit(name, email, wish, room)">Погнали!</button>
            </div>
        </div>
        </body>`,
    providers: [NetworkService]
})
export class AppComponent {
    constructor(private userService: NetworkService) {
    }


    submit(name: string, email: string, wish: string, room: string): void {

        if (name == null || email == null || wish == null || room == null) {
            alert("Заполни все поля, братюнь!");
            return;
        }

        let roomInt = Number.parseInt(room);
        roomInt = roomInt - 4264;

        let body = {name: name, email: email, wish: wish};

        this.userService.registerNewUser(body).subscribe(
            data => {
                this.userService.addUserToSession(roomInt, data.id).subscribe(
                    data => alert("Хей, жди письмо с подтверждением!")
                )
            }
        );
    }
}