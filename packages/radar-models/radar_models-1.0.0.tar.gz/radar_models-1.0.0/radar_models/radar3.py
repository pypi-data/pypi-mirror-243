from datetime import datetime, date
from typing import Callable, ClassVar, Optional, Union

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel

# --- AdultEQ5D5L --- #


class AdultEQ5D5LBase(SQLModel):
    patient_id: str = Field(foreign_key="patient.id")
    assessment_date: date
    age: int
    gender: int
    mobility: int
    self_care: int
    usual_activities: int
    pain_discomfort: int
    anxiety_depression: int
    health: int


class AdultEQ5D5L(AdultEQ5D5LBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "adult_eq5d5l"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class AdultEQ5D5LCreate(AdultEQ5D5LBase):
    pass


class AdultEQ5D5LRead(AdultEQ5D5LBase):
    id: int


# --- AdverseEvents --- #


class AdverseEventBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    review_date: date
    hospitalisation: bool
    adverse_event: bool
    new_onset_cancer: date
    cancer_cause: bool
    thromboembolism: date
    caused_venous_thrombo_embolism: int
    myocardial_infarction: date
    caused_acute_myocardial_infarction: int
    stroke: date
    caused_stroke: int
    ischaemic_attack: date
    caused_ischaemic_attack: int
    other_adverse_event: date
    other_toxicity: str
    caused_other: int
    date_of_death: date
    cause_of_death: str


class AdverseEvent(AdverseEventBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "adverse_event"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class AdverseEventCreate(AdverseEventBase):
    pass


class AdverseEventRead(AdverseEventBase):
    id: int


# --- AlportAssessment --- #


class AlportAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    date_of_picture: date
    deafness_index: int
    deafness_date: Optional[date]
    hearing_aid_date: Optional[date]


class AlportAssessment(AlportAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "alport_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class AlportAssessmentCreate(AlportAssessmentBase):
    pass


class AlportAssessmentRead(AlportAssessmentBase):
    id: int


# --- Anthropometric --- #


class AnthropometricBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    height: int
    weight: float
    bmi: float
    hip: float
    waist: float
    arm: float
    up_and_go: float
    grip_dominant: float
    grip_non_dominant: float
    karnofsky: int
    systolic_one: int
    diastolic_one: int
    systolic_two: int
    diastolic_two: int
    systolic_three: int
    diastolic_three: int
    systolic_mean: int
    diastolic_mean: int


class Anthropometric(AnthropometricBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "anthropometric"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class AnthropometricCreate(AnthropometricBase):
    pass


class AnthropometricRead(AnthropometricBase):
    id: int


# --- Biomarker --- #


class BiomarkerBase(SQLModel):
    biomarker_name: str
    biomarker_type: str


class Biomarker(BiomarkerBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "biomarker"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class BiomarkerCreate(BiomarkerBase):
    pass


class BiomarkerRead(BiomarkerBase):
    id: int


# --- BiomarkerBarcode --- #


class BiomarkerBarcodeBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    barcode: str
    sample_date: datetime


class BiomarkerBarcode(BiomarkerBarcodeBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "biomarker_barcode"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class BiomarkerBarcodeCreate(BiomarkerBarcodeBase):
    pass


class BiomarkerBarcodeRead(BiomarkerBarcodeBase):
    id: int


# --- BiomarkerResult --- #


class BiomarkerResultBase(SQLModel):
    biomarker_id: int = Field(foreign_key="biomarker.id")
    biomarker_sample_id: int = Field(foreign_key="biomarker_sample.id")
    biomarker_result_value: float
    measure_unit: str


class BiomarkerResult(BiomarkerResultBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "biomarker_result"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class BiomarkerResultCreate(BiomarkerResultBase):
    pass


class BiomarkerResultRead(BiomarkerResultBase):
    id: int


# --- BiomarkerSample --- #


class BiomarkerSampleBase(SQLModel):
    barcode_id: int = Field(foreign_key="biomarker_barcode.id")
    biomarker_sample_label: str


class BiomarkerSample(BiomarkerSampleBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "biomarker_sample"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class BiomarkerSampleCreate(BiomarkerSampleBase):
    pass


class BiomarkerSampleRead(BiomarkerSampleBase):
    id: int


# --- CalciphylaxisAssessment --- #


class CalciphylaxisAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    lesion: bool
    lesion_location: str
    infection: bool
    infection_location: str


class CalciphylaxisAssessment(CalciphylaxisAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "calciphylaxis_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CalciphylaxisAssessmentCreate(CalciphylaxisAssessmentBase):
    pass


class CalciphylaxisAssessmentRead(CalciphylaxisAssessmentBase):
    id: int


# --- CalciphylaxisAssessmentOption --- #


class CalciphylaxisAssessmentOptionBase(SQLModel):
    calciphylaxis_assessment_id: int = Field(foreign_key="calciphylaxis_assessment.id")
    option_id: int = Field(foreign_key="option.id")


class CalciphylaxisAssessmentOption(CalciphylaxisAssessmentOptionBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "calciphylaxis_assessment_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CalciphylaxisAssessmentOptionCreate(CalciphylaxisAssessmentOptionBase):
    pass


class CalciphylaxisAssessmentOptionRead(CalciphylaxisAssessmentOptionBase):
    id: int


# --- CancerTumours --- #


class CancerTumourBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    tumour_type: str
    other_tumour_name: str
    diagnosis_date: date
    tumour_count: int
    cns_image: str
    progression_date: date
    t_cat: str
    n_cat: str
    m_cat: str
    radiologic_tumor_size: str
    pathologic_tumor_size: str
    tumor_location: str


class CancerTumour(CancerTumourBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "cancer_tumour"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CancerTumourCreate(CancerTumourBase):
    pass


class CancerTumourRead(CancerTumourBase):
    id: int


# --- CKDAfricaGenetic --- #


class CKDAfricaGeneticBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    sickle_cell: str
    other_sickle_cell: str
    apol_1: str


class CKDAfricaGenetic(CKDAfricaGeneticBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "ckd_africa_genetic"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CKDAfricaGeneticCreate(CKDAfricaGeneticBase):
    pass


class CKDAfricaGeneticRead(CKDAfricaGeneticBase):
    id: int


# --- CKDAfricaRiskFactor --- #


class CKDAfricaRiskFactorBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    preterm_birth: str
    low_birth_weight: str
    malnutrition: str
    hospital_malnutrition: str


class CKDAfricaRiskFactor(CKDAfricaRiskFactorBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "ckd_africa_risk_factor"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CKDAfricaRiskFactorCreate(CKDAfricaRiskFactorBase):
    pass


class CKDAfricaRiskFactorRead(CKDAfricaRiskFactorBase):
    id: int


# --- ClinicalLetters --- #


class ClinicalLettersBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    letter_date: date
    comments: str


class ClinicalLetters(ClinicalLettersBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "clinical_letters"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ClinicalLettersCreate(ClinicalLettersBase):
    pass


class ClinicalLettersRead(ClinicalLettersBase):
    id: int


# --- Code --- #


class CodeBase(SQLModel):
    coding_system: str
    code_describes: str
    code: str
    code_label: str


class Code(CodeBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "code"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CodeCreate(CodeBase):
    pass


class CodeRead(CodeBase):
    id: int


# --- Cohort --- #


class CohortBase(SQLModel):
    cohort_code: str
    cohort_name: str
    cohort_short_name: str


class Cohort(CohortBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "cohort"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CohortCreate(CohortBase):
    pass


class CohortRead(CohortBase):
    id: int


# --- CohortDiagnose --- #


class CohortDiagnosisBase(SQLModel):
    cohort_id: int = Field(foreign_key="cohort.id")
    diagnosis_id: int = Field(foreign_key="diagnosis.id")
    diagnosis_type: int = Field(foreign_key="option.id")


class CohortDiagnosis(CohortDiagnosisBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "cohort_diagnosis"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CohortDiagnosisCreate(CohortDiagnosisBase):
    pass


class CohortDiagnosisRead(CohortDiagnosisBase):
    id: int


# --- CohortObservation --- #


class CohortObservationBase(SQLModel):
    cohort_id: int = Field(foreign_key="cohort.id")
    observation_id: int = Field(foreign_key="observation.id")
    weight: int


class CohortObservation(CohortObservationBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "cohort_observation"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CohortObservationCreate(CohortObservationBase):
    pass


class CohortObservationRead(CohortObservationBase):
    id: int


# --- CohortPatient --- #


class CohortPatientBase(SQLModel):
    cohort_id: int = Field(foreign_key="cohort.id")
    patient_id: int = Field(foreign_key="patient.id")
    recruited_date: date
    removed_date: Optional[date]


class CohortPatient(CohortPatientBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "cohort_patient"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CohortPatientCreate(CohortPatientBase):
    pass


class CohortPatientRead(CohortPatientBase):
    id: int


# --- Consent --- #


class ConsentBase(SQLModel):
    consent_code: str
    consent_label: Optional[str]
    is_paediatric: bool = Field(default=False)
    release_date: date
    consent_url: str
    is_retired: bool = Field(default=False)


class Consent(ConsentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "consent"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ConsentCreate(ConsentBase):
    pass


class ConsentRead(ConsentBase):
    id: int


# --- Consultant --- #


class ConsultantBase(SQLModel):
    specialty_id: int = Field(foreign_key="specialty.id")
    first_name: str
    last_name: str
    email: Optional[str]
    telephone_number: Optional[str]
    gmc_number: Optional[int]


class Consultant(ConsultantBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "consultant"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ConsultantCreate(ConsultantBase):
    pass


class ConsultantRead(ConsultantBase):
    id: int


# --- Country --- #


class CountryBase(SQLModel):
    country_name: str
    country_code: str


class Country(CountryBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "country"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CountryCreate(CountryBase):
    pass


class CountryRead(CountryBase):
    id: int


# --- CountryEthnicity --- #


class CountryEthnicityBase(SQLModel):
    ethnicity_id: int = Field(foreign_key="ethnicity.id")
    country_id: int = Field(foreign_key="country.id")


class CountryEthnicity(CountryEthnicityBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "country_ethnicity"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CountryEthnicityCreate(CountryEthnicityBase):
    pass


class CountryEthnicityRead(CountryEthnicityBase):
    id: int


# --- CountryNationality --- #


class CountryNationalityBase(SQLModel):
    nationality_id: int = Field(foreign_key="nationality.id")
    country_id: int = Field(foreign_key="country.id")


class CountryNationality(CountryNationalityBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "country_nationality"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CountryNationalityCreate(CountryNationalityBase):
    pass


class CountryNationalityRead(CountryNationalityBase):
    id: int


# --- CystinosisAdultVisit --- #


class CystinosisAdultVisitBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    visit: int
    visit_date: date
    urine_measurement: str
    urine_output: float
    voiding_overnight: str
    continent_day: str
    fluid_intake: float
    admission_dehydration: int
    constipation: str
    diarrhea: str
    nausea: str
    vomiting: str
    rickets: str
    kyphoscoliosis: str
    fractures: str
    muscle_strength: str
    ankle_strength: float
    elbow_strength: float
    hand_strength: float
    hip_strength: float
    knee_strength: float
    shoulder_strength: float
    wrist_strength: float
    swallowing_difficulties: str
    swallowing_difficulties_detail: str
    joint_surgery: str
    visual_impairment: str
    photophobia: str
    photophobia_grade: str
    keratoplasty_date: date
    acuity: str
    gahl_score: str
    intraocular_pressure_r: str
    intraocular_pressure_l: str
    fev1: float
    vc: float
    snip: float
    seizure: str
    headache: str
    muscle_weakness: str
    learning_difficulties: str
    cognitive_difficulties: str
    cognitive_difficulties_score: str
    movement_disorder: str
    intracranial_hypertension: str
    diabetes: str
    thyroid: str
    hypothyroidism: str
    tanner_stage: str
    wc_cystine: float
    wc_cystine_date: date
    wc_cystine_time: str
    cysteamine_last_dose: int
    cysteamine_effects: str


class CystinosisAdultVisit(CystinosisAdultVisitBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "cystinosis_adult_visit"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CystinosisAdultVisitCreate(CystinosisAdultVisitBase):
    pass


class CystinosisAdultVisitRead(CystinosisAdultVisitBase):
    id: int


# --- CystinosisPaedVisit --- #


class CystinosisPaedVisitBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    visit: int
    visit_date: date
    height: float
    weight: float
    urine_measurement: str
    urine_output: float
    voiding_overnight: str
    continence_day: str
    fluid_intake: float
    admission_dehydration: int
    constipation: str
    diarrhea: str
    nausea: str
    vomiting: str
    failure_to_thrive: str
    enteral_feeding: str
    feeding_start_date_1: date
    feeding_end_date_1: date
    feeding_start_date_2: date
    feeding_end_date_2: date
    feeding_start_date_3: date
    feeding_end_date_3: date
    normal_food_orally: str
    supplements: str
    growth_hormone_treatment: str
    rickets: str
    kyphoscoliosis: str
    fractures: str
    joint_surgery: str
    muscle_strength: str
    swallowing_difficulties: str
    nose_snoring: str
    tonsillectomy_date: date
    sight_impairment: str
    severe_sight_impairment: str
    photophobia: str
    photophobia_grade: str
    keratoplasty_date: date
    acuity: str
    gahl_score: str
    intraocular_pressure_r: str
    intraocular_pressure_l: str
    fev1: float
    vc: float
    snip: float
    seizure: str
    headache: str
    muscle_weakness: str
    learning_difficulties: str
    cognitive_difficulties: str
    movement_disorder: str
    intracranial_hypertension: str
    diabetes: str
    thyroid: str
    hypothyroidism: str
    tanner_stage: str
    wc_cystine: float
    wc_cystine_date: date
    wc_cystine_time: str
    cysteamine_last_dose: int
    cysteamine_effects: str


class CystinosisPaedVisit(CystinosisPaedVisitBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "cystinosis_paed_visit"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CystinosisPaedVisitCreate(CystinosisPaedVisitBase):
    pass


class CystinosisPaedVisitRead(CystinosisPaedVisitBase):
    id: int


# --- CystinosisPaedVisitOption --- #


class CystinosisPaedVisitOptionBase(SQLModel):
    cystinosis_paeds_visit_id: int = Field(foreign_key="cystinosis_paed_visit.id")
    option_id: int = Field(foreign_key="option.id")


class CystinosisPaedVisitOption(CystinosisPaedVisitOptionBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "cystinosis_paed_visit_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class CystinosisPaedVisitOptionCreate(CystinosisPaedVisitOptionBase):
    pass


class CystinosisPaedVisitOptionRead(CystinosisPaedVisitOptionBase):
    id: int


# --- DataSource --- #


class DataSourceBase(SQLModel):
    data_source_name: str


class DataSource(DataSourceBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "data_source"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceRead(DataSourceBase):
    id: int


# --- Death --- #


class DeathBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    date_of_death: date
    cause_of_death: Optional[str]


class Death(DeathBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "death"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DeathCreate(DeathBase):
    pass


class DeathRead(DeathBase):
    id: int


# --- DentAndLoweAssessment --- #


class DentAndLoweAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    aetiology: str
    causative_agent: str
    other_agent: str
    extra_involvement: str
    other_extra_involvement: str


class DentAndLoweAssessment(DentAndLoweAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "dent_and_lowe_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DentAndLoweAssessmentCreate(DentAndLoweAssessmentBase):
    pass


class DentAndLoweAssessmentRead(DentAndLoweAssessmentBase):
    id: int


# --- DentAndLoweAssessmentOption --- #


class DentAndLoweAssessmentOptionBase(SQLModel):
    dent_and_lowe_assessment_id: int = Field(foreign_key="dent_and_lowe_assessment.id")
    option_id: int = Field(foreign_key="option.id")


class DentAndLoweAssessmentOption(DentAndLoweAssessmentOptionBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "dent_and_lowe_assessment_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DentAndLoweAssessmentOptionCreate(DentAndLoweAssessmentOptionBase):
    pass


class DentAndLoweAssessmentOptionRead(DentAndLoweAssessmentOptionBase):
    id: int


# --- DiabeticComplication --- #


class DiabeticComplicationBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    retinopathy: int
    laser_treatment: bool
    peripheral_neuropathy: bool
    foot_ulcer: bool


class DiabeticComplication(DiabeticComplicationBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "diabetic_complication"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DiabeticComplicationCreate(DiabeticComplicationBase):
    pass


class DiabeticComplicationRead(DiabeticComplicationBase):
    id: int


# --- Diagnoses --- #


class DiagnosisBase(SQLModel):
    diagnosis_name: str


class Diagnosis(DiagnosisBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "diagnosis"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DiagnosisCreate(DiagnosisBase):
    pass


class DiagnosisRead(DiagnosisBase):
    id: int


# --- DiagnosisCode --- #


class DiagnosisCodeBase(SQLModel):
    diagnosis_id: int = Field(foreign_key="diagnosis.id")
    code_id: int = Field(foreign_key="code.id")


class DiagnosisCode(DiagnosisCodeBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "diagnosis_code"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DiagnosisCodeCreate(DiagnosisCodeBase):
    pass


class DiagnosisCodeRead(DiagnosisCodeBase):
    id: int


# --- Dialysis --- #


class DialysisBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    timeline_start: date
    timeline_end: Optional[date]
    modality: int


class Dialysis(DialysisBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "dialysis"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DialysisCreate(DialysisBase):
    pass


class DialysisRead(DialysisBase):
    id: int


# --- Drug --- #


class DrugBase(SQLModel):
    drug_name: str
    drug_group_id: Optional[int] = Field(foreign_key="drug_group.id")


class Drug(DrugBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "drug"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DrugCreate(DrugBase):
    pass


class DrugRead(DrugBase):
    id: int


# --- DrugGroup --- #


class DrugGroupBase(SQLModel):
    drug_group: Optional[str] = Field(unique=True)
    parent_drug_group_id: Optional[int] = Field(foreign_key="drug_group.id")


class DrugGroup(DrugGroupBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "drug_group"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class DrugGroupCreate(DrugGroupBase):
    pass


class DrugGroupRead(DrugGroupBase):
    id: int


# --- EQ5DY --- #


class EQ5DYBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    age: int
    gender: int
    mobility: int
    self_care: int
    usual_activities: int
    pain_discomfort: int
    anxiety_depression: int
    health: int


class EQ5DY(EQ5DYBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "eq_5d_y"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class EQ5DYCreate(EQ5DYBase):
    pass


class EQ5DYRead(EQ5DYBase):
    id: int


# --- EthnicOrigin --- #


class EthnicOriginBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    country_of_birth: str
    year_of_emigration: int
    ethnic_origin: str


class EthnicOrigin(EthnicOriginBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "ethnic_origin"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class EthnicOriginCreate(EthnicOriginBase):
    pass


class EthnicOriginRead(EthnicOriginBase):
    id: int


# --- Ethnicity --- #


class EthnicityBase(SQLModel):
    ethnicity_code: str
    ethnicity_label: str


class Ethnicity(EthnicityBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "ethnicity"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class EthnicityCreate(EthnicityBase):
    pass


class EthnicityRead(EthnicityBase):
    id: int


# --- FamilyHistory --- #


class FamilyHistoryBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    diagnosis_id: int = Field(foreign_key="diagnosis.id")
    relation_patient_id: int = Field(foreign_key="patient.id")
    has_condition: bool


class FamilyHistory(FamilyHistoryBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "family_history"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class FamilyHistoryCreate(FamilyHistoryBase):
    pass


class FamilyHistoryRead(FamilyHistoryBase):
    id: int


# --- FamilyHistoryRelation --- #


class FamilyHistoryRelationBase(SQLModel):
    family_history_id: int = Field(foreign_key="family_history.id")
    relation_id: int = Field(foreign_key="relation.id")


class FamilyHistoryRelation(FamilyHistoryRelationBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "family_history_relation"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class FamilyHistoryRelationCreate(FamilyHistoryRelationBase):
    pass


class FamilyHistoryRelationRead(FamilyHistoryRelationBase):
    id: int


# --- FamilyHistoryRelationPatient --- #


class FamilyHistoryRelationPatientBase(SQLModel):
    family_history_relation_id: int = Field(foreign_key="family_history_relation.id")
    patient_id: int = Field(foreign_key="patient.id")


class FamilyHistoryRelationPatient(FamilyHistoryRelationPatientBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "family_history_relation_patient"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class FamilyHistoryRelationPatientCreate(FamilyHistoryRelationPatientBase):
    pass


class FamilyHistoryRelationPatientRead(FamilyHistoryRelationPatientBase):
    id: int


# --- FetalAnomalyScan --- #


class FetalAnomalyScanBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    date_of_scan: date
    gestational_age: int
    oligohydramnios: bool
    right_anomaly_details: Optional[str]
    right_ultrasound_details: Optional[str]
    left_anomaly_details: Optional[str]
    left_ultrasound_details: Optional[str]
    hypoplasia: Optional[bool]
    echogenicity: Optional[bool]
    hepatic_abnormalities: Optional[bool]
    hepatic_abnormality_details: Optional[str]
    lung_abnormalities: Optional[bool]
    lung_abnormality_details: Optional[str]
    amnioinfusion: Optional[bool]
    amnioinfusion_count: Optional[int]


class FetalAnomalyScan(FetalAnomalyScanBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "fetal_anomaly_scan"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class FetalAnomalyScanCreate(FetalAnomalyScanBase):
    pass


class FetalAnomalyScanRead(FetalAnomalyScanBase):
    id: int


# --- FetalUltrasound --- #


class FetalUltrasoundBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    date_of_scan: date
    fetal_identifier: Optional[str]
    gestational_age: int
    head_centile: Optional[int]
    abdomen_centile: Optional[int]
    uterine_artery_notched: Optional[bool]
    liquor_volume: Optional[str]
    fetal_ultrasound_comment: Optional[str]


class FetalUltrasound(FetalUltrasoundBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "fetal_ultrasound"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class FetalUltrasoundCreate(FetalUltrasoundBase):
    pass


class FetalUltrasoundRead(FetalUltrasoundBase):
    id: int


# --- FuanAssessment --- #


class FuanAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    picture_date: date
    gout: bool
    gout_date: Optional[date]
    family_gout: Optional[bool]
    thp: Optional[str]
    uti: Optional[bool]
    comments: Optional[str]


class FuanAssessment(FuanAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "fuan_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class FuanAssessmentCreate(FuanAssessmentBase):
    pass


class FuanAssessmentRead(FuanAssessmentBase):
    id: int


# --- Genetics --- #


class GeneticsBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    cohort_id: int = Field(foreign_key="cohort.id")
    date_sent: datetime
    laboratory: str
    reference_number: Optional[str]
    karyotype: Optional[int]
    results: Optional[str]
    summary: Optional[str]


class Genetics(GeneticsBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "genetics"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class GeneticsCreate(GeneticsBase):
    pass


class GeneticsRead(GeneticsBase):
    id: int


# --- HADS --- #


class HADSBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    a1: int
    d1: int
    a2: int
    d2: int
    a3: int
    d3: int
    a4: int
    d4: int
    a5: int
    d5: int
    a6: int
    d6: int
    a7: int
    d7: int
    anxiety_score: int


class HADS(HADSBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "hads"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class HADSCreate(HADSBase):
    pass


class HADSRead(HADSBase):
    id: int


# --- Hnf1bAssessment --- #


class Hnf1bAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    date_of_picture: date
    single_kidney: bool
    hyperuricemia_gout: bool
    genital_malformation: bool
    genital_malformation_details: str
    familial_cystic_disease: bool
    hypertension: bool


class Hnf1bAssessment(Hnf1bAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "hnf1b_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class Hnf1bAssessmentCreate(Hnf1bAssessmentBase):
    pass


class Hnf1bAssessmentRead(Hnf1bAssessmentBase):
    id: int


# --- Hospital --- #


class HospitalBase(SQLModel):
    hospital_code: str
    hospital_name: str
    hospital_short_name: str
    is_transplant_centre: bool


class Hospital(HospitalBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "hospital"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class HospitalCreate(HospitalBase):
    pass


class HospitalRead(HospitalBase):
    id: int


# --- HospitalConsultant --- #


class HospitalConsultantBase(SQLModel):
    hospital_id: int = Field(foreign_key="hospital.id")
    consultant_id: int = Field(foreign_key="consultant.id")


class HospitalConsultant(HospitalConsultantBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "hospital_consultant"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class HospitalConsultantCreate(HospitalConsultantBase):
    pass


class HospitalConsultantRead(HospitalConsultantBase):
    id: int


# --- HospitalPatient --- #


class HospitalPatientBase(SQLModel):
    hospital_id: int = Field(foreign_key="hospital.id")
    patient_id: int = Field(foreign_key="patient.id")
    first_seen_date: date
    discharged_date: Optional[date]


class HospitalPatient(HospitalPatientBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "hospital_patient"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class HospitalPatientCreate(HospitalPatientBase):
    pass


class HospitalPatientRead(HospitalPatientBase):
    id: int


# --- Hospitalisation --- #


class HospitalisationBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    date_of_admission: date
    date_of_discharge: Optional[date]
    reason_of_admission: Optional[str]


class Hospitalisation(HospitalisationBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "hospitalisation"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class HospitalisationCreate(HospitalisationBase):
    pass


class HospitalisationRead(HospitalisationBase):
    id: int


# --- HSPAssessment --- #


class HSPAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    haematuria: bool
    nephrotic: bool
    m: str
    e: str
    s: str
    t: str
    c: str


class HSPAssessment(HSPAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "hsp_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class HSPAssessmentCreate(HSPAssessmentBase):
    pass


class HSPAssessmentRead(HSPAssessmentBase):
    id: int


# --- Identifier --- #


class IdentifierBase(SQLModel):
    identifier_label: str


class Identifier(IdentifierBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "identifier"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class IdentifierCreate(IdentifierBase):
    pass


class IdentifierRead(IdentifierBase):
    id: int


# --- IGAResearch --- #


class IGAResearchBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date


class IGAResearch(IGAResearchBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "iga_research"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class IGAResearchCreate(IGAResearchBase):
    pass


class IGAResearchRead(IGAResearchBase):
    id: int


# --- IGAResearchOptions --- #


class IGAResearchOptionsBase(SQLModel):
    IGAResearch_id: int = Field(foreign_key="iga_research.id")
    option_id: int = Field(foreign_key="option.id")


class IGAResearchOptions(IGAResearchOptionsBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "iga_research_options"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class IGAResearchOptionsCreate(IGAResearchOptionsBase):
    pass


class IGAResearchOptionsRead(IGAResearchOptionsBase):
    id: int


# --- Indicator --- #


class IndicatorBase(SQLModel):
    indicator_label: str


class Indicator(IndicatorBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "indicator"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class IndicatorCreate(IndicatorBase):
    pass


class IndicatorRead(IndicatorBase):
    id: int


# --- InsAssessment --- #


class InsAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    date_of_picture: date
    oedema: Optional[bool]
    hypovoloemia: Optional[bool]
    fever: Optional[bool]
    thrombosis: Optional[bool]
    peritonitis: Optional[bool]
    pulmonary_oedema: Optional[bool]
    hypertension: Optional[bool]
    rash: Optional[bool]
    rash_details: Optional[str]
    infection: Optional[bool]
    infection_details: Optional[str]
    ophthalmoscopy: Optional[bool]
    ophthalmoscopy_details: Optional[str]
    comments: Optional[str]


class InsAssessment(InsAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "ins_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class InsAssessmentCreate(InsAssessmentBase):
    pass


class InsAssessmentRead(InsAssessmentBase):
    id: int


# --- InsRelapse --- #


class InsRelapseBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    date_of_relapse: date
    kidney_type: Optional[str]
    viral_trigger: Optional[str]
    immunisation_trigger: Optional[str]
    other_trigger: Optional[str]
    high_dose_oral_prednisolone: Optional[bool]
    iv_methyl_prednisolone: Optional[bool]
    date_of_remission: date
    remission_type: Optional[str]
    peak_acr: Optional[float]
    peak_pcr: Optional[float]
    remission_acr: Optional[float]
    remission_pcr: Optional[float]
    peak_protein_dipstick: Optional[str]
    remission_protein_dipstick: Optional[str]
    relapse_sample_taken: Optional[bool]


class InsRelapse(InsRelapseBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "ins_relapse"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class InsRelapseCreate(InsRelapseBase):
    pass


class InsRelapseRead(InsRelapseBase):
    id: int


# --- IPOS --- #


class IPOSBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    score_1: int
    score_2: int
    score_3: int
    score_4: int
    score_5: int
    score_6: int
    score_7: int
    score_8: int
    score_9: int
    score_10: int
    score_11: int
    score_12: int
    score_13: int
    score_14: int
    score_15: int
    score_16: int
    score_17: int
    question_1: str
    score_18: int
    question_2: str
    score_19: int
    question_3: str
    score_20: int
    question_4: str
    question_5: str
    score: int


class IPOS(IPOSBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "ipos"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class IPOSCreate(IPOSBase):
    pass


class IPOSRead(IPOSBase):
    id: int


# --- LiverDisease --- #


class LiverDiseaseBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    portal_hypertension: Optional[bool]
    portal_hypertension_date: Optional[date]
    ascites: Optional[bool]
    ascites_date: Optional[date]
    oesophageal: Optional[bool]
    oesophageal_date: Optional[date]
    oesophageal_bleeding: Optional[bool]
    oesophageal_bleeding_date: Optional[date]
    gastric: Optional[bool]
    gastric_date: Optional[date]
    gastric_bleeding: Optional[bool]
    gastric_bleeding_date: Optional[date]
    anorectal: Optional[bool]
    anorectal_date: Optional[date]
    anorectal_bleeding: Optional[bool]
    anorectal_bleeding_date: Optional[date]
    cholangitis_acute: Optional[bool]
    cholangitis_acute_date: Optional[date]
    cholangitis_recurrent: Optional[bool]
    cholangitis_recurrent_date: Optional[date]
    spleen_palpable: Optional[bool]
    spleen_palpable_date: Optional[date]


class LiverDisease(LiverDiseaseBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "liver_disease"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class LiverDiseaseCreate(LiverDiseaseBase):
    pass


class LiverDiseaseRead(LiverDiseaseBase):
    id: int


# --- LiverImaging --- #


class LiverImagingBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    imaging_date: date
    imaging_type: str
    liver_size: Optional[float]
    hepatic_fibrosis: Optional[bool]
    hepatic_cysts: Optional[bool]
    bile_duct_cysts: Optional[bool]
    dilated_bile_ducts: Optional[bool]
    cholangitis: Optional[bool]


class LiverImaging(LiverImagingBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "liver_imaging"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class LiverImagingCreate(LiverImagingBase):
    pass


class LiverImagingRead(LiverImagingBase):
    id: int


# --- LiverTransplant --- #


class LiverTransplantBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    transplant_group_id: int = Field(foreign_key="hospital.id")
    registration_date: date
    transplant_date: date
    other_indications: str
    first_graft_source: str
    loss_reason: str
    other_loss_reason: str


class LiverTransplant(LiverTransplantBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "liver_transplant"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class LiverTransplantCreate(LiverTransplantBase):
    pass


class LiverTransplantRead(LiverTransplantBase):
    id: int


# --- LiverTransplantIndicator --- #


class LiverTransplantIndicatorBase(SQLModel):
    liver_transplant_id: int = Field(foreign_key="liver_transplant.id")
    indicator_id: int = Field(foreign_key="indicator.id")


class LiverTransplantIndicator(LiverTransplantIndicatorBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "liver_transplant_indicator"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class LiverTransplantIndicatorCreate(LiverTransplantIndicatorBase):
    pass


class LiverTransplantIndicatorRead(LiverTransplantIndicatorBase):
    id: int


# --- Medication --- #


class MedicationBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    drug_id: int = Field(foreign_key="drug.id")
    snapshot_date: Optional[date]
    start_date: Optional[date]
    finish_date: Optional[date]
    dose_quantity: Optional[float]
    dose_unit: str
    frequency: str
    route: str
    drug_text: str
    dose_text: str


class Medication(MedicationBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "medication"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class MedicationCreate(MedicationBase):
    pass


class MedicationRead(MedicationBase):
    id: int


# --- MpgnAssessment --- #


class MpgnAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    date_of_picture: date
    oedema: bool
    hypertension: bool
    urticaria: bool
    partial_lipodystrophy: bool
    infection: bool
    infection_details: str
    ophthalmoscopy: bool
    ophthalmoscopy_details: str
    comments: str


class MpgnAssessment(MpgnAssessmentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "mpgn_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class MpgnAssessmentCreate(MpgnAssessmentBase):
    pass


class MpgnAssessmentRead(MpgnAssessmentBase):
    id: int


# --- Nationality --- #


class NationalityBase(SQLModel):
    nationality_label: str


class Nationality(NationalityBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "nationality"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class NationalityCreate(NationalityBase):
    pass


class NationalityRead(NationalityBase):
    id: int


# --- Nephrectomy --- #


class NephrectomyBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    assessment_date: date
    kidney_side: str
    kidney_type: str
    entry_type: str


class Nephrectomy(NephrectomyBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "nephrectomy"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class NephrectomyCreate(NephrectomyBase):
    pass


class NephrectomyRead(NephrectomyBase):
    id: int


# --- NurtureFamilyHistory --- #


class NurtureFamilyHistoryBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    eskd: bool
    eskd_relative_1: int
    eskd_relative_2: int
    eskd_relative_3: int
    chd: bool
    chd_relative_1: int
    chd_relative_2: int
    chd_relative_3: int
    diabetes: bool
    diabetes_relative_1: int
    diabetes_relative_2: int
    diabetes_relative_3: int


class NurtureFamilyHistory(NurtureFamilyHistoryBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "nurture_family_history"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class NurtureFamilyHistoryCreate(NurtureFamilyHistoryBase):
    pass


class NurtureFamilyHistoryRead(NurtureFamilyHistoryBase):
    id: int


# --- NurtureMetadata --- #


class NurtureMetadataBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    signed_off_state: int
    follow_up_refused_date: date
    blood_tests: bool
    blood_refused_date: date
    interviews: bool
    interviews_refused_date: date


class NurtureMetadata(NurtureMetadataBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "nurture_metadata"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class NurtureMetadataCreate(NurtureMetadataBase):
    pass


class NurtureMetadataRead(NurtureMetadataBase):
    id: int


# --- NurtureVisit --- #


class NurtureVisitBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    visit_date: date
    visit: int
    comorbidities: int
    vaccination_flu: bool
    vaccination_pneumococcal: bool
    admission: bool
    admission_number: int
    admission_emergency: int
    admission_planned: int
    admission_days: int
    admission_antibiotics: int
    paracetamol_tablets: int
    paracetamol_years: int
    cocodamol_tablets: int
    cocodamol_years: int
    ibuprofen_tablets: int
    ibuprofen_years: int


class NurtureVisit(NurtureVisitBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "nurture_visit"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class NurtureVisitCreate(NurtureVisitBase):
    pass


class NurtureVisitRead(NurtureVisitBase):
    id: int


# --- Nutrition --- #


class NutritionBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    feeding_type: str
    from_date: date
    to_date: date


class Nutrition(NutritionBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "nutrition"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class NutritionCreate(NutritionBase):
    pass


class NutritionRead(NutritionBase):
    id: int


# --- Observation --- #


class ObservationBase(SQLModel):
    sample_type_id: int = Field(foreign_key="sample_type.id")
    name: str
    short_name: str
    min_value: int
    max_value: int
    units: str


class Observation(ObservationBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "observation"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ObservationCreate(ObservationBase):
    pass


class ObservationRead(ObservationBase):
    id: int


# --- ObservationCode --- #


class ObservationCodeBase(SQLModel):
    observation_id: int = Field(foreign_key="observation.id")
    code_id: int = Field(foreign_key="code.id")


class ObservationCode(ObservationCodeBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "observation_code"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ObservationCodeCreate(ObservationCodeBase):
    pass


class ObservationCodeRead(ObservationCodeBase):
    id: int


# --- ObservationOptions --- #


class ObservationOptionsBase(SQLModel):
    observation_id: int
    option_id: int


class ObservationOption(ObservationOptionsBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "observation_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ObservationOptionCreate(ObservationOptionsBase):
    pass


class ObservationOptionRead(ObservationOptionsBase):
    id: int


# --- Option --- #


class OptionBase(SQLModel):
    option_group: str
    display_label: str
    store_value: str


class Option(OptionBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class OptionCreate(OptionBase):
    pass


class OptionRead(OptionBase):
    id: int


# --- PaedsCHU9D --- #


class PaedsCHU9DBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    worried: int
    sad: int
    pain: int
    tired: int
    annoyed: int
    school: int
    sleep: int
    routine: int
    activities: int


class PaedsCHU9D(PaedsCHU9DBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "paeds_chu9d"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PaedsCHU9DCreate(PaedsCHU9DBase):
    pass


class PaedsCHU9DRead(PaedsCHU9DBase):
    id: int


# --- PAM --- #


class PAMBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    q1: int
    q2: int
    q3: int
    q4: int
    q5: int
    q6: int
    q7: int
    q8: int
    q9: int
    q10: int
    q11: int
    q12: int
    q13: int


class PAM(PAMBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "pam"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PAMCreate(PAMBase):
    pass


class PAMRead(PAMBase):
    id: int


# --- ParentalConsanguinity --- #


class ParentalConsanguinityBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    consanguinity: bool
    consanguinity_details: str


class ParentalConsanguinity(ParentalConsanguinityBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "parental_consanguinity"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ParentalConsanguinityCreate(ParentalConsanguinityBase):
    pass


class ParentalConsanguinityRead(ParentalConsanguinityBase):
    id: int


# --- Pathology --- #


class PathologyBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    report_date: date
    kidney_type: str
    kidney_side: str
    reference_number: str
    image_url: str
    histological_summary: str
    em_findings: str
    report_cleaned_date: date


class Pathology(PathologyBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "pathology"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PathologyCreate(PathologyBase):
    pass


class PathologyRead(PathologyBase):
    id: int


# --- Patient --- #


class PatientBase(SQLModel):
    patient_comment: Optional[str]
    is_test: bool = Field(default=False)
    is_control: bool = Field(default=False)


class Patient(PatientBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: int


# --- PatientAddress --- #


class PatientAddressBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    country_id: int = Field(foreign_key="country.id")
    from_date: date
    to_date: date
    address1: str
    address2: str
    address3: str
    address4: str
    postcode: str


class PatientAddress(PatientAddressBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_address"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientAddressCreate(PatientAddressBase):
    pass


class PatientAddressRead(PatientAddressBase):
    id: int


# --- PatientAlias --- #


class PatientAliasBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    first_name: str
    last_name: str


class PatientAlias(PatientAliasBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_alias"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientAliasCreate(PatientAliasBase):
    pass


class PatientAliasRead(PatientAliasBase):
    id: int


# --- PatientConsent --- #


class PatientConsentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    consent_id: int = Field(foreign_key="consent.id")
    signed_on_date: date
    withdrawn_on_date: Optional[date]


class PatientConsent(PatientConsentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_consent"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientConsentCreate(PatientConsentBase):
    pass


class PatientConsentRead(PatientConsentBase):
    id: int


# --- PatientConsultant --- #


class PatientConsultantBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    consultant_id: int = Field(foreign_key="consultant.id")
    from_date: date
    to_date: Optional[date]


class PatientConsultant(PatientConsultantBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_consultant"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientConsultantCreate(PatientConsultantBase):
    pass


class PatientConsultantRead(PatientConsultantBase):
    id: int


# --- PatientDemographic --- #


class PatientDemographicBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    ethnicity_id: int = Field(foreign_key="ethnicity.id")
    country_of_birth: int = Field(foreign_key="country.id")
    first_name: str
    last_name: str
    date_of_birth: date
    gender: int
    mobile_number: str
    email_address: str


class PatientDemographic(PatientDemographicBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_demographic"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientDemographicCreate(PatientDemographicBase):
    pass


class PatientDemographicRead(PatientDemographicBase):
    id: int


# --- PatientDiagnosis --- #


class PatientDiagnosisBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    diagnosis_id: int = Field(foreign_key="diagnosis.id")
    diagnosis_text: str
    symptoms_date: date
    from_date: Optional[date]
    to_date: Optional[date]
    snapshot_date: Optional[date]
    gene_test: bool
    biochemistry: bool
    assessment: bool
    biopsy: bool
    biopsy_diagnosis: int
    comments: str
    prenatal: bool


class PatientDiagnosis(PatientDiagnosisBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_diagnosis"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientDiagnosisCreate(PatientDiagnosisBase):
    pass


class PatientDiagnosisRead(PatientDiagnosisBase):
    id: int


# --- PatientIdentifier --- #


class PatientIdentifierBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    identifier_id: int = Field(foreign_key="identifier.id")
    identifier: str


class PatientIdentifier(PatientIdentifierBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_identifier"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientIdentifierCreate(PatientIdentifierBase):
    pass


class PatientIdentifierRead(PatientIdentifierBase):
    id: int


# --- PatientNationality --- #


class PatientNationalityBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    nationality_id: int = Field(foreign_key="nationality.id")


class PatientNationality(PatientNationalityBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_nationality"
    id: int = Field(default=None, primary_key=True)


class PatientNationalityCreate(PatientNationalityBase):
    pass


class PatientNationalityRead(PatientNationalityBase):
    id: int


# --- PatientReconsent --- #


class PatientReconsentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    sent_date: date
    response_date: date


class PatientReconsent(PatientReconsentBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "patient_reconsent"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PatientReconsentRead(PatientReconsentBase):
    pass


class PatientReconsentCreate(PatientReconsentBase):
    id: int


# --- Plasmapheresis --- #


class PlasmapheresisBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    from_date: date
    to_date: date
    schedule: str
    response: str


class Plasmapheresis(PlasmapheresisBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "plasmapheresis"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PlasmapheresisCreate(PlasmapheresisBase):
    pass


class PlasmapheresisRead(PlasmapheresisBase):
    id: int


# --- Post --- #


class PostBase(SQLModel):
    post_title: str
    published_date: datetime
    body: str


class Post(PostBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "post"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int


# --- Pregnancy --- #


class PregnancyBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    pregnancy_number: int
    date_of_lmp: date
    gravidity: int
    parity1: int
    parity2: int
    outcome: str
    birth_weight: int
    centile_weight: int
    gestational_age: int
    delivery_method: str
    neonatal_intensive_care: bool
    pre_eclampsia: str


class Pregnancy(PregnancyBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "pregnancy"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class PregnancyCreate(PregnancyBase):
    pass


class PregnancyRead(PregnancyBase):
    id: int


# --- Procedure --- #


class ProcedureBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    procedure: str
    other_procedure: str
    date_of_procedure: date


class Procedure(ProcedureBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "procedure"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ProcedureCreate(ProcedureBase):
    pass


class ProcedureRead(ProcedureBase):
    id: int


# --- Relation --- #


class RelationBase(SQLModel):
    relationship: str


class Relation(RelationBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "relation"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RelationCreate(RelationBase):
    pass


class RelationRead(RelationBase):
    id: int


# --- RenalCancerGenetics --- #


class RenalCancerGeneticsBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    bap1_test: bool
    bap1_variant: str
    bap1_variant_status: str
    fh_test: bool
    fh_variant: str
    fh_variant_status: str
    flcn_test: bool
    flcn_variant: str
    flcn_variant_status: str
    met_test: bool
    met_variant: str
    met_variant_status: str
    mitf_test: bool
    mitf_variant: str
    mitf_variant_status: str
    pten_test: bool
    pten_variant: str
    pten_variant_status: str
    sdha_test: bool
    sdha_variant: str
    sdha_variant_status: str
    sdhb_test: bool
    sdhb_variant: str
    sdhb_variant_status: str
    sdhc_test: bool
    sdhc_variant: str
    sdhc_variant_status: str
    sdhd_test: bool
    sdhd_variant: str
    sdhd_variant_status: str
    vhl_test: bool
    vhl_variant: str
    vhl_variant_status: str
    other_test: bool
    other_test_name: str
    other_variant: str
    other_variant_status: str


class RenalCancerGenetics(RenalCancerGeneticsBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "renal_cancer_genetics"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RenalCancerGeneticsCreate(RenalCancerGeneticsBase):
    pass


class RenalCancerGeneticsRead(RenalCancerGeneticsBase):
    id: int


# --- RenalCancerGeneticsOption --- #


class RenalCancerGeneticsOptionBase(SQLModel):
    renal_cancer_genetics_id: int = Field(foreign_key="renal_cancer_genetics.id")
    option_id: int = Field(foreign_key="option.id")


class RenalCancerGeneticsOption(RenalCancerGeneticsOptionBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "renal_cancer_genetics_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RenalCancerGeneticsOptionCreate(RenalCancerGeneticsOptionBase):
    pass


class RenalCancerGeneticsOptionRead(RenalCancerGeneticsOptionBase):
    id: int


# --- RenalCancerTumour --- #


class RenalCancerTumourBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    tumor_type: str
    assessment_date: date
    cns_imaging_method: str  #
    progression_date: date
    t_cat: str
    n_cat: str
    m_cat: str
    rt_size: str
    pt_size: str
    t_loc: str


class RenalCancerTumour(RenalCancerTumourBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "renal_cancer_tumour"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RenalCancerTumourCreate(RenalCancerTumourBase):
    pass


class RenalCancerTumourRead(RenalCancerTumourBase):
    id: int


# --- RenalImaging --- #


class RenalImagingBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    assessment_date: datetime
    imaging_type: str
    right_present: bool
    right_type: str
    right_length: int
    right_volume: int
    right_cysts: bool
    right_stones: bool
    right_calcification: bool
    right_nephrocalcinosis: bool
    right_nephrolithiasis: bool
    right_other_malformation: str
    left_present: bool
    left_type: str
    left_length: int
    left_volume: int
    left_cysts: bool
    left_stones: bool
    left_calcification: bool
    left_nephrocalcinosis: bool
    left_nephrolithiasis: bool
    left_other_malformation: str


class RenalImaging(RenalImagingBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "renal_imaging"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RenalImagingCreate(RenalImagingBase):
    pass


class RenalImagingRead(RenalImagingBase):
    id: int


# --- RenalProgression --- #


class RenalProgressionBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    onset_date: date
    esrf_date: date
    ckd5_date: date
    ckd4_date: date
    ckd3a_date: date
    ckd3b_date: date


class RenalProgression(RenalProgressionBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "renal_progression"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RenalProgressionCreate(RenalProgressionBase):
    pass


class RenalProgressionRead(RenalProgressionBase):
    id: int


# --- Result --- #


class ResultBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    result_date: datetime
    qualifier: str
    result_value: str
    sent_value: str


class Result(ResultBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "result"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class ResultCreate(ResultBase):
    pass


class ResultRead(ResultBase):
    id: int


# --- RituximabBaselineAssessment --- #


class RituximabBaselineAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    assessment_date: date
    nephropathy: str
    steroids: bool
    other_previous_treatment: str
    past_remission: bool
    performance_status: int
    comorbidities: bool


class RituximabBaselineAssessment(RituximabBaselineAssessmentBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "rituximab_baseline_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabBaselineAssessmentCreate(RituximabBaselineAssessmentBase):
    pass


class RituximabBaselineAssessmentRead(RituximabBaselineAssessmentBase):
    id: int


# --- RituximabBaselineAssessmentOption --- #


class RituximabBaselineAssessmentOptionBase(SQLModel):
    rituximab_baseline_assessment_id: int = Field(
        foreign_key="rituximab_baseline_assessment.id"
    )
    option_id: int = Field(foreign_key="option.id")


class RituximabBaselineAssessmentOption(
    RituximabBaselineAssessmentOptionBase, table=True
):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "rituximab_baseline_assessment_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabBaselineAssessmentOptionCreate(RituximabBaselineAssessmentOptionBase):
    pass


class RituximabBaselineAssessmentOptionRead(RituximabBaselineAssessmentOptionBase):
    id: int


# --- RituximabBaselinePreviousTreatment --- #


class RituximabBaselinePreviousTreatmentBase(SQLModel):
    assessment_id: int = Field(foreign_key="rituximab_baseline_assessment.id")
    option_id: int = Field(foreign_key="option.id")
    treatment_start_date: date
    treatment_end_date: Optional[date]


class RituximabBaselinePreviousTreatment(RituximabBaselineAssessmentBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "rituximab_baseline_previous_treatment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabBaselinePreviousTreatmentCreate(RituximabBaselineAssessmentBase):
    pass


class RituximabBaselinePreviousTreatmentRead(RituximabBaselineAssessmentBase):
    id: int


# --- RituximabCriterion --- #


class RituximabCriteriaBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    criteria1: bool
    criteria2: bool
    criteria3: bool
    criteria4: bool
    criteria5: bool
    criteria6: bool
    criteria7: bool
    alkylating_complication: bool
    alkylating_failure_monitoring_requirements: bool
    cancer: bool
    cni_failure_monitoring_requirements: bool
    cni_therapy_complication: bool
    diabetes: bool
    drug_associated_toxicity: bool
    fall_in_egfr: bool
    hypersensitivity: bool
    risk_factors: bool
    ongoing_severe_disease: bool
    threatened_fertility: bool
    mood_disturbance: bool
    osteoporosis_osteopenia: bool
    previous_hospitalization: bool


class RituximabCriteria(RituximabCriteriaBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "rituximab_criteria"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabCriteriaCreate(RituximabCriteriaBase):
    pass


class RituximabCriteriaRead(RituximabCriteriaBase):
    id: int


# --- RituximabFollowUpAssessment --- #


class RituximabFollowUpAssessmentBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    visit_date: date
    visit: str
    performance: str
    transplant: str
    haemodialysis: str
    peritoneal_dialysis: str
    immunosuppression: str
    ciclosporin_administered: date
    tacrolimus_administered: date
    cyclophosphamide_administered: date
    chlorambucil_administered: date
    prednisolone_administered: date
    rituximab_administered: date
    immunosuppression_comments: str


class RituximabFollowUpAssessment(RituximabFollowUpAssessmentBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "rituximab_follow_up_assessment"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabFollowUpAssessmentCreate(RituximabFollowUpAssessmentBase):
    pass


class RituximabFollowUpAssessmentRead(RituximabFollowUpAssessmentBase):
    id: int


# --- RituximabFollowUpAssessmentOption --- #


class RituximabFollowUpAssessmentOptionBase(SQLModel):
    rituximab_follow_up_assessment_id: int = Field(
        foreign_key="rituximab_follow_up_assessment.id"
    )
    option_id: int = Field(foreign_key="option.id")


class RituximabFollowUpAssessmentOption(
    RituximabFollowUpAssessmentOptionBase, table=True
):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "rituximab_follow_up_assessment_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabFollowUpAssessmentOptionCreate(RituximabFollowUpAssessmentOptionBase):
    pass


class RituximabFollowUpAssessmentOptionRead(RituximabFollowUpAssessmentOptionBase):
    id: int


# --- RituximabToxicity --- #


class RituximabToxicityBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    drug_name: str
    other_drug: str
    dose: Optional[float]
    retreatment: str
    toxicity: Optional[str]
    other_toxicity: Optional[str]


class RituximabToxicity(RituximabToxicityBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "rituximab_toxicity"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabToxicityCreate(RituximabToxicityBase):
    pass


class RituximabToxicityRead(RituximabToxicityBase):
    id: int


# --- RituximabToxicityOption --- #


class RituximabToxicityOptionBase(SQLModel):
    rituximab_toxicity_id: int = Field(foreign_key="rituximab_toxicity.id")
    option_id: int = Field(foreign_key="option.id")


class RituximabToxicityOption(RituximabToxicityOptionBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "rituximab_toxicity_option"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class RituximabToxicityOptionCreate(RituximabToxicityOptionBase):
    pass


class RituximabToxicityOptionRead(RituximabToxicityOptionBase):
    id: int


# --- SaltWastingClinicalFeature --- #


class SaltWastingClinicalFeatureBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    normal_pregnancy: bool
    abnormal_pregnancy_text: str
    neurological_problems: bool
    seizures: bool
    abnormal_gait: bool
    deafness: bool
    other_neurological_problem: bool
    other_neurological_problem_text: str
    joint_problems: bool
    joint_problems_age: int
    x_ray_abnormalities: bool
    chondrocalcinosis: bool
    other_x_ray_abnormality: bool
    other_x_ray_abnormality_text: str


class SaltWastingClinicalFeature(SaltWastingClinicalFeatureBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "salt_wasting_clinical_feature"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class SaltWastingClinicalFeatureCreate(SaltWastingClinicalFeatureBase):
    pass


class SaltWastingClinicalFeatureRead(SaltWastingClinicalFeatureBase):
    id: int


# --- SampleInventory --- #


class SampleInventoryBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    sample_date: date
    urine: bool
    urine_date: date
    urine_volume: str
    serum: bool
    serum_date: date
    serum_volume: str
    plasma: bool
    plasma_date: date
    plasma_volume: str
    dna: bool
    dna_date: date
    sputum: bool
    sputum_date: date
    faeces: bool
    faeces_date: date


class SampleInventory(SampleInventoryBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "sample_inventory"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class SampleInventoryCreate(SampleInventoryBase):
    pass


class SampleInventoryRead(SampleInventoryBase):
    id: int


# --- SampleType --- #


class SampleTypeBase(SQLModel):
    sample_type_label: str = Field(unique=True)


class SampleType(SampleTypeBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "sample_type"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class SampleTypeCreate(SampleTypeBase):
    pass


class SampleTypeRead(SampleTypeBase):
    id: int


# --- sixCIT --- #


class SixCITBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    completed_date: date
    q1: int
    q2: int
    q3: int
    q4: int
    q5: int
    q6: int
    q7: int
    score: int


class SixCIT(SixCITBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "six_cit"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class SixCITCreate(SixCITBase):
    pass


class SixCITRead(SixCITBase):
    id: int


# --- SocioEconomic --- #


class SocioEconomicBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    assessment_date: date
    education: int
    employment_status: int
    first_language: str
    martial_status: str
    smoking: int
    cigarettes_per_day: int
    alcohol: bool
    beer_pints: int
    cider_pints: int
    red_wine: int
    white_wine: int
    spirits: int
    cocktails: int
    units_per_week: int
    literacy: int
    literacy_help: str
    diet: int
    other_diet: str


class SocioEconomic(SocioEconomicBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "socioeconomic"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class SocioEconomicCreate(SocioEconomicBase):
    pass


class SocioEconomicRead(SocioEconomicBase):
    id: int


# --- Specialty --- #


class SpecialtyBase(SQLModel):
    specialty: str = Field(unique=True)


class Specialty(SpecialtyBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "specialty"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class SpecialtyCreate(SpecialtyBase):
    pass


class SpecialtyRead(SpecialtyBase):
    id: int


# --- Transplant --- #


class TransplantBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    hospital_id: int = Field(foreign_key="hospital.id")
    transplant_hospital_id: int = Field(foreign_key="hospital.id")
    data_source_id: int = Field(foreign_key="data_source.id")
    transplant_date: date
    modality: int
    date_of_recurrence: date
    date_of_failure: date
    recurrence: bool
    date_of_cmv_infection: date
    donor_hla: str
    recipient_hla: str
    graft_loss_cause: str


class Transplant(TransplantBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "transplant"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class TransplantCreate(TransplantBase):
    pass


class TransplantRead(TransplantBase):
    id: int


# --- TransplantBiopsy --- #


class TransplantBiopsyBase(SQLModel):
    transplant_id: int = Field(foreign_key="transplant.id")
    biopsy_date: date
    recurrence: bool


class TransplantBiopsy(TransplantBiopsyBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "transplant_biopsy"
    id: int = Field(default=None, primary_key=True)


class TransplantBiopsyCreate(TransplantBiopsyBase):
    pass


class TransplantBiopsyRead(TransplantBiopsyBase):
    id: int


# --- TransplantRejection --- #


class TransplantRejectionBase(SQLModel):
    transplant_id: int = Field(foreign_key="transplant.id")
    rejection_date: date


class TransplantRejection(TransplantRejectionBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "transplant_rejection"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class TransplantRejectionCreate(TransplantRejectionBase):
    pass


class TransplantRejectionRead(TransplantRejectionBase):
    id: int


# --- TubeSample --- #


class TubeSampleBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    sample_date: date
    barcode: str
    ins_state: int


class TubeSample(TubeSampleBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "tube_sample"
    id: Optional[int] = Field(sa_column=Column(BigInteger(), primary_key=True))


class TubeSampleCreate(TubeSampleBase):
    pass


class TubeSampleRead(TubeSampleBase):
    id: int
