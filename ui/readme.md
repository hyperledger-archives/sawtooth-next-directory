# Next Directory

Installation `npm install` to get all the latest packages. Node v6.11.3, npm v3.10.10.
Development server `ng serve`
Code scaffolding `ng generate component component-name` (generate new component)
Building project `ng build` (mock-data backend),  `ng build --env=prod` (api backend)
Running unit tests `ng test`
Running end-to-end tests `ng e2e`

Development Login: userId: 1, password: ''
Production Flow:
1.       Signup to create a new user
2.       Create a group
3.       Sign out
4.       Signup to create one more user, you will be logged in automatically.
5.       Click ‘All Groups’, click on a group & Request Access under the group that you’ve created in #2
6.       Sign out
7.       Sign back in as user in #1 (Tricky – you need a non-user-friendly ID to login that you would get as part of the signup API in #1)
8.       Click Requests and approve the request under Actions.
9.       You should see that the request is now approved & it disappears from ‘Requests’.
10.   Go to ‘My Groups’ and click on the group that you have selected in #5. Refresh the page and you should now see the new user in this group.