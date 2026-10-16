from pydantic import BaseModel, Field
from typing import List

# 1. Known Allergies
class Allergy(BaseModel):
    substance: str = Field(description="The name of the allergen (e.g., Penicillina)")
    reaction_type: str = Field(description="The type of reaction (e.g., anafilassi, rash cutaneo)")
    is_critical: bool = Field(description="Set to True ONLY if the severity is CRITICAL or anaphylaxis")

# 2. Active Medications
class Medication(BaseModel):
    commercial_name: str = Field(description="Drug commercial name (e.g., Cardioaspirin)")
    active_ingredient: str = Field(description="Active ingredient (e.g., Acido acetilsalicilico)")
    dosage: str = Field(description="Dosage amount (e.g., 100mg)")
    frequency: str = Field(description="How often it is taken (e.g., 1 volta al giorno)")

# 3. Primary Diagnoses & Conditions
class Diagnosis(BaseModel):
    condition: str = Field(description="Extracted condition formatted for quick reading")
    status: str = Field(description="Status: 'Attiva' (Active) or 'Risolta' (Resolved)")

# 4. The Master Payload for the Backend
class PatientSummary(BaseModel):
    allergies: List[Allergy]
    active_medications: List[Medication]
    diagnoses: List[Diagnosis]
    polypharmacy_warning: bool = Field(description="True if dangerous drug interactions exist")