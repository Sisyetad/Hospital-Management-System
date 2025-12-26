# User/Permissions/config.py

from constants import roles

ROLE_PERMISSIONS = {

    #Headoffice Permissions
    "HeadofficeView:create":[roles.ROLE_HEADOFFICE],
    "Headofficeview:update":[roles.ROLE_HEADOFFICE],

    # User Permissions
    "UserViewSet:update": ["authenticated"],
    "UserViewSet:destroy": ["authenticated"],
    "UserViewSet:list": ["authenticated"],
    "UserViewSet:retrieve": ["authenticated"],

    # Branch Permissions
    "BranchViewSet:create": [roles.ROLE_HEADOFFICE],
    "BranchViewSet:update": [roles.ROLE_HEADOFFICE],
    "BranchViewSet:destroy": [roles.ROLE_HEADOFFICE],
    "BranchViewSet:list": [roles.ROLE_HEADOFFICE, roles.ROLE_BRANCH, roles.ROLE_DOCTOR, roles.ROLE_RECEPTIONIST],
    "BranchViewSet:retrieve": [roles.ROLE_HEADOFFICE, roles.ROLE_BRANCH],

    # Doctor Permissions
    "DoctorViewSet:create": [roles.ROLE_BRANCH],
    "DoctorViewSet:update": [roles.ROLE_BRANCH],
    "DoctorViewSet:destroy": [roles.ROLE_BRANCH],
    "DoctorViewSet:list": ["authenticated"],
    "DoctorViewSet:retrieve": ["authenticated"],
    "DoctorViewSet:list_available_doctors": ["authenticated"],
    "DoctorViewSet:partial_update": [roles.ROLE_DOCTOR],

    # Receptionist Permissions
    "ReceptionistViewSet:create": [roles.ROLE_BRANCH],
    "ReceptionistViewSet:update": [roles.ROLE_BRANCH],
    "ReceptionistViewSet:destroy": [roles.ROLE_BRANCH],
    "ReceptionistViewSet:list": ["authenticated"],
    "ReceptionistViewSet:retrieve": ["authenticated"],

    # Patient Permissions
    "PatientViewSet:create": [roles.ROLE_RECEPTIONIST],
    "PatientViewSet:update": [roles.ROLE_RECEPTIONIST],
    "PatientViewSet:destroy": [roles.ROLE_RECEPTIONIST],
    "PatientViewSet:list": ["authenticated"],
    "PatientViewSet:retrieve": ["authenticated"],

    # Role Permissions
    "RoleView:create": [roles.ROLE_HEADOFFICE],
    "RoleView:update": [roles.ROLE_HEADOFFICE],
    "RoleView:destroy": [roles.ROLE_HEADOFFICE],
    "RoleView:list": [roles.ROLE_HEADOFFICE, roles.ROLE_BRANCH, roles.ROLE_DOCTOR, roles.ROLE_RECEPTIONIST],

    #Diagnosis Permissions
    "DiagnosisViewSet:create": [roles.ROLE_DOCTOR],
    "DiagnosisViewSet:update": [roles.ROLE_DOCTOR],
    "DiagnosisViewSet:list": [roles.ROLE_HEADOFFICE, roles.ROLE_BRANCH, roles.ROLE_DOCTOR, roles.ROLE_PATIENT],
    "DiagnosisViewSet:retrieve": [roles.ROLE_HEADOFFICE, roles.ROLE_BRANCH, roles.ROLE_DOCTOR, roles.ROLE_PATIENT],
    "DiagnosisViewSet:partial_update":[roles.ROLE_PATIENT],
    "DiagnosisViewSet:display_history":[roles.ROLE_HEADOFFICE],

    #Queue Permissions
    "QueueViewSet:create": [roles.ROLE_RECEPTIONIST],
    "QueueViewSet:update": [roles.ROLE_RECEPTIONIST, roles.ROLE_DOCTOR],
    "QueueViewSet:destroy": [roles.ROLE_RECEPTIONIST],
    "QueueViewSet:list": ["authenticated"],
    "QueueViewSet:retrieve": ["authenticated"],
    "QueueViewSet:partial_update":[roles.ROLE_RECEPTIONIST],
}

