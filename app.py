import gradio as gr
from prompting import prompt_maker
from llm_prompt import create_llm_chain


patient_data = """
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
def doctor_prescription(textbox_value):
    prompt = prompt_maker(textbox_value)
    chain = create_llm_chain()
    response = chain.run(prompt)
    data = eval(response)
    print((data))

    return data["Doctor's Views"], data['Medicine'], data["Remedies"]

with gr.Blocks(theme = gr.themes.Base()) as demo:
    gr.HTML("<h1><center> Daignose Me</center></h1>")
    gr.HTML("<h3><center>Instant Way to Cure</center></h3>")
    with gr.Row():
        with gr.Column():
            query = gr.TextArea(label="Input Phrase")
        with gr.Column():
            views = gr.TextArea(label="Doctor's Views", lines=4)
            medicine = gr.TextArea(label="Medicine", lines=4)
            remedies = gr.TextArea(label="Remedies", lines=4)
  
    btn = gr.Button("Generate")
    btn.click(doctor_prescription, inputs=[query], outputs=[views, medicine, remedies])
    gr.Examples([patient_data], inputs=[query])
if __name__=="__main__":
  demo.launch(share = True, debug = True)


