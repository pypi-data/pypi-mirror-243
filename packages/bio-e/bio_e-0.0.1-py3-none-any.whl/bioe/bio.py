# BioE
# Python package for biology students.

import random

def quiz():
    questions = {
        1: "Stem cells are important for living organisms because they are cells which will undergo cell division and cell differentiation to form tissues and organs such as the heart, lungs and skin.\n"
           "Embryonic stem cells are widely used in stem cell research for medical purposes. \n"
           "Discuss how stem cell research is beneficial to human health.",
        2: "Explain the importance of cellulose to herbaceous plants.",
        3: "State the function of smooth muscle tissue.",
        4: "Herbicide is often used to control the population of weeds in a garden by destroying the ATPase enzymes in the cells of the weeds.\n"
           "One of the effects of the herbicide is inhibiting the intake of minerals by the plants.\n"
           "Explain how the herbicide can inhibit the transport of minerals in the weed plants.",
        5: "Chillies are usually used as a decoration in cooking. Chillies will be cut longitudinally into a few parts. \n"
           "After removing the seeds inside, the chillies cut are soaked in water for 20 to 30 minutes. \n"
           "The results are shown in the diagram on the right. \n"
           "Why should the chillies be soaked in water?",
        6: "Why will excessive fertilisers cause a plant to wilt?",
    }

    def get_correct_answer(question_id):
        answers = {
            1: "Stem-cell research is a research that is carried out on stem cells for use in medicine. \n"
               "The research is important in treating diseases. \n"
               "The stem cells can be used in treating blood cancer such as leukemia and replacing damaged tissues and organs. \n"
               "For example, the production of nerve tissues to treat Alzheimer's and Parkinson's disease and producing new heart muscles to treat heart problems.",
            2: "Cellulose controls the water content of the cells to enable the cells to always to be turgid. \n"
               "This gives support to the herbaceous plants.",
            3: "The smooth muscle tissue contracts and relaxes to allow peristalsis to occur in the digestive tract.",
            4: "Herbicide destroys the ATPase enzymes in the cell. \n"
               "The ATPase enzymes are important in catalysing the hydrolysis of ATP into ADP and non-organic phosphate.\n"
               "Without the enzyme, active transport cannot occur as there is no phosphate ion to bind with the binding site of the carrier protein to allow it to change its shape and assist the movement of mineral salts into the cells of the weed plants.",
            5: "Water is hypotonic towards the cells of the inner part of the chillies. \n"
               "Water molecules diffuse into the inner part by osmosis.\n"
               "The outer part of the chillies has waxy layer which does not allow water to diffuse into the cells.\n"
               "Cells in the inner part become turgid and causes the chillies to bend outward. ",
            6: "Excessive fertilisers cause the ground water to be hypertonic to hair cells. \n"
               "Water molecules diffuse out of the root hair cells by osmosis which causes the cells to be plasmolysed.",
        }

        return answers.get(question_id, "Unknown")

    while True:
        question_id = random.choice(list(questions.keys()))
        question_text = questions[question_id]

        user_answer = input(f"\nQUESTION: \n{question_text}\n\nYOUR ANSWER: ").strip() or "[Skipped]"
        print(f"{user_answer}")

        correct_answer = get_correct_answer(question_id)
        print(f"\nCORRECT ANSWER: \n{correct_answer}\n")

        cont = input("Would you like to continue? [Y/N]: ")
        if cont.lower() != "y":
            print("\nWe hope the experience was helpful. \n"
                  "2023 © BioE")
            break

quiz()
