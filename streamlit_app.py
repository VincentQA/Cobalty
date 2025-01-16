import streamlit as st
import openai

# Titre de l'application
st.title("Pipeline de Traitement de Fichiers avec Assistants OpenAI")

# Étape 1 : Saisie de la clé API OpenAI par l'utilisateur
api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

if api_key:
    # Configuration de la clé API OpenAI
    openai.api_key = api_key

    # Vérification de la validité de la clé API
    try:
        openai.Model.list()
        st.success("Clé API valide.")
    except Exception as e:
        st.error(f"Clé API invalide : {e}")
        st.stop()

    # Étape 2 : Téléchargement du fichier par l'utilisateur
    uploaded_file = st.file_uploader("Téléchargez votre fichier", type=["txt", "csv", "json"])

    if uploaded_file is not None:
        # Lecture du contenu du fichier
        file_content = uploaded_file.read().decode("utf-8")
        st.write("**Contenu original du fichier :**")
        st.text(file_content)

        # Étape 3 : Modification du fichier par l'Assistant 1
        if st.button("Modifier le fichier avec l'Assistant 1"):
            with st.spinner("Modification en cours..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4-turbo",
                        messages=[
                            {"role": "system", "content": "Vous êtes l'Assistant 1 chargé de modifier le fichier."},
                            {"role": "user", "content": f"Voici le contenu du fichier à modifier :\n\n{file_content}"}
                        ]
                    )
                    modified_content = response.choices[0].message.content
                    st.write("**Contenu modifié par l'Assistant 1 :**")
                    st.text(modified_content)

                    # Étape 4 : Transmission du fichier modifié à l'Assistant 2
                    if st.button("Transmettre à l'Assistant 2 pour traitement"):
                        with st.spinner("Traitement en cours par l'Assistant 2..."):
                            response = openai.ChatCompletion.create(
                                model="gpt-4-turbo",
                                messages=[
                                    {"role": "system", "content": "Vous êtes l'Assistant 2 chargé de traiter le fichier modifié."},
                                    {"role": "user", "content": f"Voici le contenu du fichier modifié :\n\n{modified_content}"}
                                ]
                            )
                            final_output = response.choices[0].message.content
                            st.write("**Résultat final après traitement par l'Assistant 2 :**")
                            st.text(final_output)
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de l'appel à l'API OpenAI : {e}")
else:
    st.warning("Veuillez entrer votre clé API OpenAI.")
