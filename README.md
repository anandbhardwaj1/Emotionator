# EMOTIONATOR (Team: CRUSADERS)

## START-UP INSTRUCTIONS

1. Navigate to the directory "./Emotionator/emotionator".
2. Run the command **python manage.py runserver** on powershell/command-prompt.

## PROJECT DESCRIPTION:

### 1.	TECHNICAL WORKFLOW :-

#### **FIRST PHASE: EMOTION RECOGNITION**

(This phase consists of **two components**.)

The project will contain multiple machine learning/deep learning models, each pertaining to a specific task.

•	**COMPONENT A**: This will be a model, defined and optimized for recognizing the emotion of the user from the tone of their voice; the model will be trained on recorded voice samples from diverse sources and various voice-actors so as to avoid over-fitting.

•	**COMPONENT B**: This will be another model which will make use of CNN/Open-CV technologies to recognise the emotion of a person from their facial expression. The model architecture will be tuned and trained using the huge and robust stock datasets available online for this task as well as practical and real-life pictures.

The accuracy of these models (and other subsequent models if added) will be determined and the weighted average of their outcomes will be used to determine the overall emotion of the user. This outcome will be used as an input in the second phase of the application.


#### **SECOND PHASE: RECOMMENDATION SYSTEM**

(This phase consists of **one component**.)


The emotion of the user obtained in the first phase will be used to provide the user with content which matches their current mood. 

•	**COMPONENT C**: This component will consist of a web/app scraping and searching algorithm which would search through the genres of songs, tags of videos and other content in order to find, organise and output the content which pertains to the emotional state of the user.

The output of the second phase will be displayed to the user along with the state of the user obtained in the first phase in a presentable manner using the frontend of the project defined in the third phase.

#### **THIRD PHASE: FRONTEND AND DESIGN**

(This phase consists of **one component**.)

•	**COMPONENT D**: This is going to be a user-friendly web-application complete with a robust python-based (preferably) backend for organising user input as well as running models and recommendation systems. The frontend will be minimalist and presentable providing both the content recommendation and user state coupled with an easy-to-use interface.

Integration of all the components will result in a web-application capable of taking user auditory and visual input, recognising their emotion and providing them with a rich repository of content in a short span of time.

### 2.	USAGE AND BENIFITS:-

•	The application aims to save the time and hassle of scrolling the web in order to find the content which would fulfil and match our cravings.
•	It will enable the user to get to know about new content in various emotional genres without the need of searching through multiple websites.
•	Content from multiple sources as well as of different types can be accessed in a single application.
•	This can also be used to know and monitor the user’s emotional state at any time which would not only indicate depressive episodes but also help in providing helpful content in combating them.





## PROJECT TIMELINE:


**Week 1: Component A**
	
Making the model to recognize the user’s emotion through his/her voice.

**Week 2: Component B**
	
Making the model to recognize the user’s emotion through his/her facial expression.

**Week 3: Component C**
	
Making the recommendation system for providing songs/videos based on the user’s emotions.

**Week 4: Component D, Integration and Final touch-ups**
	
Integrating all the models and giving front-end to the application.




## ADDITIONAL FEATURES:


Additional components may be added to the project keeping in view the availability of time and resources. These components are not finalised and may or may not be present in the final project entirely or in their below mentioned form.

•	AI CHATBOT/QUESTIONNAIRE: An additional layer of input which would include a dynamic set of questions helping to identify the emotional state of the user better. This would also help the users which do not/cannot provide access to their audio/video feed.

•	RECOMMENDATION BASED ON TASTE: The user may provide access to their browser/searching history in order to provide data to the application as to what the general taste of the user is and to better provide them with the content of their liking.



