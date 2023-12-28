"""Create prompt for mainting uniformity """
from pinecone_data import get_context
real_query = """
History:
The person recently visited a warm place, maybe tropical or subtropical, \
where dengue fever is common. It's possible they got the dengue virus from mosquito \
bites during their trip.\
 Dengue fever is a sickness caused by a virus spread by Aedes mosquitoes.
Body Vitals:
 In the early stage of dengue fever, the person's body temperature \
 might go up to about 104°F (40°C). They might also have a strong headache,\
 along with pain in the joints and muscles, a rash, and discomfort behind the eyes.\
 As the fever continues, \
 their blood platelet count might go down, making them more likely to bleed.
 Description
 The person is showing signs of dengue fever, like a high fever, intense headache, \
 and body pain. They might have a rash on their body and mention pain behind the eyes. \
 Doctors are keeping a close eye on the patient's blood platelet count to catch any issues early. \
 The patient is getting enough fluids and rest to help them get better.
"""
def prompt_maker(query = real_query):
    """
    Build prompt to create first report for doctor.

    Paramters
    ---------
    Query
        Patient describe what he/ she feels
    """
    descript1, descript2, descript3 = get_context(query, name_space='dengue')
    previous_patient = f'<<CONTEXT>> \n {descript1} \n {descript2} \n {descript3} \n <<QUERY>> \n \n {query}'
    return previous_patient
if __name__ =="__main__":
    print(prompt_maker(real_query))
