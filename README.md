# Daignose Me
A complete enf-to-end system that connects doctor with patient remotely and use generative AI to answer the patient query within minutes.

## Flow of Service

Let's suppose Ali live in  his village, which is far away from city. Due to dengue virus, many people in his village suffering from dengue fever. Consider there is no basic health facility near his village. Now here is our application plays a vital role.
Let me introduce another character Ahmed, who is health worker with basic nursing training from city. Ahmed is appointed by us in village's basic digital health facility.

Now Ali visit the health facility. 

Ali: Greetings
Ahmed : Warmly Welcome the Ali.

Ahmed : What happen with you?

Ali : From three to four days I am feeling very weak and also I have a temprature.

Ahmed : Note the body vitals and History of Ali. 

Now Ahmed will enter all details in our Application like request body.  Also possible database where previous patient data are stored. 

### Dengue Request Body
```
{  
    {
  "name_space": "dengue",
  "history": "The patient has a history of recent travel to a tropical or subtropical region where dengue fever is endemic. They may have been exposed to the dengue virus through mosquito bites during their travel. Dengue fever is a viral infection transmitted by the Aedes mosquito.",
  "description": "The patient is presenting symptoms of dengue fever, such as high fever, severe headache, and body pain. They may have a rash on their body and complain of pain behind the eyes. The patient's blood platelet count is being monitored regularly to assess their condition and ensure early detection of any complications. Adequate hydration and rest are being provided to support the patient's recovery.",
  "body_vitals": {
    "Weight": 69,
    "Body_temperature": 39.7,
    "Blood_pressure_diastolic": 78,
    "Blood_pressure_systolic": 126,
    "Heart_rate": "95 bpm",
    "Respiratory_rate": 19,
    "Blood_sugar_level": 115
  }
}

}
```

After sending request a full fledge response ready and sent to doctor for verification. If any modification required, doctor will do and sent back to Ahmed's dashboard.  

Following is the response sent by doctor.
### Dengue Response Body 
```
{
  "Status": "OK",
  "message": {
    "Doctor's views": "The patient's symptoms and travel history suggest a strong likelihood of dengue fever. The high fever, severe headache, body pain, and potential rash are all common symptoms of this disease. The patient's body vitals are generally stable, but the high body temperature is a concern. Regular monitoring of the blood platelet count is crucial as a sudden drop can indicate severe dengue. It's good that the patient is being kept hydrated and rested, as these are key to recovery.",
    "Medicine": "There is no specific medication to treat dengue fever. However, to manage symptoms, the patient can take paracetamol to reduce fever and pain. Aspirin or ibuprofen should be avoided as they can increase the risk of bleeding. If the patient's condition worsens or they develop severe dengue, hospitalization may be required for supportive care.",
    "Remedies": "The patient should continue to rest and stay hydrated. They should also avoid mosquito bites to prevent further transmission of the virus. Using mosquito repellents, wearing protective clothing, and staying in air-conditioned or screened-in areas can help. The patient should seek immediate medical attention if symptoms worsen or if they experience severe abdominal pain, persistent vomiting, rapid breathing, bleeding gums, or fatigue."
  }
}
```
Ahmed : These are the Remedies and medicine for you Ali.

Ali : Thanks  Ahmed.

Ali goes to his home and in few days he was cure from dengue fever.

**--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------**

These is the request body for ENT Patient. 
### Ent Request Body

```
{
  "name_space": "ent",
  "description": "asthma in a 5-year-old, mother states he has been wheezing and coughing.",
  "history": "this 5-year-old male presents to children's hospital emergency department by the mother with \"have asthma.\" mother states he has been wheezing and coughing. they saw their primary medical doctor. he was evaluated at the clinic, given the breathing treatment and discharged home, was not having asthma, prescribed prednisone and an antibiotic. they told to go to the er if he got worse. he has had some vomiting and some abdominal pain. his peak flows on the morning are normal at 150, but in the morning, they were down to 100 and subsequently decreased to 75 over the course of the day.",
  "body_vitals": {
    "temperature": 98.7,
    "pulse": 105,
    "Respiratory_rate": 28,
    "Blood_pressure_diastolic": 78,
    "Blood_pressure_systolic": 126,
    "weight": 16.5,
    "oxygen_saturation_low": "91%",
    "general": "this is a well-developed male who is cooperative, alert, active with oxygen by facemask.",
    "heent": "head is atraumatic and normocephalic. pupils are equal, round, and reactive to light. extraocular motions are intact and conjugate. clear tms, nose, and oropharynx.",
    "neck": "supple. full painless nontender range of motion.",
    "chest": "tight wheezing and retractions heard bilaterally.",
    "heart": "regular without rubs or murmurs.",
    "abdomen": "soft, nontender. no masses. no hepatosplenomegaly.",
    "skin": "no significant bruising, lesions or rash.",
    "extremities": "moves all extremities without difficulty, nontender. no deformity.",
    "neurologics": "symmetric face, cooperative, and age-appropriate."
  }
}

```
**Note** Keys are same in ENT response body. Values will be according to ENT data.

## How you can run this Repo?

Clone this repo using this command.
```bash
git clone https://github.com/Drwaish/Xavor_AI_Bootcamp.git
cd Xavor_AI_Bootcamp
``` 
Now install requirements
```bash
pip install -r requirements.txt
```

For Gradio Application, run this command.
```bash
python app.py
```

If you want console base output.
```bash
python main.py
```

if you want to test apis.
```bash
python flask_api.py
```
Make sure in request header api access key is available. `api-key` is key and `zain` is value.  
Use `thunder-collection_xavor.json` collection for request on thunder client api tester.


If you have any queries kindly let me know.




