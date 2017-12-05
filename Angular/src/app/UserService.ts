import {Injectable} from '@angular/core';
import {Http, Response} from '@angular/http';
import 'rxjs/add/operator/map';

const SERVER_URL = 'http://78.24.216.173:8081/';

@Injectable()
export class NetworkService {
    constructor(private http: Http) {
    }

    registerNewUser(body: object) {
        return this.http.post(SERVER_URL + 'users/', body)
            .map((res: Response) => res.json())
    }


    addUserToSession(sessionId: Number, userId: Number) {
        return this.http.put(SERVER_URL + 'sessions/' + sessionId + '/', {new_user: userId})
            .map((res: Response) => res.json())
    }

    playSession(sessionId: Number) {
        return this.http.get(SERVER_URL + 'sessions/' + sessionId + '/')
    }
}