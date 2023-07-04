from enum import Enum


class SimpleEnum(Enum):
    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return hash(str(self))


class Gender(SimpleEnum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"


class MaritalStatus(SimpleEnum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"


class Ethnicity(SimpleEnum):
    CAUCASIAN = "Caucasian"
    AFRICAN_AMERICAN = "African-American"
    HISPANIC = "Hispanic"
    ASIAN = "Asian"
    MIXED = "Mixed"


class Nationality(SimpleEnum):
    AMERICAN = "American"
    BRITISH = "British"
    CANADIAN = "Canadian"
    AUSTRALIAN = "Australian"
    GERMAN = "German"


class EducationLevel(SimpleEnum):
    HIGH_SCHOOL = "High School"
    BSC = "BSc"
    MSC = "MSc"
    PHD = "PhD"


class Occupation(SimpleEnum):
    TEACHER = "Teacher"
    ENGINEER = "Engineer"
    DOCTOR = "Doctor"
    ARTIST = "Artist"
    ENTREPRENEUR = "Entrepreneur"


class EmploymentStatus(SimpleEnum):
    EMPLOYED = "Employed"
    UNEMPLOYED = "Unemployed"
    SELF_EMPLOYED = "Self-employed"


class HousingStatus(SimpleEnum):
    RENTING = "Renting"
    OWN_HOME = "Own Home"
    LIVING_WITH_FAMILY = "Living with Family"


class Religion(SimpleEnum):
    CHRISTIANITY = "Christianity"
    ISLAM = "Islam"
    HINDUISM = "Hinduism"
    BUDDHISM = "Buddhism"
    JUDAISM = "Judaism"


class Generation(SimpleEnum):
    BABY_BOOMER = "Baby Boomer"
    GENERATION_X = "Generation X"
    MILLENNIAL = "Millennial"
    GENERATION_Z = "Generation Z"


class LevelOfUrbanization(SimpleEnum):
    URBAN = "Urban"
    SUBURBAN = "Suburban"
    RURAL = "Rural"


class InternetAccess(SimpleEnum):
    HIGH_SPEED = "High-speed"
    MODERATE_SPEED = "Moderate-speed"
    LOW_SPEED = "Low-speed"
    NO_ACCESS = "No access"


class ParentalStatus(SimpleEnum):
    PARENT = "Parent"
    NON_PARENT = "Non-parent"


class PhysicalFitnessLevel(SimpleEnum):
    ACTIVE = "Active"
    MODERATELY_ACTIVE = "Moderately active"
    INACTIVE = "Inactive"


class PetOwnership(SimpleEnum):
    DOG = "Dog"
    CAT = "Cat"
    BIRD = "Bird"
    FISH = "Fish"
    NO_PETS = "No pets"


class CarOwnership(SimpleEnum):
    OWN_A_CAR = "Own a car"
    DO_NOT_OWN_A_CAR = "Do not own a car"


class LifeSatisfaction(SimpleEnum):
    VERY_SATISFIED = "Very satisfied"
    SATISFIED = "Satisfied"
    NEUTRAL = "Neutral"
    DISSATISFIED = "Dissatisfied"
    VERY_DISSATISFIED = "Very dissatisfied"


class SecondLanguageLiteracyLevel(SimpleEnum):
    FLUENT = "Fluent"
    INTERMEDIATE = "Intermediate"
    BASIC = "Basic"
    NOT_LITERATE = "Not literate"


class TypeOfHousing(SimpleEnum):
    APARTMENT = "Apartment"
    HOUSE = "House"
    CONDO = "Condo"
    TOWNHOUSE = "Townhouse"


class HealthCondition(SimpleEnum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"


class DietaryPreferences(SimpleEnum):
    VEGETARIAN = "Vegetarian"
    VEGAN = "Vegan"
    PESCATARIAN = "Pescatarian"
    GLUTEN_FREE = "Gluten-free"
    DAIRY_FREE = "Dairy-free"
    NUT_FREE = "Nut-free"
    HALAL = "Halal"
