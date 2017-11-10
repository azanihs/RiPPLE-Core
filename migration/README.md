# peerwise-flashcard
PeerWise Flashcard - A flashcard based application to import questions from [PeerWise](http://www.peerwise.cs.auckland.ac.nz/) and display them as flashcards.

<b>Purpose</b>
The purpose of this application is to allow students to generate questions on [PeerWise](http://www.peerwise.cs.auckland.ac.nz/), share them with each other and later 
export these questions so that they can be used by later offerings of a course as review. 

<b>Collaborators</b> : Dr. Hassan Khosravi & Akshat Divekar

<b>Project Structure </b>

<h6>For Admins</h6>
1. <b>index.php</b> - the file served when the project folder is first visited. This is the login page for admins

2. <b>options.php</b> - shows instructions for importing a new peerwise export (note : if a database does not already exist, a new one will be created, or else questions will be added to the existing pw_orig.db) , deleting an existing peerwise database (if one exists) and modifying the question tags (if a database already exists)

3. <b>modify.php</b> - shows a page to add new quiz topics (or tags). If previous tags already exist, this list will be pre-populated with them.

4. <b>assign.php</b> - called from the modify.php page and generates a (long) single page with all the questions. Each question has a dropdown on the left-hand side to select the topic to assign the question to. 

5. <b>save.php</b> - saves the changes selected on assign.php deleting any questions that have been marked for deletion.

<h6>For Students</h6>
6. <b>select.php</b> - shows the list of quiz topics that a student can select. Pressing start quiz will load all the questions for the topic

7. <b>quiz.php</b> - serves the quiz selected in select.php. This is actually a single long page (to avoid hitting the DB again and again) and divs for previous and next questions are hidden/shown as required.

<h6>Deployment Instructions<h6>

1. Login using the admin interface by navigating to the project root in a web browser

2. Follow the instructions on-screen to add questions to the existing database or create a new database. You can also click on the `Delete Database` button to delete the exising database

3. Modify the existing question tags or assign new tags to questions. 

4. Assign a tag to assign to each of the questions. If you want to do this later, indicate the tag as `Do not Include`. If you wish to delete the question, indicate the tag as `Delete Question` and it will be deleted from the database

5. Once you are done assigning tags, follow the instructions on-screen in order to serve the quizzes will appear






