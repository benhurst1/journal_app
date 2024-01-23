### Requirements

*Structure*
- [ ] Backend: Design & create your backend application server
  - [ ] Set up your backend boilerplate (e.g. database URI)
  - [x] Create the note schema
  - [x] Create the backend routes (e.g. GET, POST)
- [x] Frontend: Identify and create the main components of your frontend application 
(e.g. Header, Note input area, list of previously entered notes, dialog or area
to update previously entered notes)

*Style*
- [ ] You may use any style you choose. However, it should be consistent (e.g.
font, font size, color scheme, layout, etc.).
  - See [Consistent Web Design](https://1stwebdesigner.com/consistent-web-design/)
  - See [Why is consistency important in Web Design?](https://laceytechsolutions.co.uk/blog/importance-of-consistency-in-web-design/)

*Functionality*
- Backend: Implement user authentication
  - [x] Add a signup route to allow users to create an app account (e.g. user
  name & password) for themselves
  - [x] Add a login route to allow users who have completed the signup process
  to login to the application
- Frontend: Implement the necessary functionality for each component. Users
must be able to:
  - [x] signup to create an app-specific account
  - [x] login to use the app
  - [x] post a new notes to the list of previously entered notes
  - [x] modify previously added notes
  - [x] delete previously entered notes
- Frontend: Miscellaneous functionality
  - [x] Use the API exposed by the app Backend to deliver functionality to 
your users
  - [x] Frontend: Application secrets and user credentials should not be stored or
left exposed in the browser

*Other*
- [ ] Your repo needs to have a robust `README.md` (See [Keys to a Well-Written Readme](https://medium.com/chingu/keys-to-a-well-written-readme-55c53d34fe6d))
- [ ] Before submitting make sure that there are no errors in the developer console
- Anticipate and handle any edge cases
  - [x] Does entering random data, such as a mix of alphbetic, numeric, and
  special characters in the search input result in an error?
  - [x] What is displayed if the search location is not found?
- [ ] The app should be responsive across multiple devices (e.g. phone, tablet, 
laptop, and desktop computers)

**Extras (Not Required)**
- [ ] Add the ability for users to upload pictures (or even audio clips) to notes
- [ ] Allow notes to be formatting using Markdown
- [ ] Use as FEW external packages and libraries as possible to reduce the 
number of dependencies.
- [ ] Include tests cases using tools like Jest, Enzyme, etc.
- [ ] Use Accessibility techniques (i.e. a11ly) to improve your site for users 
with impairments (see [A11Y Project](https://a11yproject.com/))
- [ ] Add a `CONTRIBUTING.md` file with instructions on how to contribute to
your project
- [ ] Implement service workers to improve performance by relying on cached 
data (see [Service Workers: An Introduction](https://developers.google.com/web/fundamentals/primers/service-workers))