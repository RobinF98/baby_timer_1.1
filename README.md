# BABY TIMER

---

Baby timer is a simple but useful website that you can use to log your baby's feeds and diapers.
It features user accounts and the ability to add multiple babies.
View all your baby's sleeps and diapers in one list, with notes for each entry on the side.
Easily edit and delete log entries, and with it's responsive design you can take Baby Timer with you no matter what device you're using.

---

## Features

---

- ### Nav bar

  - The responsive naviagtion bar provides quick and easy access to the things you will need most.
  - Here you will find a logs dropdown, the homepage link, and the logout button.
  - On smaller pages the nav bar switches to a dropdown to save space

- ### Sign up / Sign in

  - The sign in and sign up pages are styled neatly, making extensive use of bootstrap templates.
  - New users can create an account that they can use to add babies and entries.
  - User authentication and sign in / sign up is powered by AllAuth

- ### Date / Time Input

  - Users can easily select dates and times for entries (like baby's birthday, or sleep times)
  - This is done using the bootstrap_datepicker_plus widgets, which provide an easy to use gui for date / time selection

- ### Footer

  - The footer is simple, featuring nothing more than the year of creation and a link to the project's GitHub repository.

- ### Home Page

  - Here the user can see all babies registered to them, and add babies by clicking on the green "Add new baby' buttons at the bottom of the page

- ### Logs page

  - Users can see all log entries collated in one list on the logs page.
  - From here users can click/tap on log entries to edit or delete them.

- ### Add entry pages

  - Users can add log entries or babies on a neatly styled form.
  - The form has all fields the entry or baby requires, including a notes text field, which can be used for any additional information.
  - The form features bright submit/delete/cancel buttons for intuitive control.
  - The form does valdation on user input, ensuring all necessary fields are filled and preventing things like a sleep entry ending before it began.

- ### Delete / logout confirmation

  - Anytime the user is about to make a critical change to the site, such as logging out or deleting an entry, a confirmation modal appears.
  - The modal makes it clear to the user what will happen if they continue, so as to prevent accidental deletions or logouts.

- ### Access control

  - Users are require to be logged in to access any of the site's functionality.
  - Users are also unable to view the logs of a baby registered to another user.
  - If this is attempted by modifying the url, the user is redirected to the home page.

## Future Features

---

- ### Additional entry types

  - Despite what some may think, babies do a good bit more than just sleeping and soiling diapers.
  - Functionality for feeds (breast, bottle, and solid foods) can be added easily
  - Functionality for any medication the baby may be taking can be added as well.

- ### AllAuth email verification

  - As it currently stands site is accessed using a username and password. While this is secure, there is a good bit more that can be done in terms of user accesiability.
  - AllAuth offers built in email verification, forgot password, and password reset functionality.

## Testing

---

- The site was tested for responsiveness on the Firefox and Chrome browsers, using the developer tools that come with the browsers.
- As the site is styled almost exclusively bootstrap, the responsiveness is very good by default.
- Of primary importance is how the site operates on the backend.
  - Extensive manual testing was conducted to ensure teh site behaved as intended, with no strange redirects or buttons doing anything other than what they say they will do.
  - Users can add/edit/delete babies/diapers/sleep entries.
  - Users can view all entries registered to a particular baby.
  - Users are redirected if they attempt to access another user's baby or baby's logs via the url.

- ### BUGS
  - [SOLVED] Users can access other user's records by changing pk in url
    - Solved by creating UserAccessMixin which checks to see if the user that the records being requested are registered to is the current session user.
  - [SOLVED] Delete confirmation modal deletes object when cancel button is clicked
    - Solved by moving cancel button outside the delete form heirarchy and adding 
    ```type="submit"```
    to the Delete button attributes.
