/*=========================================================================
Copyright © 2017 T-Mobile USA, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
=========================================================================*/
import {Injectable} from '@angular/core';
import * as _ from "lodash";
import {Headers, RequestOptions} from "@angular/http";
import {MatSnackBar} from "@angular/material";
@Injectable()
export class UtilsService {
    constructor(private snackBar: MatSnackBar){}

    setTimeoutPromise(milliseconds) {
        const promise = new Promise((resolve: any, reject: any) => {
            setTimeout(() => {
                resolve(resolve, reject);
            }, milliseconds);
        });
        return promise;
    }

    isObjectEmpty = (obj) => {
        return (Object.keys(obj).length === 0 && obj.constructor === Object);
    };

    debounce(func, wait, immediate) {
        let timeout;
        return function () {
            let context = this, args = arguments;
            let later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            let callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    catchError(error) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }

    stubHttp(response) {
        return this.setTimeoutPromise(100)
            .then(() => {
                return response;
            })
    }

    defaultSnackBar(message) {
        return this.snackBar.open(message, 'Dismiss', {duration: 5000});
    }

}
