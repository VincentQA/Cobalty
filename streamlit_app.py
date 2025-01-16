import streamlit as st
import openai
from openai.error import AuthenticationError, APIConnectionError, InvalidRequestError, RateLimitError

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
    except AuthenticationError:
        st.error("Clé API invalide. Veuillez vérifier votre clé et réessayer.")
        st.stop()
    except APIConnectionError:
        st.error("Erreur de connexion à l'API OpenAI. Veuillez vérifier votre connexion internet et réessayer.")
        st.stop()
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue : {e}")
        st.stop()

    # Étape 2 : Téléchargement du fichier par l'utilisateur
    uploaded_file = st.file_uploader("Téléchargez votre fichier", type=["txt", "csv", "json"])

    if uploaded_file is not None:
        # Lecture du contenu du fichier
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.write("**Contenu original du fichier :**")
            st.text(file_content)
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")
            st.stop()

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
                except InvalidRequestError as e:
                    st.error(f"Requête invalide : {e}")
                except RateLimitError:
                    st.error("Limite de requêtes atteinte. Veuillez patienter avant de réessayer.")
                except APIConnectionError:
                    st.error("Erreur de connexion à l'API OpenAI. Veuillez vérifier votre connexion internet et réessayer.")
                except Exception as e:
                    st.error(f"Une erreur inattendue est survenue lors de la modification : {e}")

                # Étape 4 : Transmission du fichier modifié à l'Assistant 2
                if st.button("Transmettre à l'Assistant 2 pour traitement"):
                    with st.spinner("Traitement en cours par l'Assistant 2..."):
                        try:
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
                        except InvalidRequestError as e:
                            st.error(f"Requête invalide : {e}")
                        except RateLimitError:
                            st.error("Limite de requêtes atteinte. Veuillez patienter avant de réessayer.")
                        except APIConnectionError:
                            st.error("Erreur de connexion à l'API OpenAI. Veuillez vérifier votre connexion internet et réessayer.")
                        except Exception as e:
                            st.error(f"Une erreur inattendue est survenue lors du traitement : {e}")
else:
    st.warning("Veuillez entrer votre clé API OpenAI.")
