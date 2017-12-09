import {Component} from '@angular/core';
import {NetworkService} from "./UserService";


@Component({
    selector: 'secret-santa',
    template: `
        <body>

        <nav class="navbar navbar-default">
            <div class="container-fluid">
                <div class="navbar-header">
                    <a class="navbar-brand" href="#">
                        <img alt="Brand" src="https://www.ialottery.com/images/Promotions/SecretSanta/SecretSantaLogo_300px.png">
                    </a>
                </div>
            </div>
        </nav>

        <div style="width: 350px; margin-left: 50px;">
            <div class="form-group">
                <label for="name">Имя</label>
                <input type="text" class="form-control" id="name" [(ngModel)]="name">
            </div>

            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" id="email"
                       [(ngModel)]="email">
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else. It's a
                    lie.
                </small>
            </div>

            <div class="form-group">
                <label for="wish">Пожелание</label>
                <textarea class="form-control" id="wish" [(ngModel)]="wish" placeholder="Ну давай, жги"></textarea>
            </div>

            <div class="form-group">
                <label for="room">Идентификатор комнаты</label>
                <input type="text" class="form-control" id="room" [(ngModel)]="room">
            </div>


            <div class="form-group">
                <button class="btn btn-default" [disabled]="buttonDisabled" (click)="submit(name, email, wish, room)">
                    Готово!
                </button>
            </div>


            <div style="margin-top: 50px; margin-bottom: 15px;">Разыграть нужную комнату можно ниже</div>

            <div class="form-group">
                <label for="session_id">Идентификатор комнаты</label>
                <input type="text" class="form-control" id="session_id" [(ngModel)]="session_id">
            </div>

            <div class="form-group">
                <button class="btn btn-default" [disabled]="playButtonDisabled" (click)="play(session_id)">
                    Понеслась!
                </button>
            </div>
        </div>
        </body>`,
    providers: [NetworkService]
})
export class AppComponent {
    constructor(private userService: NetworkService) {
    }

    buttonDisabled = false;
    playButtonDisabled = false;
    maginNumber = 4264;

    submit(name: string, email: string, wish: string, room: string): void {

        if (name == null || email == null || wish == null || room == null) {
            alert("Заполни все поля, братюнь!");
            return;
        }

        this.buttonDisabled = true;

        let roomInt = Number.parseInt(room);
        roomInt = roomInt - this.maginNumber;

        let body = {name: name, email: email, wish: wish};

        this.userService.registerNewUser(body).subscribe(
            data => {
                this.userService.addUserToSession(roomInt, data.id).subscribe(
                    data => alert("Йоу, жди письмо с подтверждением!")
                )
            }
        );
    }


    play(session_id: string): void {
        if (session_id == null) {
            alert("Заполни все поля, братюнь!");
            return;
        }

        this.playButtonDisabled = true;

        let roomInt = Number.parseInt(session_id);
        roomInt = roomInt - this.maginNumber;

        this.userService.playSession(roomInt).subscribe(
            data => alert("Письма разосланы!")
        )
    }
}