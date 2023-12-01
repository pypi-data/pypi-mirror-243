# coding: utf-8
from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Biomarker(Base):
    __tablename__ = "biomarkers"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarkers_id_seq'::regclass)"),
    )
    name = Column(String(100), nullable=False)
    type = Column(String(100))


class Code(Base):
    __tablename__ = "codes"
    __table_args__ = (
        CheckConstraint(
            "(((system)::text = 'ICD-10'::text) AND ((code)::text ~ similar_escape('[A-Z][0-9][0-9](\\.[0-9])?'::text, NULL::text))) OR (((system)::text = 'SNOMED CT'::text) AND ((code)::text ~ similar_escape('[1-9][0-9]*'::text, NULL::text))) OR (((system)::text = 'ERA-EDTA PRD'::text) AND ((code)::text ~ similar_escape('[1-9][0-9]*'::text, NULL::text)))"
        ),
        Index("codes_system_code_idx", "system", "code", unique=True),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('codes_id_seq'::regclass)"),
    )
    system = Column(String, nullable=False)
    code = Column(String, nullable=False)
    display = Column(String, nullable=False)


class Consent(Base):
    __tablename__ = "consents"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('consents_id_seq'::regclass)"),
    )
    code = Column(String(50), nullable=False)
    label = Column(String)
    paediatric = Column(Boolean, server_default=text("false"))
    from_date = Column(Date, nullable=False)
    link_url = Column(String)
    retired = Column(Boolean, server_default=text("false"))
    consent_type = Column(
        Enum("FORM", "INFORMATION_SHEET", name="consent_type_type"), nullable=False
    )
    weight = Column(Integer)


class Country(Base):
    __tablename__ = "countries"

    code = Column(String(2), primary_key=True)
    label = Column(String(100), nullable=False)


t_cthree = Table("cthree", metadata, Column("id", Integer))


class Diagnose(Base):
    __tablename__ = "diagnoses"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('diagnoses_id_seq'::regclass)"),
    )
    name = Column(String, nullable=False)
    retired = Column(Boolean, nullable=False, server_default=text("false"))


class DrugGroup(Base):
    __tablename__ = "drug_groups"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('drug_groups_id_seq'::regclass)"),
    )
    name = Column(String, nullable=False, unique=True)
    parent_drug_group_id = Column(ForeignKey("drug_groups.id"))

    parent_drug_group = relationship("DrugGroup", remote_side=[id])


class Ethnicity(Base):
    __tablename__ = "ethnicities"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('ethnicities_id_seq'::regclass)"),
    )
    code = Column(String(10))
    label = Column(String)


class Form(Base):
    __tablename__ = "forms"
    __table_args__ = (
        CheckConstraint(
            "(slug)::text ~ similar_escape('([a-z0-9]+-)*[a-z0-9]+'::text, NULL::text)"
        ),
        {"comment": "data definitions for forms"},
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('forms_id_seq'::regclass)"),
    )
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    data = Column(JSONB(astext_type=Text()), nullable=False)


class Log(Base):
    __tablename__ = "logs"
    __table_args__ = (
        Index("logs_user_type_idx", "user_id", "type"),
        Index("logs_user_date_idx", "user_id", "date"),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('logs_id_seq'::regclass)"),
    )
    date = Column(
        DateTime(True), nullable=False, index=True, server_default=text("now()")
    )
    type = Column(String, nullable=False, index=True)
    user_id = Column(Integer, index=True)
    data = Column(JSONB(astext_type=Text()))


t_mpgn = Table("mpgn", metadata, Column("patient_id", Integer))


class Nationality(Base):
    __tablename__ = "nationalities"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('nationalities_id_seq'::regclass)"),
    )
    label = Column(String)


class NurtureSamplesBlood(Base):
    __tablename__ = "nurture_samples_blood"

    sample_id = Column(String(20), primary_key=True)
    sample_date = Column(DateTime, nullable=False)
    radar_id = Column(String(20), nullable=False)
    bnp = Column(String(10))
    creat = Column(String(10))
    crp = Column(String(10))
    cyst = Column(String(10))
    gdf15 = Column(String(10))
    trop = Column(String(10))
    ins_state = Column(Integer)
    comments_label = Column(String(50))
    comments_sample = Column(String(50))


class NurtureSamplesOption(Base):
    __tablename__ = "nurture_samples_options"

    id = Column(
        Enum(
            "ADULT_NS",
            "ADULT_CKD",
            "CHILDREN15_2ND",
            "CHILDREN15_B",
            "CHILDREN_LESS_15_2ND",
            "CHILDREN_LESS_15_B",
            "CHILDREN30_2ND",
            "CHILDREN30_B",
            name="protocol_option_type",
        ),
        primary_key=True,
        unique=True,
    )
    label = Column(String, nullable=False)
    epa = Column(Integer)
    epb = Column(Integer)
    lpa = Column(Integer)
    lpb = Column(Integer)
    uc = Column(Integer)
    ub = Column(Integer)
    ud = Column(Integer)
    fub = Column(Integer)
    sc = Column(Integer)
    sa = Column(Integer)
    sb = Column(Integer)
    rna = Column(Integer)
    wb = Column(Integer)


class NurtureSamplesUrine(Base):
    __tablename__ = "nurture_samples_urine"

    sample_id = Column(String(20), primary_key=True)
    sample_date = Column(DateTime, nullable=False)
    radar_id = Column(String(20), nullable=False)
    albumin = Column(String(10))
    creatinin = Column(String(10))
    ins_state = Column(Integer)
    comments_label = Column(String(50))
    comments_sample = Column(String(50))


class Observation(Base):
    __tablename__ = "observations"
    __table_args__ = (
        CheckConstraint(
            "((value_type = 'ENUM'::observation_value_type) AND (options IS NOT NULL)) OR ((value_type <> 'ENUM'::observation_value_type) AND (options IS NULL))"
        ),
        CheckConstraint("(max_length IS NULL) OR (max_length > 0)"),
        CheckConstraint(
            "(max_length IS NULL) OR (value_type = 'STRING'::observation_value_type)"
        ),
        CheckConstraint(
            "(max_value IS NULL) OR (value_type = ANY (ARRAY['REAL'::observation_value_type, 'INTEGER'::observation_value_type]))"
        ),
        CheckConstraint(
            "(min_length IS NULL) OR (max_length IS NULL) OR (max_length >= min_length)"
        ),
        CheckConstraint("(min_length IS NULL) OR (min_length > 0)"),
        CheckConstraint(
            "(min_length IS NULL) OR (value_type = 'STRING'::observation_value_type)"
        ),
        CheckConstraint(
            "(min_value IS NULL) OR (max_value IS NULL) OR (max_value >= min_value)"
        ),
        CheckConstraint(
            "(min_value IS NULL) OR (value_type = ANY (ARRAY['REAL'::observation_value_type, 'INTEGER'::observation_value_type]))"
        ),
        CheckConstraint(
            "(options IS NULL) OR ((COALESCE(array_length(options, 1), 0) > 0) AND ((array_length(options, 1) %% 2) = 0))"
        ),
        CheckConstraint("(units IS NULL) OR (units <> ''::text)"),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('observations_id_seq'::regclass)"),
    )
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    value_type = Column(
        Enum("ENUM", "INTEGER", "REAL", "STRING", name="observation_value_type"),
        nullable=False,
    )
    sample_type = Column(
        Enum(
            "BLOOD",
            "OBSERVATION",
            "URINE",
            "URINE_DIPSTICK",
            name="observation_sample_type",
        ),
        nullable=False,
    )
    pv_code = Column(String)
    min_value = Column(Numeric)
    max_value = Column(Numeric)
    min_length = Column(Integer)
    max_length = Column(Integer)
    units = Column(Text)
    options = Column(ARRAY(Text()))


class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('specialties_id_seq'::regclass)"),
    )
    name = Column(String, nullable=False, unique=True)


t_tracing_export = Table(
    "tracing_export",
    metadata,
    Column("id", Integer),
    Column("nhs", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("date_of_birth", Date),
    Column("gender", Integer),
    Column("address1", String),
    Column("address2", String),
    Column("address3", String),
    Column("postcode", String),
    Column("chi", String),
)


t_ukrdc_patients = Table("ukrdc_patients", metadata, Column("id", Integer))


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('users_id_seq'::regclass)"),
    )
    username = Column(String, nullable=False, index=True)
    password = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    telephone_number = Column(String)
    is_admin = Column(Boolean, nullable=False, server_default=text("false"))
    is_bot = Column(Boolean, nullable=False, server_default=text("false"))
    is_enabled = Column(Boolean, nullable=False, server_default=text("true"))
    reset_password_token = Column(String)
    reset_password_date = Column(DateTime)
    force_password_change = Column(
        Boolean, nullable=False, server_default=text("false")
    )
    created_user_id = Column(ForeignKey("users.id"))
    modified_user_id = Column(ForeignKey("users.id"))
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", remote_side=[id], primaryjoin="User.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", remote_side=[id], primaryjoin="User.modified_user_id == User.id"
    )


t_vbase = Table(
    "vbase",
    metadata,
    Column("patient_id", Integer),
    Column("date_of_birth", Date),
    Column("ethnicity", Text),
    Column("year_of_birth", Float(53)),
    Column("gender", Text),
    Column("first_name", Text),
    Column("last_name", Text),
)


t_vbase_hnf1b = Table("vbase_hnf1b", metadata, Column("patient_id", Integer))


t_vcomorbs = Table(
    "vcomorbs",
    metadata,
    Column("patient_id", Integer),
    Column("from_date", Date),
    Column("to_date", Date),
    Column("symptoms_date", Date),
    Column("diag", String),
)


t_vdiags = Table(
    "vdiags",
    metadata,
    Column("patient_id", Integer),
    Column("name", String),
    Column("primary_diagnosis", String),
    Column("primary_diag_id", Integer),
    Column("age_at_diag", Float(53)),
    Column("symptoms_date", Date),
    Column("diagnosis_date", Date),
    Column("biopsy_comments", Text),
)


t_vfam_hist = Table(
    "vfam_hist",
    metadata,
    Column("patient_id", Integer),
    Column("parental_consanguinity", Text),
    Column("family_history_cohort_diag", Text),
    Column("other_family_history", Text),
    Column("relatives_affected", ARRAY(Text())),
    Column("fh_chd", Text),
    Column("fh_eskd", Text),
    Column("fh_diabetes", Text),
)


t_vgenetics = Table(
    "vgenetics",
    metadata,
    Column("patient_id", Integer),
    Column("genetics_results", ARRAY(Text())),
)


t_vlabs = Table(
    "vlabs",
    metadata,
    Column("patient_id", Integer),
    Column("test", String),
    Column("date", DateTime(True)),
    Column("sent_value", String),
    Column("units", Text),
)


t_vlong_meds = Table(
    "vlong_meds",
    metadata,
    Column("patient_id", Integer),
    Column("med_data", Text),
    Column("name", String),
    Column("from_date", Date),
    Column("to_date", Date),
    Column("dose_quantity", Numeric),
    Column("dose_unit", String),
    Column("route", String),
    Column("frequency", String),
)


t_vmeds = Table(
    "vmeds", metadata, Column("patient_id", Integer), Column("meds", ARRAY(Text()))
)


t_vpath = Table(
    "vpath",
    metadata,
    Column("patient_id", Integer),
    Column("date", Date),
    Column("kidney_type", String),
    Column("kidney_side", String),
    Column("histological_summary", Text),
    Column("em_findings", Text),
)


t_vtrans = Table(
    "vtrans",
    metadata,
    Column("patient_id", Integer),
    Column("transplant_date", Text),
    Column("type", Text),
    Column("recur_date", Text),
    Column("fail_date", Text),
)


class Consultant(Base):
    __tablename__ = "consultants"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('consultants_id_seq'::regclass)"),
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    telephone_number = Column(String)
    gmc_number = Column(Integer, unique=True)
    specialty_id = Column(ForeignKey("specialties.id"), nullable=False)

    specialty = relationship("Specialty")


class CountryEthnicity(Base):
    __tablename__ = "country_ethnicities"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('country_ethnicities_id_seq'::regclass)"),
    )
    ethnicity_id = Column(ForeignKey("ethnicities.id"))
    country_code = Column(ForeignKey("countries.code"))

    country = relationship("Country")
    ethnicity = relationship("Ethnicity")


class CountryNationality(Base):
    __tablename__ = "country_nationalities"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('country_nationalities_id_seq'::regclass)"),
    )
    nationality_id = Column(ForeignKey("nationalities.id"))
    country_code = Column(ForeignKey("countries.code"))

    country = relationship("Country")
    nationality = relationship("Nationality")


class DiagnosisCode(Base):
    __tablename__ = "diagnosis_codes"
    __table_args__ = (
        Index(
            "diagnosis_codes_diagnosis_code_idx", "diagnosis_id", "code_id", unique=True
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('diagnosis_codes_id_seq'::regclass)"),
    )
    diagnosis_id = Column(
        ForeignKey("diagnoses.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    code_id = Column(
        ForeignKey("codes.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )

    code = relationship("Code")
    diagnosis = relationship("Diagnose")


class Drug(Base):
    __tablename__ = "drugs"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('drugs_id_seq'::regclass)"),
    )
    name = Column(String, nullable=False, unique=True)
    drug_group_id = Column(ForeignKey("drug_groups.id"))

    drug_group = relationship("DrugGroup")


class Group(Base):
    __tablename__ = "groups"
    __table_args__ = (
        CheckConstraint(
            "(type <> 'COHORT'::group_type) OR (parent_group_id IS NOT NULL)"
        ),
        Index("groups_code_type_idx", "code", "type", unique=True),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('groups_id_seq'::regclass)"),
    )
    type = Column(
        Enum("COHORT", "HOSPITAL", "OTHER", "SYSTEM", name="group_type"), nullable=False
    )
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    instructions = Column(String)
    multiple_diagnoses = Column(Boolean, nullable=False, server_default=text("false"))
    is_recruitment_number_group = Column(
        Boolean, nullable=False, server_default=text("false")
    )
    parent_group_id = Column(ForeignKey("groups.id"))
    is_transplant_centre = Column(Boolean, server_default=text("false"))
    country_code = Column(ForeignKey("countries.code"))

    country = relationship("Country")
    parent_group = relationship("Group", remote_side=[id])


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    comments = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    test = Column(Boolean, nullable=False, server_default=text("false"))
    control = Column(Boolean, nullable=False, server_default=text("false"))

    created_user = relationship(
        "User", primaryjoin="Patient.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Patient.modified_user_id == User.id"
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('posts_id_seq'::regclass)"),
    )
    title = Column(Text, nullable=False)
    published_date = Column(DateTime(True), nullable=False)
    body = Column(Text, nullable=False)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship("User", primaryjoin="Post.created_user_id == User.id")
    modified_user = relationship("User", primaryjoin="Post.modified_user_id == User.id")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('user_sessions_id_seq'::regclass)"),
    )
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date = Column(DateTime(True), nullable=False)
    ip_address = Column(INET, nullable=False)
    user_agent = Column(String)

    user = relationship("User")


class AlportClinicalPicture(Base):
    __tablename__ = "alport_clinical_pictures"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date_of_picture = Column(Date, nullable=False)
    deafness = Column(Integer, nullable=False)
    deafness_date = Column(Date)
    hearing_aid_date = Column(Date)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="AlportClinicalPicture.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="AlportClinicalPicture.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class BiomarkerBarcode(Base):
    __tablename__ = "biomarker_barcodes"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarker_barcodes_id_seq'::regclass)"),
    )
    pat_id = Column(ForeignKey("patients.id"))
    barcode = Column(String(100))
    sample_date = Column(DateTime)

    pat = relationship("Patient")


class CurrentMedication(Base):
    __tablename__ = "current_medications"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date_recorded = Column(Date, nullable=False)
    drug_id = Column(ForeignKey("drugs.id"))
    dose_quantity = Column(Numeric)
    dose_unit = Column(String)
    frequency = Column(String)
    route = Column(String)
    drug_text = Column(String)
    dose_text = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="CurrentMedication.created_user_id == User.id"
    )
    drug = relationship("Drug")
    modified_user = relationship(
        "User", primaryjoin="CurrentMedication.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class Dialysi(Base):
    __tablename__ = "dialysis"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    modality = Column(Integer, nullable=False)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Dialysi.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Dialysi.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class Entry(Base):
    __tablename__ = "entries"
    __table_args__ = {"comment": "data entered via specific form definitions"}

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    form_id = Column(ForeignKey("forms.id"), nullable=False)
    data = Column(JSONB(astext_type=Text()), nullable=False)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship("User", primaryjoin="Entry.created_user_id == User.id")
    form = relationship("Form")
    modified_user = relationship(
        "User", primaryjoin="Entry.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class FamilyHistory(Base):
    __tablename__ = "family_histories"
    __table_args__ = (
        Index(
            "family_histories_patient_group_idx", "patient_id", "group_id", unique=True
        ),
    )

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    parental_consanguinity = Column(Boolean)
    family_history = Column(Boolean)
    other_family_history = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="FamilyHistory.created_user_id == User.id"
    )
    group = relationship("Group")
    modified_user = relationship(
        "User", primaryjoin="FamilyHistory.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class FetalAnomalyScan(Base):
    __tablename__ = "fetal_anomaly_scans"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date_of_scan = Column(Date, nullable=False)
    gestational_age = Column(Integer, nullable=False)
    oligohydramnios = Column(Boolean)
    right_anomaly_details = Column(String)
    right_ultrasound_details = Column(String)
    left_anomaly_details = Column(String)
    left_ultrasound_details = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    hypoplasia = Column(Boolean)
    echogenicity = Column(Boolean)
    hepatic_abnormalities = Column(Boolean)
    hepatic_abnormality_details = Column(String)
    lung_abnormalities = Column(Boolean)
    lung_abnormality_details = Column(String)
    amnioinfusion = Column(Boolean)
    amnioinfusion_count = Column(Integer)

    created_user = relationship(
        "User", primaryjoin="FetalAnomalyScan.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="FetalAnomalyScan.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class FetalUltrasound(Base):
    __tablename__ = "fetal_ultrasounds"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date_of_scan = Column(Date, nullable=False)
    fetal_identifier = Column(String)
    gestational_age = Column(Integer)
    head_centile = Column(Integer)
    abdomen_centile = Column(Integer)
    uterine_artery_notched = Column(Boolean)
    liquor_volume = Column(String)
    comments = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="FetalUltrasound.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="FetalUltrasound.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class FuanClinicalPicture(Base):
    __tablename__ = "fuan_clinical_pictures"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    picture_date = Column(Date, nullable=False)
    gout = Column(Boolean)
    gout_date = Column(Date)
    family_gout = Column(Boolean)
    family_gout_relatives = Column(ARRAY(Integer()))
    thp = Column(String)
    uti = Column(Boolean)
    comments = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="FuanClinicalPicture.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="FuanClinicalPicture.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class Genetic(Base):
    __tablename__ = "genetics"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    date_sent = Column(DateTime(True), nullable=False)
    laboratory = Column(String)
    reference_number = Column(String)
    karyotype = Column(Integer)
    results = Column(Text)
    summary = Column(Text)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Genetic.created_user_id == User.id"
    )
    group = relationship("Group")
    modified_user = relationship(
        "User", primaryjoin="Genetic.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class GroupConsultant(Base):
    __tablename__ = "group_consultants"
    __table_args__ = (
        Index(
            "group_consultants_group_consultant_idx",
            "group_id",
            "consultant_id",
            unique=True,
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_consultants_id_seq'::regclass)"),
    )
    group_id = Column(ForeignKey("groups.id"), nullable=False)
    consultant_id = Column(
        ForeignKey("consultants.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    consultant = relationship("Consultant")
    group = relationship("Group")


class GroupDiagnose(Base):
    __tablename__ = "group_diagnoses"
    __table_args__ = (
        CheckConstraint("weight >= 0"),
        Index(
            "group_diagnoses_diagnosis_group_idx",
            "diagnosis_id",
            "group_id",
            unique=True,
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_diagnoses_id_seq'::regclass)"),
    )
    group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    diagnosis_id = Column(
        ForeignKey("diagnoses.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    type = Column(
        Enum("PRIMARY", "SECONDARY", name="group_diagnosis_type"), nullable=False
    )
    weight = Column(Integer, nullable=False, server_default=text("9999"))

    diagnosis = relationship("Diagnose")
    group = relationship("Group")


class GroupForm(Base):
    __tablename__ = "group_forms"
    __table_args__ = (
        CheckConstraint("weight >= 0"),
        Index("group_forms_form_group_idx", "form_id", "group_id", unique=True),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_forms_id_seq'::regclass)"),
    )
    group_id = Column(
        ForeignKey("groups.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    form_id = Column(
        ForeignKey("forms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    weight = Column(Integer, nullable=False)

    form = relationship("Form")
    group = relationship("Group")


class GroupObservation(Base):
    __tablename__ = "group_observations"
    __table_args__ = (
        Index(
            "group_observations_observation_group_idx",
            "observation_id",
            "group_id",
            unique=True,
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_observations_id_seq'::regclass)"),
    )
    group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    observation_id = Column(ForeignKey("observations.id"), nullable=False, index=True)
    weight = Column(Integer)

    group = relationship("Group")
    observation = relationship("Observation")


class GroupPage(Base):
    __tablename__ = "group_pages"
    __table_args__ = (
        CheckConstraint("weight >= 0"),
        Index("group_pages_page_group_idx", "page", "group_id", unique=True),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_pages_id_seq'::regclass)"),
    )
    group_id = Column(
        ForeignKey("groups.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    page = Column(String, nullable=False, index=True)
    weight = Column(Integer, nullable=False)

    group = relationship("Group")


class GroupPatient(Base):
    __tablename__ = "group_patients"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_patients_id_seq'::regclass)"),
    )
    group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    from_date = Column(DateTime(True), nullable=False)
    to_date = Column(DateTime(True))
    created_group_id = Column(ForeignKey("groups.id"), nullable=False)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    discharged_date = Column(Date)

    created_group = relationship(
        "Group", primaryjoin="GroupPatient.created_group_id == Group.id"
    )
    created_user = relationship(
        "User", primaryjoin="GroupPatient.created_user_id == User.id"
    )
    group = relationship("Group", primaryjoin="GroupPatient.group_id == Group.id")
    modified_user = relationship(
        "User", primaryjoin="GroupPatient.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class GroupQuestionnaire(Base):
    __tablename__ = "group_questionnaires"
    __table_args__ = (
        CheckConstraint("weight >= 0"),
        Index(
            "group_questionnaires_form_group_idx", "form_id", "group_id", unique=True
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_questionnaires_id_seq'::regclass)"),
    )
    group_id = Column(
        ForeignKey("groups.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    form_id = Column(
        ForeignKey("forms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    weight = Column(Integer, nullable=False)

    form = relationship("Form")
    group = relationship("Group")


class GroupUser(Base):
    __tablename__ = "group_users"
    __table_args__ = (
        Index(
            "group_patients_group_user_role_idx",
            "group_id",
            "user_id",
            "role",
            unique=True,
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('group_users_id_seq'::regclass)"),
    )
    group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(
        Enum(
            "ADMIN",
            "CLINICIAN",
            "IT",
            "RESEARCHER",
            "SENIOR_CLINICIAN",
            "SENIOR_RESEARCHER",
            name="role",
        ),
        nullable=False,
    )
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="GroupUser.created_user_id == User.id"
    )
    group = relationship("Group")
    modified_user = relationship(
        "User", primaryjoin="GroupUser.modified_user_id == User.id"
    )
    user = relationship("User", primaryjoin="GroupUser.user_id == User.id")


class Hnf1bClinicalPicture(Base):
    __tablename__ = "hnf1b_clinical_pictures"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date_of_picture = Column(Date, nullable=False)
    single_kidney = Column(Boolean)
    hyperuricemia_gout = Column(Boolean)
    genital_malformation = Column(Boolean)
    genital_malformation_details = Column(String)
    familial_cystic_disease = Column(Boolean)
    hypertension = Column(Boolean)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Hnf1bClinicalPicture.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Hnf1bClinicalPicture.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class Hospitalisation(Base):
    __tablename__ = "hospitalisations"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date_of_admission = Column(DateTime(True), nullable=False)
    date_of_discharge = Column(DateTime(True))
    reason_for_admission = Column(Text)
    comments = Column(Text)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Hospitalisation.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Hospitalisation.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class IndiaEthnicity(Base):
    __tablename__ = "india_ethnicities"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    father_ancestral_state = Column(String)
    father_language = Column(String)
    mother_ancestral_state = Column(String)
    mother_language = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="IndiaEthnicity.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="IndiaEthnicity.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class InsClinicalPicture(Base):
    __tablename__ = "ins_clinical_pictures"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date_of_picture = Column(Date, nullable=False)
    oedema = Column(Boolean)
    hypovalaemia = Column(Boolean)
    fever = Column(Boolean)
    thrombosis = Column(Boolean)
    peritonitis = Column(Boolean)
    pulmonary_odemea = Column(Boolean)
    hypertension = Column(Boolean)
    rash = Column(Boolean)
    rash_details = Column(String)
    infection = Column(Boolean)
    infection_details = Column(String)
    ophthalmoscopy = Column(Boolean)
    ophthalmoscopy_details = Column(String)
    comments = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="InsClinicalPicture.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="InsClinicalPicture.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class InsRelapse(Base):
    __tablename__ = "ins_relapses"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date_of_relapse = Column(Date, nullable=False)
    kidney_type = Column(String)
    viral_trigger = Column(String)
    immunisation_trigger = Column(String)
    other_trigger = Column(String)
    high_dose_oral_prednisolone = Column(Boolean)
    iv_methyl_prednisolone = Column(Boolean)
    date_of_remission = Column(Date)
    remission_type = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    peak_acr = Column(Float(53))
    peak_pcr = Column(Float(53))
    remission_acr = Column(Float(53))
    remission_pcr = Column(Float(53))
    peak_protein_dipstick = Column(String)
    remission_protein_dipstick = Column(String)
    relapse_sample_taken = Column(Boolean)

    created_user = relationship(
        "User", primaryjoin="InsRelapse.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="InsRelapse.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class LiverDisease(Base):
    __tablename__ = "liver_diseases"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    portal_hypertension = Column(Boolean)
    portal_hypertension_date = Column(Date)
    ascites = Column(Boolean)
    ascites_date = Column(Date)
    oesophageal = Column(Boolean)
    oesophageal_date = Column(Date)
    oesophageal_bleeding = Column(Boolean)
    oesophageal_bleeding_date = Column(Date)
    gastric = Column(Boolean)
    gastric_date = Column(Date)
    gastric_bleeding = Column(Boolean)
    gastric_bleeding_date = Column(Date)
    anorectal = Column(Boolean)
    anorectal_date = Column(Date)
    anorectal_bleeding = Column(Boolean)
    anorectal_bleeding_date = Column(Date)
    cholangitis_acute = Column(Boolean)
    cholangitis_acute_date = Column(Date)
    cholangitis_recurrent = Column(Boolean)
    cholangitis_recurrent_date = Column(Date)
    spleen_palpable = Column(Boolean)
    spleen_palpable_date = Column(Date)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="LiverDisease.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="LiverDisease.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class LiverImaging(Base):
    __tablename__ = "liver_imaging"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date = Column(DateTime(True), nullable=False)
    imaging_type = Column(String, nullable=False)
    size = Column(Numeric)
    hepatic_fibrosis = Column(Boolean)
    hepatic_cysts = Column(Boolean)
    bile_duct_cysts = Column(Boolean)
    dilated_bile_ducts = Column(Boolean)
    cholangitis = Column(Boolean)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="LiverImaging.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="LiverImaging.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class LiverTransplant(Base):
    __tablename__ = "liver_transplants"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    transplant_group_id = Column(ForeignKey("groups.id"))
    registration_date = Column(Date)
    transplant_date = Column(Date, nullable=False)
    indications = Column(ARRAY(String()))
    other_indications = Column(String)
    first_graft_source = Column(String)
    loss_reason = Column(String)
    other_loss_reason = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="LiverTransplant.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="LiverTransplant.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship(
        "Group", primaryjoin="LiverTransplant.source_group_id == Group.id"
    )
    transplant_group = relationship(
        "Group", primaryjoin="LiverTransplant.transplant_group_id == Group.id"
    )


class Medication(Base):
    __tablename__ = "medications"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    drug_id = Column(ForeignKey("drugs.id"))
    dose_quantity = Column(Numeric)
    dose_unit = Column(String)
    frequency = Column(String)
    route = Column(String)
    drug_text = Column(String)
    dose_text = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Medication.created_user_id == User.id"
    )
    drug = relationship("Drug")
    modified_user = relationship(
        "User", primaryjoin="Medication.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class MpgnClinicalPicture(Base):
    __tablename__ = "mpgn_clinical_pictures"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date_of_picture = Column(Date, nullable=False)
    oedema = Column(Boolean)
    hypertension = Column(Boolean)
    urticaria = Column(Boolean)
    partial_lipodystrophy = Column(Boolean)
    infection = Column(Boolean)
    infection_details = Column(String)
    ophthalmoscopy = Column(Boolean)
    ophthalmoscopy_details = Column(String)
    comments = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="MpgnClinicalPicture.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="MpgnClinicalPicture.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class Nephrectomy(Base):
    __tablename__ = "nephrectomies"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    kidney_side = Column(String, nullable=False)
    kidney_type = Column(String, nullable=False)
    entry_type = Column(String, nullable=False)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Nephrectomy.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Nephrectomy.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class NurtureDatum(Base):
    __tablename__ = "nurture_data"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('nurture_data_id_seq'::regclass)"),
    )
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    signed_off_state = Column(Integer)
    follow_up_refused_date = Column(Date)
    blood_tests = Column(Boolean)
    blood_refused_date = Column(Date)
    interviews = Column(Boolean)
    interviews_refused_date = Column(Date)
    created_user_id = Column(Integer, nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(Integer, nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    patient = relationship("Patient")


class NurtureSample(Base):
    __tablename__ = "nurture_samples"
    __table_args__ = {"comment": "see form 11 for current storage"}

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    taken_on = Column(Date, nullable=False)
    barcode = Column(Integer, nullable=False)
    epa = Column(Integer)
    epb = Column(Integer)
    lpa = Column(Integer)
    lpb = Column(Integer)
    uc = Column(Integer)
    ub = Column(Integer)
    ud = Column(Integer)
    fub = Column(Integer)
    sc = Column(Integer)
    sa = Column(Integer)
    sb = Column(Integer)
    rna = Column(Integer)
    wb = Column(Integer)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    protocol_id = Column(ForeignKey("nurture_samples_options.id"), nullable=False)

    created_user = relationship(
        "User", primaryjoin="NurtureSample.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="NurtureSample.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    protocol = relationship("NurtureSamplesOption")


class Nutrition(Base):
    __tablename__ = "nutrition"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    feeding_type = Column(String, nullable=False)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Nutrition.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Nutrition.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class Pathology(Base):
    __tablename__ = "pathology"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    kidney_type = Column(String)
    kidney_side = Column(String)
    reference_number = Column(String)
    image_url = Column(String)
    histological_summary = Column(String)
    em_findings = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    report_cleaned = Column(Date)

    created_user = relationship(
        "User", primaryjoin="Pathology.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Pathology.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class PatientAddress(Base):
    __tablename__ = "patient_addresses"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    from_date = Column(Date)
    to_date = Column(Date)
    address1 = Column(String)
    address2 = Column(String)
    address3 = Column(String)
    postcode = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    address4 = Column(String)
    country = Column(String, server_default=text("'GB'::character varying"))

    created_user = relationship(
        "User", primaryjoin="PatientAddress.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="PatientAddress.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class PatientAliase(Base):
    __tablename__ = "patient_aliases"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="PatientAliase.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="PatientAliase.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class PatientConsent(Base):
    __tablename__ = "patient_consents"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('patient_consents_id_seq'::regclass)"),
    )
    consent_id = Column(ForeignKey("consents.id"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    signed_on_date = Column(Date, nullable=False)
    withdrawn_on_date = Column(Date)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    reconsent_letter_returned_date = Column(Date)
    reconsent_letter_sent_date = Column(Date)

    consent = relationship("Consent")
    created_user = relationship(
        "User", primaryjoin="PatientConsent.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="PatientConsent.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class PatientConsultant(Base):
    __tablename__ = "patient_consultants"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('patient_consultants_id_seq'::regclass)"),
    )
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    consultant_id = Column(ForeignKey("consultants.id"), nullable=False)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    consultant = relationship("Consultant")
    created_user = relationship(
        "User", primaryjoin="PatientConsultant.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="PatientConsultant.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class PatientDemographic(Base):
    __tablename__ = "patient_demographics"
    __table_args__ = (
        Index(
            "patient_demographics_patient_source_idx",
            "patient_id",
            "source_group_id",
            "source_type",
            unique=True,
        ),
    )

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    date_of_death = Column(Date)
    gender = Column(Integer)
    home_number = Column(String)
    work_number = Column(String)
    mobile_number = Column(String)
    email_address = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    ethnicity_id = Column(ForeignKey("ethnicities.id"))
    nationality_id = Column(ForeignKey("nationalities.id"))
    cause_of_death = Column(String)

    created_user = relationship(
        "User", primaryjoin="PatientDemographic.created_user_id == User.id"
    )
    ethnicity = relationship("Ethnicity")
    modified_user = relationship(
        "User", primaryjoin="PatientDemographic.modified_user_id == User.id"
    )
    nationality = relationship("Nationality")
    patient = relationship("Patient")
    source_group = relationship("Group")


class PatientDiagnose(Base):
    __tablename__ = "patient_diagnoses"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    diagnosis_id = Column(ForeignKey("diagnoses.id"))
    diagnosis_text = Column(String)
    symptoms_date = Column(Date)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    gene_test = Column(Boolean)
    biochemistry = Column(Boolean)
    clinical_picture = Column(Boolean)
    biopsy = Column(Boolean)
    biopsy_diagnosis = Column(Integer)
    comments = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    prenatal = Column(Boolean)

    created_user = relationship(
        "User", primaryjoin="PatientDiagnose.created_user_id == User.id"
    )
    diagnosis = relationship("Diagnose")
    modified_user = relationship(
        "User", primaryjoin="PatientDiagnose.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class PatientLock(Base):
    __tablename__ = "patient_locks"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('patient_locks_id_seq'::regclass)"),
    )
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    sequence_number = Column(Integer)

    patient = relationship("Patient")


class PatientNumber(Base):
    __tablename__ = "patient_numbers"
    __table_args__ = (
        Index(
            "patient_numbers_source_number_idx",
            "source_group_id",
            "source_type",
            "number_group_id",
            "number",
            unique=True,
        ),
    )

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    source_type = Column(String, nullable=False)
    number_group_id = Column(ForeignKey("groups.id"), nullable=False, index=True)
    number = Column(String, nullable=False)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="PatientNumber.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="PatientNumber.modified_user_id == User.id"
    )
    number_group = relationship(
        "Group", primaryjoin="PatientNumber.number_group_id == Group.id"
    )
    patient = relationship("Patient")
    source_group = relationship(
        "Group", primaryjoin="PatientNumber.source_group_id == Group.id"
    )


class Plasmapheresi(Base):
    __tablename__ = "plasmapheresis"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    no_of_exchanges = Column(String)
    response = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Plasmapheresi.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Plasmapheresi.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class Pregnancy(Base):
    __tablename__ = "pregnancies"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    pregnancy_number = Column(Integer, nullable=False)
    date_of_lmp = Column(Date, nullable=False)
    gravidity = Column(Integer)
    parity1 = Column(Integer)
    parity2 = Column(Integer)
    outcome = Column(String)
    weight = Column(Integer)
    weight_centile = Column(Integer)
    gestational_age = Column(Integer)
    delivery_method = Column(String)
    neonatal_intensive_care = Column(Boolean)
    pre_eclampsia = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="Pregnancy.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Pregnancy.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class RenalImaging(Base):
    __tablename__ = "renal_imaging"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date = Column(DateTime(True))
    imaging_type = Column(String)
    right_present = Column(Boolean)
    right_type = Column(String)
    right_length = Column(Numeric)
    right_volume = Column(Numeric)
    right_cysts = Column(Boolean)
    right_stones = Column(Boolean)
    right_calcification = Column(Boolean)
    right_nephrocalcinosis = Column(Boolean)
    right_nephrolithiasis = Column(Boolean)
    right_other_malformation = Column(String)
    left_present = Column(Boolean)
    left_type = Column(String)
    left_length = Column(Numeric)
    left_volume = Column(Numeric)
    left_cysts = Column(Boolean)
    left_stones = Column(Boolean)
    left_calcification = Column(Boolean)
    left_nephrocalcinosis = Column(Boolean)
    left_nephrolithiasis = Column(Boolean)
    left_other_malformation = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="RenalImaging.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="RenalImaging.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class RenalProgression(Base):
    __tablename__ = "renal_progressions"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    onset_date = Column(Date)
    esrf_date = Column(Date)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    ckd5_date = Column(Date)
    ckd4_date = Column(Date)
    ckd3a_date = Column(Date)
    ckd3b_date = Column(Date)

    created_user = relationship(
        "User", primaryjoin="RenalProgression.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="RenalProgression.modified_user_id == User.id"
    )
    patient = relationship("Patient", uselist=False)


class Result(Base):
    __tablename__ = "results"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    observation_id = Column(ForeignKey("observations.id"), nullable=False)
    date = Column(DateTime(True), nullable=False)
    value = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    sent_value = Column(String, nullable=False)

    created_user = relationship("User", primaryjoin="Result.created_user_id == User.id")
    modified_user = relationship(
        "User", primaryjoin="Result.modified_user_id == User.id"
    )
    observation = relationship("Observation")
    patient = relationship("Patient")
    source_group = relationship("Group")


class RituximabBaselineAssessment(Base):
    __tablename__ = "rituximab_baseline_assessment"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    nephropathy = Column(String)
    supportive_medication = Column(ARRAY(String()))
    previous_treatment = Column(JSONB(astext_type=Text()))
    steroids = Column(Boolean)
    other_previous_treatment = Column(String)
    past_remission = Column(Boolean)
    performance_status = Column(Integer)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    comorbidities = Column(Boolean, server_default=text("true"))

    created_user = relationship(
        "User", primaryjoin="RituximabBaselineAssessment.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="RituximabBaselineAssessment.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship("Group")


class RituximabCriterion(Base):
    __tablename__ = "rituximab_criteria"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    date = Column(Date, nullable=False)
    criteria1 = Column(Boolean)
    criteria2 = Column(Boolean)
    criteria3 = Column(Boolean)
    criteria4 = Column(Boolean)
    criteria5 = Column(Boolean)
    criteria6 = Column(Boolean)
    criteria7 = Column(Boolean)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    alkylating_complication = Column(Boolean)
    alkylating_failure_monitoring_requirements = Column(Boolean)
    cancer = Column(Boolean)
    cni_failure_monitoring_requirements = Column(Boolean)
    cni_therapy_complication = Column(Boolean)
    diabetes = Column(Boolean)
    drug_associated_toxicity = Column(Boolean)
    fall_in_egfr = Column(Boolean)
    hypersensitivity = Column(Boolean)
    risk_factors = Column(Boolean)
    ongoing_severe_disease = Column(Boolean)
    threatened_fertility = Column(Boolean)
    mood_disturbance = Column(Boolean)
    osteoporosis_osteopenia = Column(Boolean)
    previous_hospitalization = Column(Boolean)

    created_user = relationship(
        "User", primaryjoin="RituximabCriterion.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="RituximabCriterion.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class SaltWastingClinicalFeature(Base):
    __tablename__ = "salt_wasting_clinical_features"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    normal_pregnancy = Column(Boolean)
    abnormal_pregnancy_text = Column(String)
    neurological_problems = Column(Boolean)
    seizures = Column(Boolean)
    abnormal_gait = Column(Boolean)
    deafness = Column(Boolean)
    other_neurological_problem = Column(Boolean)
    other_neurological_problem_text = Column(String)
    joint_problems = Column(Boolean)
    joint_problems_age = Column(Integer)
    x_ray_abnormalities = Column(Boolean)
    chondrocalcinosis = Column(Boolean)
    other_x_ray_abnormality = Column(Boolean)
    other_x_ray_abnormality_text = Column(String)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    created_user = relationship(
        "User", primaryjoin="SaltWastingClinicalFeature.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="SaltWastingClinicalFeature.modified_user_id == User.id"
    )
    patient = relationship("Patient")


class Transplant(Base):
    __tablename__ = "transplants"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_id = Column(
        ForeignKey("patients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    source_group_id = Column(ForeignKey("groups.id"), nullable=False)
    source_type = Column(String, nullable=False)
    transplant_group_id = Column(ForeignKey("groups.id"))
    date = Column(Date, nullable=False)
    modality = Column(Integer, nullable=False)
    date_of_recurrence = Column(Date)
    date_of_failure = Column(Date)
    created_user_id = Column(ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    modified_user_id = Column(ForeignKey("users.id"), nullable=False)
    modified_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    recurrence = Column(Boolean)
    date_of_cmv_infection = Column(Date)
    donor_hla = Column(String)
    recipient_hla = Column(String)
    graft_loss_cause = Column(String)

    created_user = relationship(
        "User", primaryjoin="Transplant.created_user_id == User.id"
    )
    modified_user = relationship(
        "User", primaryjoin="Transplant.modified_user_id == User.id"
    )
    patient = relationship("Patient")
    source_group = relationship(
        "Group", primaryjoin="Transplant.source_group_id == Group.id"
    )
    transplant_group = relationship(
        "Group", primaryjoin="Transplant.transplant_group_id == Group.id"
    )


class BiomarkerSample(Base):
    __tablename__ = "biomarker_samples"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarker_samples_id_seq'::regclass)"),
    )
    barcode_id = Column(ForeignKey("biomarker_barcodes.id", ondelete="CASCADE"))

    label = Column(String(100), nullable=False)

    barcode = relationship("BiomarkerBarcode")


class FamilyHistoryRelative(Base):
    __tablename__ = "family_history_relatives"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('family_history_relatives_id_seq'::regclass)"),
    )
    family_history_id = Column(
        ForeignKey("family_histories.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    relationship = Column(Integer, nullable=False)
    patient_id = Column(
        ForeignKey("patients.id", ondelete="SET NULL", onupdate="CASCADE")
    )


class TransplantBiopsy(Base):
    __tablename__ = "transplant_biopsies"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('transplant_biopsies_id_seq'::regclass)"),
    )
    transplant_id = Column(
        ForeignKey("transplants.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date_of_biopsy = Column(Date, nullable=False)
    recurrence = Column(Boolean)

    transplant = relationship("Transplant")


class TransplantRejection(Base):
    __tablename__ = "transplant_rejections"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('transplant_rejections_id_seq'::regclass)"),
    )
    transplant_id = Column(
        ForeignKey("transplants.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    date_of_rejection = Column(Date, nullable=False)

    transplant = relationship("Transplant")


class BiomarkerResult(Base):
    __tablename__ = "biomarker_results"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarker_results_id_seq'::regclass)"),
    )
    bio_id = Column(ForeignKey("biomarkers.id", ondelete="CASCADE"))
    sample_id = Column(ForeignKey("biomarker_samples.id", ondelete="CASCADE"))
    value = Column(Float(53))
    unit_measure = Column(String(100))
    proc_date = Column(DateTime)
    hospital = Column(String(100))

    bio = relationship("Biomarker")
    sample = relationship("BiomarkerSample")
