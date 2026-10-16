def get_pdf_extraction_prompt(raw_pdf_text):
    """
    Instructs the AMD LLM to extract the medical history into our exact JSON schema.
    """
    return f"""
    Sei un assistente clinico esperto. Analizza la seguente Lettera di Dimissione Ospedaliera.
    Estrai le informazioni richieste attenendoti RIGOROSAMENTE ai fatti presenti nel testo.
    Traduci tutte le diagnosi in Italiano affinché corrispondano al nostro database.
    
    Testo del referto:
    {raw_pdf_text}
    """

def get_zero_diagnosis_prompt(patient_answers):
    """
    The Zero-Diagnosis Summarizer Prompt for the patient check-in feature.
    """
    return f"""
    You are an objective clinical scribe. Summarize the patient's reported answers into maximum two concise sentences in Italian for the attending physician[cite: 2]. 
    
    STRICT NEGATIVE CONSTRAINTS[cite: 2]:
    - NEVER diagnose a condition[cite: 2].
    - NEVER reassure the patient[cite: 2].
    - NEVER suggest medications or treatments[cite: 2].
    
    Patient Answers:
    {patient_answers}
    """